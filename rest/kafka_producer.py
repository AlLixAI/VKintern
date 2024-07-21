from aiokafka import AIOKafkaProducer
import json

class KafkaProducer:
    def __init__(self, bootstrap_servers: str, client_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.client_id = client_id
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            client_id=self.client_id
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_message(self, topic: str, key: str, value: dict):
        try:
            await self.producer.send_and_wait(topic, key=key.encode(), value=json.dumps(value).encode())
        except Exception as e:
            print(f"Failed to send message to Kafka: {e}")
            raise

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_CLIENT_ID = 'fastapi-producer'

kafka_producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    client_id=KAFKA_CLIENT_ID
)