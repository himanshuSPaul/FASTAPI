from fastapi import FastAPI
from app.db.dbConnectionPool import init_pool, close_pool, ping
from app.api.products import router as products_router
# from app.api.v1.inventory import router as inventory_router
# from app.api.v1.categories import router as categories_router
# from app.api.v1.suppliers import router as suppliers_router
# from app.api.v1.warehouses import router as warehouses_router

app = FastAPI(title="Product Inventory API", version="1.0.0")

@app.on_event("startup")
def _startup():
    init_pool()

@app.on_event("shutdown")
def _shutdown():
    close_pool()

@app.get("/health")
def health():
    return {"status": "ok", "db": ping()}

# Versioned API
app.include_router(products_router)
# app.include_router(inventory_router, prefix="/api/v1")
# app.include_router(categories_router, prefix="/api/v1")
# app.include_router(suppliers_router, prefix="/api/v1")
# app.include_router(warehouses_router, prefix="/api/v1")
