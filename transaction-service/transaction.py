import json
import logging
from kafka import KafkaProducer, KafkaConsumer
logging.basicConfig(level=logging.INFO)

ORDER_KAFKA_TOPIC = "order-details"
ORDER_PROCESSED_KAFKA_TOPIC = "order-processed"
BOOT_STRAP_SERVER = "kafka-local.orders-microservice.svc.cluster.local:9092"

# consumer
consumer = KafkaConsumer(
    ORDER_KAFKA_TOPIC,
    bootstrap_servers=BOOT_STRAP_SERVER,
)

# producer
producer = KafkaProducer(bootstrap_servers=BOOT_STRAP_SERVER)

if __name__ == '__main__':
    # This file will consume the topic coming from order-service, process info and produce new topic
    logging.info("Started processing transactions...")
    while True:
        for message in consumer:
            # the message that we'll consume is coming in bytes,
            # so we need to decode it to python string
            consumed_message = json.loads(message.value.decode("utf-8"))

            username = consumed_message.get("username")
            qty = consumed_message.get("quantity")
            price = consumed_message.get("price")
            total_cost = round(float(qty * price), 2)

            data = {
                "username": username,
                "order_id": consumed_message.get("order_id"),
                "email": consumed_message.get("email"),
                "total_cost": total_cost,
            }

            logging.info(f"Successful transactions sent ... {data}")
            producer.send(ORDER_PROCESSED_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
