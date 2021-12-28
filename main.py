from flask import Flask, request, redirect, url_for, render_template
import plants

app = Flask(__name__)
db = plants.Plant_Database("plant_data.txt")
garden = []

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        zipcode = request.form['code']
        plant_name = request.form['plant']
        search = request.form['search']
        if plant_name:
            return redirect(url_for('similar',plant=plant_name))
        if zipcode:
            return redirect(url_for('zipcode',code=zipcode))
        if search:
            return redirect(url_for('search',plant=search))
    else:
        return render_template('homepage.html')

@app.route('/allplants', methods=['GET', 'POST'])
def allplants():
    if request.method == 'POST':
        plant_name = request.form['plant_name']
        garden.append(db.plants[plant_name])

    title = 'All Plants'

    return render_template('tables.html', name='All Plants', title=title, plantlist=db.listplants())

@app.route('/similar/<plant>', methods=['GET', 'POST'])
def similar(plant):
    results = db.latin_name_search(plant)
    if results:
        condition = results.pop(0)
        if condition:
            title = f'Here is a table of all plants that have similar needs to {plant}'
            plants = db.get_similar_plants(plant)
        else:
            title = f'There are no plants by that name. Here are some suggestions'
            plants = results
    else:
        title = f"The plant name {plant} does not seem to be in our system. Sorry for the inconvenience."
        return render_template('tables.html', name='Zipcode', title=title)
    if request.method == 'POST':
        plant_name = request.form['plant_name']
        garden.append(db.plants[plant_name])

    return render_template('tables.html', name='Similar Plants', title=title, plantlist=plants)

@app.route('/<code>', methods=['GET', 'POST'])
def zipcode(code):
    try:
        zone = plants.get_hardiness_zone(code)
    except:
        title = f"Your zipcode {code} does not seem to be in our system. Sorry for the inconvenience."
        return render_template('tables.html', name='Zipcode', title=title)
    if request.method == 'POST':
        plant_name = request.form['plant_name']
        garden.append(db.plants[plant_name])
    
    title = f"Your zone is {zone[2]} with a coldest temp of {zone[1]}"
    extra = 'Here is a table of all plants that will thrive in your hardiness zone'

    return render_template('tables.html', name='Zipcode', title=title, plantlist=db.plants_in_zone(zone[0]), extra=extra)

@app.route('/search/<plant>', methods=['GET', 'POST'])
def search(plant):
    results = db.common_name_search(plant)
    if results:
        condition = results.pop(0)
        if condition:
            title = f'Here are your search results'
        else:
            title = f'There are no plants by that name. Here are some suggestions'
    else:
        title = f"The plant name {plant} does not seem to be in our system. Sorry for the inconvenience."
        return render_template('tables.html', name='Zipcode', title=title)
    if request.method == 'POST':
        plant_name = request.form['plant_name']
        garden.append(db.plants[plant_name])
    return render_template('tables.html', name='Search', title=title, plantlist=results)

@app.route('/mygarden', methods=['GET', 'POST'])
def mygarden():
    title = 'This is your garden'
    if request.method == 'POST':
        plant_name = request.form['plant_name']
        garden.remove(db.plants[plant_name])
    gardenlist = []
    for plant in garden:
        gardenlist.append(plant.list_attrs())
    return render_template('garden.html', name='My Garden', title=title, plantlist=gardenlist)