--Instal venv
python -m venv venv

--Activate Virtual Envirnment
.\venv\Scripts\activate

--Install fastapi and uvicorn package
pip install fastapi uvicorn

--Get into This path
(venv) D:\Learning\VSCode\FastAPI\FASTAPI\YTLearning\code

--Run uvicorn server
uvicorn main:app --reload

--URL
http://127.0.0.1:8000