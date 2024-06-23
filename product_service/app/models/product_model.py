from sqlmodel import SQLModel, Field, Relationship


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    expiry: str | None = None
    brand: str | None = None
    weights: str | None = None
    category: str
    sku: str | None = None
    rating: list["ProductRating"]= Relationship(back_populates="product")


class ProductRating(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    rating: int
    review: str | None = None
    product: Product = Relationship(back_populates="rating")


class Updatedproducts(SQLModel):
    name: str
    description: str
    price: float
    expiry: str | None = None
    brand: str | None = None
    weights: str | None = None
    category: str
    sku: str | None = None