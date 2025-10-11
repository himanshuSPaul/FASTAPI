from fastapi import APIRouter, HTTPException, Query
from app.schemas.products import ProductCreate, ProductUpdate, ProductOut
from app.db.repositories import products as prd

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=list[ProductOut])
def list_products(limit: int = Query(100, ge=1, le=500),
                  offset: int = Query(0, ge=0),
                  active_only: bool = True):
    return prd.list_products(limit=limit, offset=offset, active_only=active_only)

@router.post("", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate):
    return prd.create_product(**payload.model_dict())

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int):
    row = prd.get_product(product_id)
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return row

@router.patch("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate):
    row = prd.update_product(product_id, **payload.model_dump(exclude_unset=True))
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return row

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int):
    # delete returns True even if row didn't exist; enforce 404 by probing first
    if not prd.get_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    prd.delete_product(product_id)
    return None
