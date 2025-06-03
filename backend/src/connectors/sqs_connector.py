"""
AWS SQS Connector for retrieving messages from an SQS queue.
This connector can work with queues located on a different subnet.
"""
import json
import time
import logging
from typing import Dict, List, Any, Optional

import boto3
from botocore.exceptions import ClientError

from src.config.config import (
    AWS_REGION,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    SQS_QUEUE_URL,
    SQS_SUBNET_ID,
    VPC_ID
)

logger = logging.getLogger(__name__)

class SQSConnector:
    """
    Connector class for AWS SQS.
    
    This class handles connection to AWS SQS queue and provides methods
    to retrieve, process and delete messages from the queue.
    """
    
    def __init__(self, queue_url: Optional[str] = None, region: Optional[str] = None):
        """
        Initialize the SQS connector.
        
        Args:
            queue_url: URL of the SQS queue. Defaults to value from config.
            region: AWS region. Defaults to value from config.
        """
        self.queue_url = queue_url or SQS_QUEUE_URL
        self.region = region or AWS_REGION
        
        # Check if credentials are provided
        if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
            logger.info("Using AWS IAM role for authentication")
            self.sqs = boto3.client('sqs', region_name=self.region)
        else:
            logger.info("Using AWS access key for authentication")
            self.sqs = boto3.client(
                'sqs', 
                region_name=self.region,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
        
        # For cross-subnet communication, we need to use VPC endpoints
        if SQS_SUBNET_ID and VPC_ID:
            logger.info(f"Using VPC endpoint for subnet {SQS_SUBNET_ID}")
            self._setup_vpc_endpoint()

    def _setup_vpc_endpoint(self):
        """
        Set up a VPC endpoint for SQS to allow cross-subnet communication.
        This is needed when the SQS queue is in a different subnet.
        """
        try:
            ec2 = boto3.client(
                'ec2',
                region_name=self.region,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            
            # Create a VPC endpoint for SQS if it doesn't exist
            response = ec2.describe_vpc_endpoints(
                Filters=[
                    {
                        'Name': 'vpc-id',
                        'Values': [VPC_ID]
                    },
                    {
                        'Name': 'service-name',
                        'Values': [f'com.amazonaws.{self.region}.sqs']
                    }
                ]
            )
            
            if not response['VpcEndpoints']:
                logger.info(f"Creating VPC endpoint for SQS in VPC {VPC_ID}")
                ec2.create_vpc_endpoint(
                    VpcId=VPC_ID,
                    ServiceName=f'com.amazonaws.{self.region}.sqs',
                    SubnetIds=[SQS_SUBNET_ID],
                    VpcEndpointType='Interface',
                    PrivateDnsEnabled=True
                )
                logger.info("VPC endpoint created successfully")
            else:
                logger.info("VPC endpoint for SQS already exists")
                
        except ClientError as e:
            logger.error(f"Error setting up VPC endpoint: {e}")
            raise

    def receive_messages(self, max_messages: int = 10, wait_time: int = 20) -> List[Dict[str, Any]]:
        """
        Receive messages from the SQS queue.
        
        Args:
            max_messages: Maximum number of messages to receive (1-10)
            wait_time: Long polling wait time in seconds (0-20)
            
        Returns:
            List of messages, each as a dictionary
        """
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time,
                AttributeNames=['All'],
                MessageAttributeNames=['All']
            )
            
            messages = response.get('Messages', [])
            logger.info(f"Received {len(messages)} messages from SQS")
            
            # Process messages and extract the body
            processed_messages = []
            for message in messages:
                try:
                    # Parse the message body as JSON if possible
                    body = message['Body']
                    message_id = message['MessageId']
                    receipt_handle = message['ReceiptHandle']
                    
                    try:
                        body_json = json.loads(body)
                    except json.JSONDecodeError:
                        body_json = {"raw_message": body}
                    
                    processed_messages.append({
                        'message_id': message_id,
                        'receipt_handle': receipt_handle,
                        'body': body_json,
                        'attributes': message.get('Attributes', {}),
                        'message_attributes': message.get('MessageAttributes', {})
                    })
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
            
            return processed_messages
            
        except ClientError as e:
            logger.error(f"Error receiving messages: {e}")
            return []

    def delete_message(self, receipt_handle: str) -> bool:
        """
        Delete a message from the queue after processing.
        
        Args:
            receipt_handle: The receipt handle of the message to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
            logger.debug(f"Deleted message with receipt handle {receipt_handle[:10]}...")
            return True
        except ClientError as e:
            logger.error(f"Error deleting message: {e}")
            return False
    
    def send_message(self, message_body: Dict[str, Any]) -> Optional[str]:
        """
        Send a message to the SQS queue.
        
        Args:
            message_body: Message body as a dictionary, will be converted to JSON
            
        Returns:
            Message ID if successful, None otherwise
        """
        try:
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message_body)
            )
            message_id = response['MessageId']
            logger.info(f"Sent message to SQS with ID {message_id}")
            return message_id
        except ClientError as e:
            logger.error(f"Error sending message: {e}")
            return None
    
    def stream_messages(self, handler_func, poll_interval: int = 5, max_messages: int = 10):
        """
        Stream messages continuously from the queue and process them with a handler function.
        
        Args:
            handler_func: Function that will process each message
            poll_interval: Time to wait between polling attempts in seconds
            max_messages: Maximum number of messages to retrieve per poll
        """
        logger.info(f"Starting SQS message streaming from {self.queue_url}")
        while True:
            try:
                messages = self.receive_messages(max_messages=max_messages)
                
                for message in messages:
                    # Process the message with the handler function
                    result = handler_func(message)
                    
                    # If processing was successful, delete the message from the queue
                    if result:
                        self.delete_message(message['receipt_handle'])
                
                # If no messages were received, wait before polling again
                if not messages:
                    time.sleep(poll_interval)
                    
            except Exception as e:
                logger.error(f"Error in message streaming loop: {e}")
                time.sleep(poll_interval)  # Wait before retrying
