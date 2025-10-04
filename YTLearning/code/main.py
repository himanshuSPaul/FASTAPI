from fastapi import FastAPI

app = FastAPI()


"""Define a root ("/") endpoint """
@app.get("/")
def root_path():
    return "This is The root path  of APi"