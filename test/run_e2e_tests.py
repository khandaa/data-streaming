#!/usr/bin/env python3
"""
End-to-End Test Runner for AWS SQS to Kafka Streaming Application.

This script orchestrates the complete end-to-end testing process:
1. Starts the local Kafka cluster using Docker Compose
2. Runs individual component tests
3. Runs the complete streaming process test
4. Shuts down the Kafka cluster
"""
import argparse
import logging
import os
import subprocess
import sys
import time
from typing import List, Dict, Any, Tuple

# Add project root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Add test-data folder to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'test-data'))

from test.test_sqs_simulator_connector import SQSSimulatorTest
from test.test_kafka_connector import KafkaConnectorTest
from test.test_stream_processor import StreamProcessorTest
from data_generator import TestDataGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EndToEndTestRunner:
    """
    Orchestrates the end-to-end test process for the streaming application.
    """
    
    def __init__(
        self,
        docker_compose_file: str = "../docker-compose.test.yml",
        bootstrap_servers: str = "localhost:29092",
        sqs_queue: str = "sqs-queue-1",
        kafka_topic: str = "streaming-topic",
        skip_docker: bool = False
    ):
        """
        Initialize the test runner.
        
        Args:
            docker_compose_file: Path to the Docker Compose file
            bootstrap_servers: Kafka bootstrap servers
            sqs_queue: Name of the SQS simulator queue
            kafka_topic: Name of the destination Kafka topic
            skip_docker: If True, skip Docker Compose start/stop (useful if already running)
        """
        self.docker_compose_file = os.path.abspath(os.path.join(os.path.dirname(__file__), docker_compose_file))
        self.bootstrap_servers = bootstrap_servers
        self.sqs_queue = sqs_queue
        self.kafka_topic = kafka_topic
        self.skip_docker = skip_docker
        
        # Test results tracking
        self.test_results = {}
        
    def start_kafka_cluster(self) -> bool:
        """
        Start the Kafka cluster using Docker Compose.
        
        Returns:
            True if successful, False otherwise
        """
        if self.skip_docker:
            logger.info("Skipping Docker Compose start (--skip-docker flag used)")
            return True
            
        logger.info(f"Starting Kafka cluster using Docker Compose file: {self.docker_compose_file}")
        
        try:
            result = subprocess.run(
                ["docker-compose", "-f", self.docker_compose_file, "up", "-d"],
                check=True,
                capture_output=True,
                text=True
            )
            
            logger.info(f"Docker Compose output: {result.stdout}")
            
            # Wait for Kafka to become available
            logger.info("Waiting for Kafka cluster to become available...")
            time.sleep(10)  # Adjust based on startup time requirements
            
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start Kafka cluster: {e}")
            logger.error(f"Docker Compose error output: {e.stderr}")
            return False
    
    def stop_kafka_cluster(self) -> bool:
        """
        Stop the Kafka cluster using Docker Compose.
        
        Returns:
            True if successful, False otherwise
        """
        if self.skip_docker:
            logger.info("Skipping Docker Compose stop (--skip-docker flag used)")
            return True
            
        logger.info("Stopping Kafka cluster...")
        
        try:
            result = subprocess.run(
                ["docker-compose", "-f", self.docker_compose_file, "down"],
                check=True,
                capture_output=True,
                text=True
            )
            
            logger.info(f"Docker Compose output: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to stop Kafka cluster: {e}")
            logger.error(f"Docker Compose error output: {e.stderr}")
            return False
    
    def check_kafka_status(self) -> bool:
        """
        Check if Kafka is running properly.
        
        Returns:
            True if Kafka is healthy, False otherwise
        """
        logger.info("Checking Kafka status...")
        
        try:
            # Test Kafka connector to see if Kafka is responsive
            kafka_test = KafkaConnectorTest(
                bootstrap_servers=self.bootstrap_servers,
                topic="test-kafka-health"
            )
            
            # If we can create a topic, Kafka is working
            return kafka_test.test_ensure_topic_exists()
        except Exception as e:
            logger.error(f"Kafka health check failed: {e}")
            return False
    
    def generate_test_data(self) -> str:
        """
        Generate test data for use in tests.
        
        Returns:
            Path to the generated test data file
        """
        logger.info("Generating test data...")
        
        test_data_file = os.path.join(os.path.dirname(__file__), "test-data", "e2e_test_data.json")
        
        # Generate a mix of data types
        TestDataGenerator.generate_to_file(
            test_data_file,
            count=100,
            data_type="mixed",
            batch_size=10
        )
        
        return test_data_file
    
    def run_component_tests(self) -> Dict[str, bool]:
        """
        Run individual component tests.
        
        Returns:
            Dictionary with test results
        """
        logger.info("=== Running Component Tests ===")
        results = {}
        
        # Test SQS Simulator
        logger.info("Running SQS Simulator tests...")
        sqs_test = SQSSimulatorTest(
            bootstrap_servers=self.bootstrap_servers,
            queue_name=self.sqs_queue
        )
        results["sqs_simulator"] = sqs_test.run_all_tests()
        
        # Test Kafka Connector
        logger.info("Running Kafka Connector tests...")
        kafka_test = KafkaConnectorTest(
            bootstrap_servers=self.bootstrap_servers,
            topic=self.kafka_topic
        )
        results["kafka_connector"] = kafka_test.run_all_tests()
        
        return results
    
    def run_stream_processor_test(self) -> bool:
        """
        Run the stream processor test.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("=== Running Stream Processor Test ===")
        
        stream_test = StreamProcessorTest(
            bootstrap_servers=self.bootstrap_servers,
            sqs_queue=self.sqs_queue,
            kafka_topic=self.kafka_topic
        )
        
        return stream_test.run_all_tests()
    
    def run_all_tests(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Run the complete end-to-end test suite.
        
        Returns:
            Tuple containing overall success status and detailed results
        """
        logger.info("=== Starting End-to-End Tests ===")
        
        # Step 1: Start Kafka cluster
        kafka_started = self.start_kafka_cluster()
        self.test_results["kafka_cluster_start"] = kafka_started
        
        if not kafka_started and not self.skip_docker:
            logger.error("Failed to start Kafka cluster, cannot proceed with tests")
            return False, self.test_results
        
        # Step 2: Check Kafka status
        kafka_healthy = self.check_kafka_status()
        self.test_results["kafka_health"] = kafka_healthy
        
        if not kafka_healthy:
            logger.error("Kafka is not healthy, cannot proceed with tests")
            self.stop_kafka_cluster()
            return False, self.test_results
        
        # Step 3: Generate test data
        try:
            test_data_file = self.generate_test_data()
            self.test_results["test_data_generation"] = True
        except Exception as e:
            logger.error(f"Failed to generate test data: {e}")
            self.test_results["test_data_generation"] = False
        
        # Step 4: Run component tests
        component_results = self.run_component_tests()
        self.test_results["component_tests"] = component_results
        
        # Check if component tests were successful
        component_success = all(component_results.values())
        
        if not component_success:
            logger.warning("Some component tests failed, but continuing with stream processor test")
        
        # Step 5: Run stream processor test
        stream_processor_success = self.run_stream_processor_test()
        self.test_results["stream_processor_test"] = stream_processor_success
        
        # Step 6: Stop Kafka cluster
        kafka_stopped = self.stop_kafka_cluster()
        self.test_results["kafka_cluster_stop"] = kafka_stopped
        
        # Determine overall success
        overall_success = (
            kafka_started and 
            kafka_healthy and 
            component_success and 
            stream_processor_success and 
            kafka_stopped
        )
        
        # Print summary
        self.print_test_summary()
        
        logger.info(f"=== End-to-End Tests {'Passed' if overall_success else 'Failed'} ===")
        
        return overall_success, self.test_results
    
    def print_test_summary(self):
        """
        Print a summary of test results.
        """
        logger.info("=== Test Summary ===")
        
        # Kafka cluster status
        kafka_start = self.test_results.get("kafka_cluster_start", False)
        kafka_health = self.test_results.get("kafka_health", False)
        kafka_stop = self.test_results.get("kafka_cluster_stop", False)
        
        logger.info(f"Kafka Cluster Start: {'✅' if kafka_start else '❌'}")
        logger.info(f"Kafka Health Check: {'✅' if kafka_health else '❌'}")
        logger.info(f"Kafka Cluster Stop: {'✅' if kafka_stop else '❌'}")
        
        # Test data generation
        data_gen = self.test_results.get("test_data_generation", False)
        logger.info(f"Test Data Generation: {'✅' if data_gen else '❌'}")
        
        # Component tests
        component_tests = self.test_results.get("component_tests", {})
        logger.info("Component Tests:")
        for component, result in component_tests.items():
            logger.info(f"  - {component}: {'✅' if result else '❌'}")
        
        # Stream processor test
        stream_test = self.test_results.get("stream_processor_test", False)
        logger.info(f"Stream Processor Test: {'✅' if stream_test else '❌'}")
        
        # Overall result
        overall_success = (
            kafka_start and 
            kafka_health and 
            all(component_tests.values()) and 
            stream_test and 
            kafka_stop
        )
        
        logger.info(f"Overall Result: {'✅ PASSED' if overall_success else '❌ FAILED'}")

