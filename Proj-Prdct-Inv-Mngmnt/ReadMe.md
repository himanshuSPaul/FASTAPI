


# Project: Proj-Prdct-Inv-Mngmnt

Repository layout (example) — run from project root to preserve package imports:

```
D:.
├── app/
│   ├── api/
│   ├── db/
│   ├── schemas/
│   ├── sql/
│   │   └── schema_and_seed.sql
│   └── utils/
├── config/
├── scripts/
└── tests/
```

## Test Config Parser

Run from the project root:

```powershell
cd 'D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt'
python -m app.utils.config
```

Expected output:

```text
Config File Path : D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt\config\config.ini
ConfigFile Exists : True
Available Sections in Config File : ['app', 'database', 'features']
Application Name: inventory_api
```

## Testing DB modules




Example: call the products repository CLI (module run) from project root:

```powershell
python -m app.db.repositories.products -o get_product_by_sku -s P1001
```

Sample output (includes logging and DB pool initialization):

```text
2025-10-11 20:17:44,235 -:- INFO -:- app.db.repositories.products -:- Logging initialized at INFO, file=D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt\logs\inventory_api_20251011201744.log
2025-10-11 20:17:44,278 -:- INFO -:- app.db.dbConnectionPool -:- DB pool initialized to fastapi@127.0.0.1:5432 (1..10)
RealDictRow({'product_id': 1, 'sku': 'P1001', 'product_name': 'Smartphone X', 'category_id': 1, 'supplier_id': 1, 'unit_price': Decimal('19999.00'), 'is_active': True})
```

Notes:

- Always run modules from the project root using `python -m module.path` so absolute imports like `from app.utils.config import ...` work.
- If you get `ModuleNotFoundError: No module named 'app'`, either run with `-m` from the project root or set `PYTHONPATH` to the project root, or install the project in editable mode (`pip install -e .`).
- Ensure required dependencies are installed (for DB examples install `psycopg2-binary` or other DB drivers):

```powershell
python -m pip install psycopg2-binary
```



(venv) (venv) D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt
> python -m app.db.repositories.products -o get_product_by_sku -s P1001
2025-10-11 20:42:31,846 -:- INFO -:- app.db.repositories.products -:- Logging initialized at INFO, file=D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt\logs\inventory_api_20251011204231.log
2025-10-11 20:42:31,890 -:- INFO -:- app.db.dbConnectionPool -:- DB pool initialized to fastapi@127.0.0.1:5432 (1..10)
RealDictRow({'product_id': 1, 'sku': 'P1001', 'product_name': 'Smartphone X', 'category_id': 1, 'supplier_id': 1, 'unit_price': Decimal('19999.00'), 'is_active': True})

(venv) (venv) D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt
> python -m app.db.repositories.products -o get_product --prd_id 1
2025-10-11 20:42:38,790 -:- INFO -:- app.db.repositories.products -:- Logging initialized at INFO, file=D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt\logs\inventory_api_20251011204238.log   
2025-10-11 20:42:38,839 -:- INFO -:- app.db.dbConnectionPool -:- DB pool initialized to fastapi@127.0.0.1:5432 (1..10)
RealDictRow({'product_id': 1, 'sku': 'P1001', 'product_name': 'Smartphone X', 'category_id': 1, 'category_name': 'Electronics', 'supplier_id': 1, 'supplier_name': 'Acme Supplies', 'unit_price': Decimal('19999.00'), 'is_active': True})   
(venv) (venv) D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt