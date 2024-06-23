from sqlmodel import SQLModel, Field

# Inventory Model
class InventoryItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int
    variant_id: int | None = None
    quantity: int
    status: str

# class InventoryItemUpdate(SQLModel):
#     name: str
#     description: str
#     price: float
#     expiry: str | None = None
#     brand: str | None = None
#     weights: str | None = None
#     category: str
#     sku: str | None = None