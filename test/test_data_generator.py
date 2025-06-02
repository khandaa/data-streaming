"""
Test data generator for the AWS SQS to Kafka streaming application.
Generates synthetic data for testing the SQS simulator and streaming process.
"""
import json
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Sample data patterns
EVENT_TYPES = ["purchase", "pageview", "login", "logout", "signup", "click", "impression", "error"]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]
STATUS_CODES = [200, 200, 200, 200, 201, 301, 302, 400, 401, 403, 404, 500]
COUNTRIES = ["USA", "UK", "Canada", "Germany", "France", "Japan", "Australia", "Brazil", "India", "China"]
CITIES = ["New York", "London", "Toronto", "Berlin", "Paris", "Tokyo", "Sydney", "Rio", "Mumbai", "Beijing"]
PRODUCTS = ["t-shirt", "jeans", "shoes", "hat", "sunglasses", "watch", "bag", "dress", "jacket", "socks"]
PAYMENT_METHODS = ["credit_card", "paypal", "apple_pay", "google_pay", "bank_transfer"]

class TestDataGenerator:
    """
    Generates test data for simulating SQS messages and streaming.
    """
    
    @staticmethod
    def generate_user_event() -> Dict[str, Any]:
        """
        Generate a random user event.
        
        Returns:
            Dictionary with event data
        """
        event_type = random.choice(EVENT_TYPES)
        timestamp = datetime.now() - timedelta(seconds=random.randint(0, 3600))
        
        # Base event data
        event = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": timestamp.isoformat(),
            "user_id": f"user_{random.randint(1, 1000)}",
            "session_id": f"session_{random.randint(1, 5000)}",
            "user_agent": random.choice(USER_AGENTS),
            "ip_address": f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}",
            "location": {
                "country": random.choice(COUNTRIES),
                "city": random.choice(CITIES),
                "latitude": round(random.uniform(-90, 90), 6),
                "longitude": round(random.uniform(-180, 180), 6)
            }
        }
        
        # Add event-specific data
        if event_type == "purchase":
            items = []
            for _ in range(random.randint(1, 5)):
                items.append({
                    "product_id": f"prod_{random.randint(1, 100)}",
                    "product_name": random.choice(PRODUCTS),
                    "quantity": random.randint(1, 5),
                    "price": round(random.uniform(9.99, 99.99), 2)
                })
            
            event.update({
                "order_id": f"order_{random.randint(10000, 99999)}",
                "items": items,
                "total_amount": sum(item["price"] * item["quantity"] for item in items),
                "currency": "USD",
                "payment_method": random.choice(PAYMENT_METHODS),
                "shipping_address": {
                    "street": f"{random.randint(1, 999)} Main St",
                    "city": event["location"]["city"],
                    "country": event["location"]["country"],
                    "postal_code": f"{random.randint(10000, 99999)}"
                }
            })
        elif event_type == "pageview":
            event.update({
                "page_url": f"https://example.com/{random.choice(['home', 'products', 'about', 'contact', 'blog'])}",
                "referrer": random.choice([
                    "https://www.google.com/",
                    "https://www.facebook.com/",
                    "https://www.twitter.com/",
                    "https://www.instagram.com/",
                    "direct"
                ]),
                "time_on_page": random.randint(5, 300)
            })
        elif event_type in ["login", "logout", "signup"]:
            event.update({
                "success": random.choice([True, True, True, False]),
                "method": random.choice(["email", "google", "facebook", "apple", "twitter"]),
                "device_type": random.choice(["desktop", "mobile", "tablet"])
            })
        elif event_type in ["click", "impression"]:
            event.update({
                "element_id": f"el_{random.randint(1, 100)}",
                "element_type": random.choice(["button", "link", "image", "video", "banner"]),
                "page_section": random.choice(["header", "footer", "sidebar", "main", "navigation"])
            })
        elif event_type == "error":
            event.update({
                "error_code": random.choice(STATUS_CODES),
                "error_message": random.choice([
                    "Connection timeout",
                    "Invalid credentials",
                    "Resource not found",
                    "Server error",
                    "Permission denied"
                ]),
                "stack_trace": f"Error at line {random.randint(1, 1000)}"
            })
        
        return event
    
    @staticmethod
    def generate_sensor_data() -> Dict[str, Any]:
        """
        Generate random IoT sensor data.
        
        Returns:
            Dictionary with sensor data
        """
        sensor_types = ["temperature", "humidity", "pressure", "light", "motion", "air_quality", "sound"]
        sensor_type = random.choice(sensor_types)
        
        # Base sensor data
        data = {
            "sensor_id": f"sensor_{random.randint(1, 100)}",
            "device_id": f"device_{random.randint(1, 50)}",
            "timestamp": datetime.now().isoformat(),
            "sensor_type": sensor_type,
            "location": {
                "building": f"Building {random.randint(1, 5)}",
                "floor": random.randint(1, 10),
                "room": f"Room {random.randint(101, 999)}",
                "latitude": round(random.uniform(-90, 90), 6),
                "longitude": round(random.uniform(-180, 180), 6)
            },
            "battery_level": random.randint(1, 100),
            "status": random.choice(["active", "active", "active", "warning", "error"]),
            "firmware_version": f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 99)}"
        }
        
        # Add sensor-specific readings
        if sensor_type == "temperature":
            data["reading"] = {
                "value": round(random.uniform(-10, 40), 1),
                "unit": "celsius"
            }
        elif sensor_type == "humidity":
            data["reading"] = {
                "value": round(random.uniform(0, 100), 1),
                "unit": "percent"
            }
        elif sensor_type == "pressure":
            data["reading"] = {
                "value": round(random.uniform(980, 1050), 1),
                "unit": "hPa"
            }
        elif sensor_type == "light":
            data["reading"] = {
                "value": random.randint(0, 1000),
                "unit": "lux"
            }
        elif sensor_type == "motion":
            data["reading"] = {
                "value": random.choice([True, False]),
                "last_motion": datetime.now().isoformat() if random.choice([True, False]) else None
            }
        elif sensor_type == "air_quality":
            data["reading"] = {
                "co2": random.randint(300, 2000),
                "tvoc": random.randint(0, 1000),
                "pm25": round(random.uniform(0, 100), 1),
                "pm10": round(random.uniform(0, 150), 1),
                "aqi": random.randint(0, 500)
            }
        elif sensor_type == "sound":
            data["reading"] = {
                "value": random.randint(30, 100),
                "unit": "dB"
            }
        
        return data
    
    @staticmethod
    def generate_log_entry() -> Dict[str, Any]:
        """
        Generate a random log entry.
        
        Returns:
            Dictionary with log data
        """
        log_levels = ["DEBUG", "INFO", "INFO", "WARNING", "ERROR", "CRITICAL"]
        services = ["api", "auth", "database", "notification", "payment", "user", "order", "inventory"]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "level": random.choice(log_levels),
            "service": random.choice(services),
            "instance": f"instance-{random.randint(1, 10)}",
            "message": f"Log message {random.randint(1000, 9999)}",
            "trace_id": str(uuid.uuid4()),
            "request_id": str(uuid.uuid4()),
            "user_id": f"user_{random.randint(1, 1000)}",
            "duration_ms": random.randint(1, 10000),
            "status_code": random.choice(STATUS_CODES),
            "endpoint": f"/{random.choice(['api', 'v1', 'v2'])}/{random.choice(services)}/{random.choice(['get', 'create', 'update', 'delete'])}",
            "method": random.choice(["GET", "POST", "PUT", "DELETE"]),
            "user_agent": random.choice(USER_AGENTS),
            "ip_address": f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
        }
    
    @classmethod
    def generate_batch(cls, count: int = 10, data_type: str = "mixed") -> List[Dict[str, Any]]:
        """
        Generate a batch of test data.
        
        Args:
            count: Number of data items to generate
            data_type: Type of data to generate (user_event, sensor_data, log_entry, or mixed)
            
        Returns:
            List of data dictionaries
        """
        batch = []
        
        for _ in range(count):
            if data_type == "user_event":
                batch.append(cls.generate_user_event())
            elif data_type == "sensor_data":
                batch.append(cls.generate_sensor_data())
            elif data_type == "log_entry":
                batch.append(cls.generate_log_entry())
            elif data_type == "mixed":
                generator = random.choice([
                    cls.generate_user_event,
                    cls.generate_sensor_data,
                    cls.generate_log_entry
                ])
                batch.append(generator())
            else:
                raise ValueError(f"Unknown data type: {data_type}")
        
        return batch
    
    @classmethod
    def generate_to_file(cls, filename: str, count: int = 100, data_type: str = "mixed", batch_size: int = 10):
        """
        Generate test data and save to a file.
        
        Args:
            filename: Path to the output file
            count: Total number of data items to generate
            data_type: Type of data to generate
            batch_size: Number of items to generate in each batch
        """
        with open(filename, 'w') as f:
            for i in range(0, count, batch_size):
                batch_count = min(batch_size, count - i)
                batch = cls.generate_batch(batch_count, data_type)
                
                for item in batch:
                    f.write(json.dumps(item) + "\n")
                    
                # Progress indicator
                print(f"Generated {min(i + batch_count, count)} of {count} items", end="\r")
                
                # Small delay to make timestamps more realistic
                time.sleep(0.01)
                
        print(f"\nGenerated {count} items and saved to {filename}")

if __name__ == "__main__":
    # Generate sample test data
    TestDataGenerator.generate_to_file("test_data.json", count=100)
    
    # Generate specific test data types
    TestDataGenerator.generate_to_file("user_events.json", count=50, data_type="user_event")
    TestDataGenerator.generate_to_file("sensor_data.json", count=50, data_type="sensor_data")
    TestDataGenerator.generate_to_file("log_entries.json", count=50, data_type="log_entry")
