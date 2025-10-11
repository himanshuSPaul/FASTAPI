from pydantic import BaseModel, Field, condecimal, constr


class ProductCreate(BaseModel):
    sku: str | None = None
    product_name: str
    category_id: int 
    supplier_id: int
    unit_price: float
    is_active: bool = True

class ProductUpdate(BaseModel):
    sku: str | None = None
    product_name: str | None = None
    category_id: int | None = None
    supplier_id: int | None = None
    unit_price: str | None = None
    is_active: bool | None = None

class ProductOut(BaseModel):
    product_id: int
    sku: str
    product_name: str
    category_id: int
    supplier_id: int
    unit_price: float
    is_active: bool
