


PS D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt> tree /f
Folder PATH listing for volume New Volume
Volume serial number is E221-A9E7
D:.
│   ReadMe.md
│   
├───app
│   ├───api
│   ├───db
│   ├───schemas
│   ├───sql
│   │       schema_and_seed.sql
│   │
│   └───utils
├───config
├───scripts
└───tests



# Test Config Parser
```
cd D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt  
python app/utils/config.py
```

Expected Output 
```
Config File Path : D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt\config\config.ini      
ConfigFile Exists : True
Avaialbel Section in Config File : ['app', 'database', 'features']
application_name: inventory_api
```

or 
```
python -m app.utils.config
```
Expected Output 
```
(venv) (venv) D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt
> python -m app.utils.config
Config File Path : D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt\config\config.ini
ConfigFile Exists : True
Avaialbel Section in Config File : ['app', 'database', 'features']
Application Name: inventory_api
(venv) (venv) D:\Learning\VSCode\FastAPI\FASTAPI\Proj-Prdct-Inv-Mngmnt