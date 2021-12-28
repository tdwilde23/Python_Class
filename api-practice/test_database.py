from database import DataBase

def test_get():
    #GIVEN
    db = DataBase()
    db._data = {'example_key':'example_value'}

    #WHEN
    result = db.get('example_key')

    #THEN
    assert result == 'example_value'

def test_put():
    #GIVEN
    db = DataBase()

    #WHEN
    db.put('some_key', 'some_value')

    #THEN
    assert db._data['some_key'] == 'some_value'

def test_all():
    #GIVEN
    db = DataBase()
    dictionary_of_data = {'example_key':'example_value', 'some_key': 'some_value'}
    db._data = dictionary_of_data

    #WHEN
    result = db.all()

    #THEN
    assert result == dictionary_of_data