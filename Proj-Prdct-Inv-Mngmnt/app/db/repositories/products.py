# app/db/repositories/products.py
# from __future__ import annotations
from typing import Any
from app.db.dbConnectionPool import execute
import argparse
from app.utils.logging import setup_logging
def create_product(sku: str, product_name: str, category_id: int, supplier_id: int,
                   unit_price: float, is_active: bool = True) -> dict:
    q = """
        INSERT INTO products (sku, product_name, category_id, supplier_id, unit_price, is_active)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING product_id, sku, product_name, category_id, supplier_id, unit_price, is_active;
    """
    return execute(q, (sku, product_name, category_id, supplier_id, unit_price, is_active),
                   fetch="one", commit=True)

def get_product(product_id: int) -> dict | None:
    q = """
        SELECT p.product_id, p.sku, p.product_name, p.category_id, c.category_name,
               p.supplier_id, s.supplier_name, p.unit_price, p.is_active
        FROM inv_mng.products p
        JOIN inv_mng.categories c ON c.category_id = p.category_id
        JOIN inv_mng.suppliers  s ON s.supplier_id  = p.supplier_id
        WHERE p.product_id = %s;
    """
    return execute(q, (product_id,), fetch="one")

def get_product_by_sku(sku: str) -> dict | None:
    q = "SELECT product_id, sku, product_name, category_id, supplier_id, unit_price, is_active FROM inv_mng.products WHERE sku = %s;"
    return execute(q, (sku,), fetch="one")

def list_products(limit: int = 100, offset: int = 0, active_only: bool = True) -> list[dict]:
    q = """
        SELECT product_id, sku, product_name, category_id, supplier_id, unit_price, is_active
        FROM inv_mng.products
        WHERE (%s = FALSE) OR (is_active = TRUE)
        ORDER BY product_id
        LIMIT %s OFFSET %s;
    """
    return execute(q, (not active_only, limit, offset), fetch="all")

def update_product(product_id: int, **fields) -> dict | None:
    allowed = {"sku", "product_name", "category_id", "supplier_id", "unit_price", "is_active"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return get_product(product_id)
    set_clause = ", ".join([f"{k} = COALESCE(%s, {k})" for k in updates.keys()])
    params = list(updates.values()) + [product_id]
    q = f"""
        UPDATE products
        SET {set_clause}
        WHERE product_id = %s
        RETURNING product_id, sku, product_name, category_id, supplier_id, unit_price, is_active;
    """
    return execute(q, params, fetch="one", commit=True)

def delete_product(product_id: int) -> bool:
    execute("DELETE FROM products WHERE product_id = %s;", (product_id,), commit=True)
    return True


if __name__ == "__main__":
    setup_logging()
    parser = argparse.ArgumentParser(description="Small CLI to call product repository functions")

    parser.add_argument("--operation", "-o", dest="operation",
                        choices=["get_product", "get_product_by_sku", "list_products","delete_product","update_product"],
                        help="Operation to run: get_product, get_product_by_sku, list_products",
                        required=True)
    parser.add_argument("--oparation", "-y", dest="operation", help=argparse.SUPPRESS)
    parser.add_argument("--prd_id", "-i", type=int, dest="prd_id", help="Product id for get_product")
    parser.add_argument("--prd_sku", "-s", type=str, dest="prd_sku", help="SKU for get_product_by_sku")
    parser.add_argument("--limit", "-l", type=int, default=100, help="Limit for list_products")
    parser.add_argument("--offset", "-f", type=int, default=0, help="Offset for list_products")
    parser.add_argument("--all", action="store_true", help="Include inactive products in list_products")

    args = parser.parse_args()

    if args.operation == "get_product":
        if args.prd_id is None:
            parser.error("--prd_id is required for get_product")
        print(get_product(args.prd_id))
    elif args.operation == "get_product_by_sku":
        if not args.prd_sku:
            parser.error("--prd_sku is required for get_product_by_sku")
        print(get_product_by_sku(args.prd_sku))
    elif args.operation == "list_products":
        products = list_products(limit=args.limit, offset=args.offset, active_only=not args.all)
        print(products)
    # elif args.operation == "list_products":
    #     products = list_products(limit=args.limit, offset=args.offset, active_only=not args.all)
    #     print(products)

