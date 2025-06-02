"""
Test Data Generator for the data streaming application.
Generates various types of test data for unit and integration testing.
"""
import json
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

class TestDataGenerator:
    """
    Generates test data for the data streaming application.
    """
    
    @staticmethod
    def generate_user_event() -> Dict[str, Any]:
        """
        Generate a sample user event for testing.
        
        Returns:
            Dict: A dictionary containing user event data
        """
        event_types = [
            "login", "logout", "purchase", "page_view", 
            "click", "signup", "account_update", "settings_change"
        ]
        
        platforms = ["web", "ios", "android", "desktop"]
        browsers = ["chrome", "firefox", "safari", "edge", None]
        countries = ["US", "UK", "CA", "AU", "DE", "FR", "JP", "IN"]
        
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        session_id = f"session_{uuid.uuid4().hex}"
        
        event = {
            "event_id": str(uuid.uuid4()),
            "event_type": random.choice(event_types),
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "session_id": session_id,
            "platform": random.choice(platforms),
            "browser": random.choice(browsers) if random.random() > 0.3 else None,
            "country": random.choice(countries),
            "ip_address": f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
            "device_id": f"device_{uuid.uuid4().hex[:10]}",
            "data": {
                "page": f"/page_{random.randint(1, 100)}",
                "referrer": f"/page_{random.randint(1, 100)}" if random.random() > 0.5 else None,
                "duration_sec": random.randint(5, 300) if random.random() > 0.3 else None,
                "successful": random.random() > 0.1
            }
        }
        
        # Add some purchase-specific data if it's a purchase event
        if event["event_type"] == "purchase":
            event["data"]["transaction"] = {
                "transaction_id": f"tx_{uuid.uuid4().hex[:10]}",
                "amount": round(random.uniform(10, 1000), 2),
                "currency": "USD",
                "items": random.randint(1, 10),
                "payment_method": random.choice(["credit_card", "paypal", "apple_pay", "google_pay"])
            }
            
        return event
    
    @staticmethod
    def generate_sensor_data() -> Dict[str, Any]:
        """
        Generate sample IoT sensor data for testing.
        
        Returns:
            Dict: A dictionary containing sensor data
        """
        sensor_types = ["temperature", "humidity", "pressure", "light", "motion", "air_quality"]
        locations = ["room_1", "room_2", "kitchen", "living_room", "outdoor", "basement"]
        
        sensor_id = f"sensor_{random.randint(1000, 9999)}"
        device_id = f"device_{random.randint(100, 999)}"
        
        # Base values for different sensor types
        base_values = {
            "temperature": 21.0,  # Celsius
            "humidity": 45.0,     # Percentage
            "pressure": 1013.0,   # hPa
            "light": 450.0,       # Lux
            "motion": 0.0,        # Binary
            "air_quality": 50.0   # AQI
        }
        
        # Variation ranges for different sensor types
        variations = {
            "temperature": 10.0,
            "humidity": 20.0,
            "pressure": 10.0,
            "light": 200.0,
            "motion": 1.0,
            "air_quality": 30.0
        }
        
        # Choose a sensor type
        sensor_type = random.choice(sensor_types)
        
        # Generate value with some randomness around the base
        base = base_values[sensor_type]
        variation = variations[sensor_type]
        value = base + (random.random() * 2 - 1) * variation
        
        # For motion, make it binary (0 or 1)
        if sensor_type == "motion":
            value = 1 if random.random() > 0.7 else 0
        
        # Create the sensor reading
        data = {
            "reading_id": str(uuid.uuid4()),
            "sensor_id": sensor_id,
            "device_id": device_id,
            "sensor_type": sensor_type,
            "timestamp": datetime.now().isoformat(),
            "location": random.choice(locations),
            "value": round(value, 2),
            "unit": self._get_unit_for_sensor_type(sensor_type),
            "battery_level": random.randint(1, 100) if random.random() > 0.2 else None,
            "metadata": {
                "firmware_version": f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
                "installation_date": (datetime.now() - timedelta(days=random.randint(1, 500))).strftime("%Y-%m-%d"),
                "last_maintenance": (datetime.now() - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d") if random.random() > 0.3 else None
            }
        }
        
        return data
    
    @staticmethod
    def _get_unit_for_sensor_type(sensor_type: str) -> str:
        """
        Get the appropriate unit for a sensor type.
        
        Args:
            sensor_type: Type of the sensor
            
        Returns:
            str: The appropriate unit
        """
        units = {
            "temperature": "celsius",
            "humidity": "percent",
            "pressure": "hPa",
            "light": "lux",
            "motion": "binary",
            "air_quality": "aqi"
        }
        return units.get(sensor_type, "unknown")
    
    @staticmethod
    def generate_log_entry() -> Dict[str, Any]:
        """
        Generate a sample log entry for testing.
        
        Returns:
            Dict: A dictionary containing log entry data
        """
        log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        services = ["api", "auth", "database", "frontend", "backend", "worker", "scheduler"]
        
        # Weight log levels to make critical errors less common
        level_weights = [0.4, 0.3, 0.2, 0.08, 0.02]
        log_level = random.choices(log_levels, weights=level_weights)[0]
        
        # Generate random trace and span IDs for distributed tracing
        trace_id = uuid.uuid4().hex
        span_id = uuid.uuid4().hex[:16]
        
        # Create common log entry structure
        log_entry = {
            "log_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "level": log_level,
            "service": random.choice(services),
            "instance_id": f"i-{uuid.uuid4().hex[:8]}",
            "trace_id": trace_id,
            "span_id": span_id,
            "message": TestDataGenerator._generate_log_message(log_level),
            "context": {
                "request_id": uuid.uuid4().hex if random.random() > 0.3 else None,
                "user_id": f"user_{uuid.uuid4().hex[:8]}" if random.random() > 0.5 else None,
                "resource": f"/{random.choice(['api', 'auth', 'admin'])}/v1/{random.choice(['users', 'orders', 'products', 'settings'])}" if random.random() > 0.4 else None
            }
        }
        
        # Add error details for warning, error and critical logs
        if log_level in ["WARNING", "ERROR", "CRITICAL"]:
            log_entry["error"] = {
                "code": random.randint(400, 599),
                "type": random.choice(["ValidationError", "AuthenticationError", "DatabaseError", "TimeoutError", "InternalServerError"]),
                "stack_trace": TestDataGenerator._generate_stack_trace() if log_level in ["ERROR", "CRITICAL"] else None
            }
        
        # Add performance metrics sometimes
        if random.random() > 0.7:
            log_entry["performance"] = {
                "duration_ms": random.randint(1, 10000),
                "cpu_percent": random.uniform(0.1, 100.0),
                "memory_mb": random.uniform(10, 1024)
            }
            
        return log_entry
    
    @staticmethod
    def _generate_log_message(level: str) -> str:
        """
        Generate a realistic looking log message based on the log level.
        
        Args:
            level: The log level
            
        Returns:
            str: A log message
        """
        if level == "DEBUG":
            messages = [
                "Initializing component",
                "Processing request parameters",
                "Cache hit for key",
                "Retrieved 23 records from database",
                "API response received in 127ms",
                "Connection established to service",
                "Thread pool status: 4/10 active"
            ]
        elif level == "INFO":
            messages = [
                "User successfully authenticated",
                "Payment processed successfully",
                "New account created",
                "Email notification sent",
                "Database migration completed",
                "Scheduled task started",
                "API request completed successfully"
            ]
        elif level == "WARNING":
            messages = [
                "Rate limit threshold approaching",
                "Database connection pool running low",
                "API endpoint deprecated, please upgrade",
                "High memory usage detected",
                "Slow query execution (>500ms)",
                "Retrying failed operation (attempt 2/3)",
                "Cache miss rate above normal"
            ]
        elif level == "ERROR":
            messages = [
                "Failed to connect to database",
                "API request timeout after 30s",
                "Payment processing failed",
                "Unable to send email notification",
                "Invalid authentication token",
                "Database query execution error",
                "Service dependency unavailable"
            ]
        else:  # CRITICAL
            messages = [
                "System is out of disk space",
                "Database connection pool exhausted",
                "Fatal exception in main application thread",
                "Security breach detected",
                "Data corruption detected",
                "Unrecoverable system state",
                "Emergency shutdown initiated"
            ]
            
        return random.choice(messages)
    
    @staticmethod
    def _generate_stack_trace() -> str:
        """
        Generate a realistic looking stack trace.
        
        Returns:
            str: A stack trace
        """
        stack_traces = [
            """Traceback (most recent call last):
  File "/app/services/api.py", line 142, in process_request
    result = database.execute_query(query)
  File "/app/database/client.py", line 85, in execute_query
    connection = self.get_connection()
  File "/app/database/client.py", line 32, in get_connection
    return self.connection_pool.acquire()
  File "/app/database/pool.py", line 67, in acquire
    raise DatabaseError("Connection pool exhausted")
DatabaseError: Connection pool exhausted""",

            """Traceback (most recent call last):
  File "/app/workers/processor.py", line 78, in run
    message = self.queue.get(timeout=5)
  File "/usr/local/lib/python3.9/queue.py", line 178, in get
    raise Empty
EmptyQueueError: Timeout waiting for queue message""",

            """Traceback (most recent call last):
  File "/app/auth/jwt.py", line 56, in validate_token
    decoded = jwt.decode(token, self.secret_key, algorithms=["HS256"])
  File "/usr/local/lib/python3.9/site-packages/jwt/api_jwt.py", line 112, in decode
    raise InvalidTokenError("Signature verification failed")
jwt.exceptions.InvalidTokenError: Signature verification failed"""
        ]
        
        return random.choice(stack_traces)
    
    @staticmethod
    def generate_batch(data_type: str, count: int = 10) -> List[Dict[str, Any]]:
        """
        Generate a batch of test data.
        
        Args:
            data_type: Type of data to generate ('user_event', 'sensor_data', or 'log_entry')
            count: Number of items to generate
            
        Returns:
            List[Dict]: A list of generated data items
        """
        generators = {
            'user_event': TestDataGenerator.generate_user_event,
            'sensor_data': TestDataGenerator.generate_sensor_data,
            'log_entry': TestDataGenerator.generate_log_entry
        }
        
        if data_type not in generators:
            raise ValueError(f"Unknown data type: {data_type}. Must be one of {list(generators.keys())}")
            
        return [generators[data_type]() for _ in range(count)]
    
    @staticmethod
    def generate_simple_message() -> Dict[str, Any]:
        """
        Generate a simple message for basic testing.
        
        Returns:
            Dict: A simple message
        """
        return {
            "message_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "content": f"Test message {random.randint(1, 1000)}",
            "priority": random.choice(["low", "medium", "high"]),
            "attributes": {
                "test": True,
                "sequence": random.randint(1, 1000)
            }
        }
        
    @staticmethod
    def generate_to_file(file_path: str, count: int = 100, data_type: str = "mixed", batch_size: int = 10) -> bool:
        """
        Generate test data and write it to a file.
        
        Args:
            file_path: Path to output file
            count: Number of data items to generate
            data_type: Type of data to generate ('user_event', 'sensor_data', 'log_entry', or 'mixed')
            batch_size: Number of items to generate in each batch
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if data_type == "mixed":
                # Generate a mix of all data types
                data_types = ["user_event", "sensor_data", "log_entry"]
                data = []
                
                # Distribute count roughly evenly among data types
                type_count = count // len(data_types)
                remaining = count % len(data_types)
                
                for dt in data_types:
                    # Add an extra item for some types if there's a remainder
                    curr_count = type_count + (1 if remaining > 0 else 0)
                    remaining -= 1 if remaining > 0 else 0
                    
                    data.extend(TestDataGenerator.generate_batch(dt, curr_count))
                    
                # Shuffle to mix data types
                random.shuffle(data)
            else:
                # Generate specific data type
                data = TestDataGenerator.generate_batch(data_type, count)
            
            # Write to file
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
                
            return True
        except Exception as e:
            print(f"Error generating test data: {e}")
            return False
