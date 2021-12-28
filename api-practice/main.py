from fastapi import FastAPI
from database import DataBase
from pydantic import BaseModel

app = FastAPI()
app.db = DataBase()

class Cat(BaseModel):
    name: str
    breed: str

#@app.get('/')
#def hello():
#    return {'hello' : 'world!'}

@app.get('/cats')
def get_cats():
    return app.db.all()

@app.get('/cats/{cat_name}')
def get_cat(cat_name: str):
    return app.db.get(cat_name.lower())

@app.post('/cats')
def create_cat(cat: Cat):
    app.db.put(cat.name.lower(), cat.dict())
    return app.db.get(cat.name.lower())

@app.delete('/cats/{cat_name}')
def delete_cat(cat_name: str):
    deleted = app.db.delete(cat_name.lower())
    return deleted