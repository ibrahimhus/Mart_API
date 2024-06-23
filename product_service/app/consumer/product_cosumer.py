# main.py
from aiokafka import AIOKafkaConsumer
import json
from app.models.product_model import Product
from app.crud.product_crud import add_new_product
from app.dep import get_session






async def consume_message(topic, bootstrap_servers):
# create a consumer instance
    consumer = AIOKafkaConsumer(
        topic, 
        bootstrap_servers= bootstrap_servers,
        group_id = "my-product-consumer-group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message: {
                  message.value.decode()} on topic {message.topic}") 
            prod_data = json.loads(message.value.decode())
            print("Type", type(prod_data))
            print(f"prod_data {prod_data}") 

            with next(get_session()) as session:
                db_product = add_new_product(product_data=Product(**prod_data), session=session)
                print("db_product", db_product)

    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
