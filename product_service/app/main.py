# main.py
from contextlib import asynccontextmanager
from typing import Annotated
from app import settings
from sqlmodel import Session, SQLModel, select
from fastapi import FastAPI, Depends, HTTPException
from typing import AsyncGenerator
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json


from app.consumer.inventory_cosumer import consume_inventory_message
from app.consumer.product_cosumer import consume_message
from app.db import engine
from app.models.product_model import Product, Updatedproducts
from app.crud.product_crud import add_new_product, get_all_products, get_product_by_id, delete_product_by_id, update_product_by_id
from app.dep import get_kafka_producer, get_session




def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables.")
    task = asyncio.create_task(consume_message(settings.KAFKA_PRODUCT_TOPIC, 'broker:19092'))
    asyncio.create_task(consume_inventory_message(
        "Addstock",
        'broker:19092'
    ))
    create_db_and_tables()
    yield



app = FastAPI(lifespan=lifespan, title="Hello World API with DB", 
    version="0.0.1")



@app.get("/")
def read_root():
    return {"Hello": "PanaCloud"}

# Kafka Producer as a dependency

@app.post("/manage-prod/", response_model=Product)
#   """Create a new product and send it to Kafka"""
async def new_product (product: Product, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]) -> Product: 
    # session.add(product)    
    # session.commit()
    # session.refresh(product)
    # return product
    product_dict = {field: getattr(product, field) for field in product.dict()}
    product_json = json.dumps(product_dict).encode("utf-8")
    print("product_JSON:", product_json)
    # Produce message
    await producer.send_and_wait(settings.KAFKA_PRODUCT_TOPIC, product_json)
    # _product = add_new_product(product, session)
    return product

@app.get("/products/", response_model=list[Product])
def get_prod(session: Annotated[Session, Depends(get_session)]):
    """Get all products"""
    return get_all_products(session)


@app.get("/products/{product_id}", response_model=Product)
def get_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    """Get a single product by ID"""
    try:
        return get_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    """delete a single product by ID"""
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return  {"message": "Product deleted successfully"}

# update product by ID
@app.patch("/manage-products/{product_id}", response_model=Product)
def update_single_product(product_id: int, product: Updatedproducts, session: Annotated[Session, Depends(get_session)]):
    """ Update a single product by ID"""
    try:
        return update_product_by_id(product_id=product_id, to_update_product_data=product, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
