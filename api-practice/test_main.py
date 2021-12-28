from fastapi.testclient import TestClient
from main import app, Cat
from database import DataBase

client = TestClient(app)

test_data = {'kona': {'name':'Kona','breed':'Bengal'}, \
    'cloud': {'name':'Cloud','breed':'Balinese'}, \
    'noodle': {'name':'Noodle','breed':'American Shorthair'}}

db = DataBase()
db.put('Kona', {'name':'Kona','breed':'Bengal'})
db.put('Cloud', {'name':'Cloud','breed':'Balinese'})
db.put('Noodle', {'name':'Noodle','breed':'American Shorthair'})
app.db = db



#def test_hello():
#    response = client.get('/')
#
#    assert response.status_code == 200
#    assert response.json() == {'hello':'world!'}

def test_get_cats():
    response = client.get('/cats')

    assert response.status_code == 200
    assert response.json() == test_data


def test_get_one_cat():
    response = client.get('/cats/cloud')

    assert response.status_code == 200
    assert response.json() == {'name':'Cloud','breed':'Balinese'}

def test_post_cat():

    response = client.post('/cats', json={'name':'Beau','breed':'Maine Coon'})

    assert response.status_code == 200
    assert response.json() == {'name':'Beau','breed':'Maine Coon'}

def test_delete_cat():

    response = client.delete('/cats/kona')

    assert response.status_code == 200
    assert response.json() == {'beau': {'breed': 'Maine Coon', 'name': 'Beau'}, 'cloud': {'name':'Cloud','breed':'Balinese'}, \
        'noodle': {'name':'Noodle','breed':'American Shorthair'}}
