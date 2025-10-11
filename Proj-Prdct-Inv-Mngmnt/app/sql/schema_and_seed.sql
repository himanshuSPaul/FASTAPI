-- =========================
-- Product Inventory Schema
-- =========================
-- Target: PostgreSQL 12+

-- Drop existing (for idempotent dev runs)
DROP TABLE IF EXISTS inv_mng.sales_order_items CASCADE;
DROP TABLE IF EXISTS inv_mng.sales_orders CASCADE;
DROP TABLE IF EXISTS inv_mng.purchase_order_items CASCADE;
DROP TABLE IF EXISTS inv_mng.purchase_orders CASCADE;
DROP TABLE IF EXISTS inv_mng.inventory CASCADE;
DROP TABLE IF EXISTS inv_mng.products CASCADE;
DROP TABLE IF EXISTS inv_mng.categories CASCADE;
DROP TABLE IF EXISTS inv_mng.suppliers CASCADE;
DROP TABLE IF EXISTS inv_mng.warehouses CASCADE;




-- ==============
-- Master tables
-- ==============

CREATE TABLE inv_mng.categories (
    category_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE inv_mng.suppliers (
    supplier_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_name TEXT NOT NULL UNIQUE,
    contact_email TEXT,
    contact_phone TEXT
);

CREATE TABLE inv_mng.products (
    product_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    product_name TEXT NOT NULL,
    category_id BIGINT NOT NULL REFERENCES inv_mng.categories(category_id) ON DELETE RESTRICT,
    supplier_id BIGINT NOT NULL REFERENCES inv_mng.suppliers(supplier_id) ON DELETE RESTRICT,
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE INDEX idx_products_name ON inv_mng.products (product_name);

CREATE TABLE inv_mng.warehouses (
    warehouse_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    warehouse_name TEXT NOT NULL,
    city TEXT
);

-- ==================
-- Inventory (stock)
-- ==================
CREATE TABLE inv_mng.inventory (
    product_id BIGINT NOT NULL REFERENCES inv_mng.products(product_id) ON DELETE CASCADE,
    warehouse_id BIGINT NOT NULL REFERENCES inv_mng.warehouses(warehouse_id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    PRIMARY KEY (product_id, warehouse_id)
);

-- ======================
-- (Optional) PO & SO
-- Keeping placeholders for future expansion
-- ======================
CREATE TABLE inv_mng.purchase_orders (
    po_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_id BIGINT NOT NULL REFERENCES inv_mng.suppliers(supplier_id),
    po_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status TEXT NOT NULL DEFAULT 'CREATED'  -- CREATED | RECEIVED | CANCELLED
);

CREATE TABLE inv_mng.purchase_order_items (
    po_item_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    po_id BIGINT NOT NULL REFERENCES inv_mng.purchase_orders(po_id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES inv_mng.products(product_id),
    ordered_qty INTEGER NOT NULL CHECK (ordered_qty > 0),
    unit_cost NUMERIC(10,2) NOT NULL CHECK (unit_cost >= 0)
);

CREATE TABLE inv_mng.sales_orders (
    so_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_name TEXT NOT NULL,
    so_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status TEXT NOT NULL DEFAULT 'CREATED'  -- CREATED | FULFILLED | CANCELLED
);

CREATE TABLE inv_mng.sales_order_items (
    so_item_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    so_id BIGINT NOT NULL REFERENCES inv_mng.sales_orders(so_id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES inv_mng.products(product_id),
    ordered_qty INTEGER NOT NULL CHECK (ordered_qty > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0)
);





-- =================
-- Seed sample data(More to be inserted via api
-- =================




INSERT INTO inv_mng.categories (category_name, description) VALUES
('Electronics', 'Phones, laptops, gadgets'),
('Groceries',   'Everyday grocery items'),
('Clothing',    'Apparel and accessories');

INSERT INTO inv_mng.suppliers (supplier_name, contact_email, contact_phone) VALUES
('Acme Supplies',   'sales@acme.example',      '+91-90000-00001'),
('FreshFoods Co.',  'hello@freshfoods.example','+91-90000-00002'),
('FashionHub Ltd.', 'contact@fashionhub.example', '+91-90000-00003');

INSERT INTO inv_mng.products (sku, product_name, category_id, supplier_id, unit_price, is_active) VALUES
('P1001', 'Smartphone X',     (SELECT category_id FROM inv_mng.categories WHERE category_name='Electronics'),
                               (SELECT supplier_id  FROM inv_mng.suppliers  WHERE supplier_name='Acme Supplies'),
                               19999.00, TRUE),
('P2001', 'Basmati Rice 5kg', (SELECT category_id FROM inv_mng.categories WHERE category_name='Groceries'),
                               (SELECT supplier_id  FROM inv_mng.suppliers  WHERE supplier_name='FreshFoods Co.'),
                               549.00, TRUE),
('P3001', 'Classic T-Shirt',  (SELECT category_id FROM inv_mng.categories WHERE category_name='Clothing'),
                               (SELECT supplier_id  FROM inv_mng.suppliers  WHERE supplier_name='FashionHub Ltd.'),
                               499.00, TRUE),
('P1002', 'Laptop Air 13"',   (SELECT category_id FROM inv_mng.categories WHERE category_name='Electronics'),
                               (SELECT supplier_id  FROM inv_mng.suppliers  WHERE supplier_name='Acme Supplies'),
                               72999.00, TRUE);

INSERT INTO inv_mng.warehouses (code, warehouse_name, city) VALUES
('WH-MUM', 'Mumbai Central DC', 'Mumbai'),
('WH-DEL', 'Delhi North DC',    'Delhi');

-- Stock
INSERT INTO inv_mng.inventory (product_id, warehouse_id, quantity)
SELECT p.product_id, w.warehouse_id, q.qty
FROM (VALUES
    ('P1001','WH-MUM',50),
    ('P1001','WH-DEL',30),
    ('P2001','WH-MUM',200),
    ('P3001','WH-DEL',120),
    ('P1002','WH-MUM',15)
) AS q(sku, wcode, qty)
JOIN inv_mng.products   p ON p.sku = q.sku
JOIN inv_mng.warehouses w ON w.code = q.wcode;

-- Some example orders (optional)
INSERT INTO inv_mng.purchase_orders (supplier_id, status) VALUES
((SELECT supplier_id FROM inv_mng.suppliers WHERE supplier_name='Acme Supplies'), 'CREATED');

INSERT INTO inv_mng.purchase_order_items (po_id, product_id, ordered_qty, unit_cost)
VALUES (
    (SELECT po_id FROM inv_mng.purchase_orders LIMIT 1),
    (SELECT product_id FROM inv_mng.products WHERE sku='P1001'),
    40, 18000.00
);

INSERT INTO inv_mng.sales_orders (customer_name, status) VALUES
('Rahul Sharma','CREATED');

INSERT INTO inv_mng.sales_order_items (so_id, product_id, ordered_qty, unit_price)
VALUES (
    (SELECT so_id FROM inv_mng.sales_orders LIMIT 1),
    (SELECT product_id FROM inv_mng.products WHERE sku='P3001'),
    2, 499.00
);