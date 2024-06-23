from app.models.inventory_model import InventoryItem
from sqlmodel import Session, select  
from fastapi import HTTPException 

# Add a New inventory to the Database
def add_new_inventory(inventory_data:InventoryItem, session:Session):
    session.add(inventory_data)
    session.commit()
    session.refresh(inventory_data)
    return inventory_data

# Get All inventory from the DB.
def get_all_inventorys(session:Session):
    all_inventoris = session.exec(select(InventoryItem)).all()
    return all_inventoris

# Get a inventory by ID
def get_inventory_by_id(inventory_id:int, session:Session):
    inventory = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_id)).one_or_none() 
    if inventory is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return inventory

# Delete Product by ID
def delete_inventory_by_id(inventory_id:int, session:Session):
    inventory = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_id)).one_or_none() 
    if inventory is None:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(inventory)
    session.commit()
    return {'message': "Product deleted successfully"}

# Update Product by ID
# def update_product_by_id(product_id: int, to_update_product_data:Updatedproducts, session: Session):
#     # Step 1: Get the Product by ID
#     product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
#     if product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     # Step 2: Update the Product
#     hero_data = to_update_product_data.model_dump(exclude_unset=True)
#     product.sqlmodel_update(hero_data)
#     session.add(product)
#     session.commit()
#     return product