def parse_args():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Run end-to-end tests for SQS to Kafka streaming application")
    
    parser.add_argument(
        "--skip-docker", 
        action="store_true", 
        help="Skip Docker Compose start/stop (use if Kafka is already running)"
    )
    
    parser.add_argument(
        "--bootstrap-servers", 
        default="localhost:29092", 
        help="Kafka bootstrap servers (default: localhost:29092)"
    )
    
    parser.add_argument(
        "--sqs-queue", 
        default="sqs-queue-1", 
        help="SQS simulator queue name (default: sqs-queue-1)"
    )
    
    parser.add_argument(
        "--kafka-topic", 
        default="streaming-topic", 
        help="Destination Kafka topic (default: streaming-topic)"
    )
    
    parser.add_argument(
        "--docker-compose-file", 
        default="../docker-compose.test.yml", 
        help="Path to Docker Compose file (default: ../docker-compose.test.yml)"
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    runner = EndToEndTestRunner(
        docker_compose_file=args.docker_compose_file,
        bootstrap_servers=args.bootstrap_servers,
        sqs_queue=args.sqs_queue,
        kafka_topic=args.kafka_topic,
        skip_docker=args.skip_docker
    )
    
    success, _ = runner.run_all_tests()
    
    # Set exit code based on test result
    sys.exit(0 if success else 1)
