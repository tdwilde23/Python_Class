import requests
from bs4 import BeautifulSoup

class Plant():

    def __init__(self,latin_name, common_name = None, habit = None, height = None, hardiness = None, growth = None, soil = None, shade = None, moisture = None, edible = None):
        self.latin_name = latin_name
        self.common_name = common_name
        self.habit = habit
        self.height = height
        self.hardiness = hardiness
        # S = slow M = medium F = fast
        self.growth = growth
        # L = light (sandy) M = medium H = heavy (clay)
        self.soil = soil
        # F = full shade S = semi-shade N = no shade
        self.shade = shade
        # D = dry M = Moist We = wet Wa = water
        self.moisture = moisture
        self.edible = edible

    def __repr__(self):
        return f'Latin Name: {self.latin_name}\n\
Common Name(s): {self.common_name}\n\
Habit: {self.habit}\n\
Height: {self.height}\n\
Hardiness: {self.hardiness}\n\
Growth: {self.growth}\n\
Soil: {self.soil}\n\
Sun: {self.shade}\n\
Moisture: {self.moisture}\n\
Edible: {self.edible}\n'

    def __eq__(self, other):
        if self.soil == other.soil and self.shade == other.shade and self.moisture == other.moisture:
            return True
        else:
            return False
    
    def hardiness_value(self):
        if self.hardiness == '-':
            return False
        else:
            zones = self.hardiness.split('-')
            lower_zone = int(zones[0])
            upper_zone = int(zones[1])
            return [lower_zone, upper_zone]
    
    def list_attrs(self):
        return [self.latin_name, self.common_name, self.habit, self.height, self.hardiness, self.growth, self.soil, self.shade, self.moisture, self.edible]



class Plant_Database():

    def __init__(self, file):
        self.plants = {}
        with open(file, 'r') as text:
            for plant in text:
                plant_list = plant.split('|')
                plant_name = ''
                for key_value in plant_list:
                    split_key_values = key_value.split(':')
                    key = split_key_values[0]
                    value = split_key_values[1]
                    if key == 'Latin Name':
                        plant_name = value
                        self.plants[plant_name] = Plant(plant_name)
                    elif key == 'Common Name':
                        if value == "['']":
                            value = "None"
                        else:
                            list_of_names = value.strip("[]").split(',')
                            if len(list_of_names) == 1:
                                value = list_of_names[0].strip("'").strip('"')
                            else:
                                value = []
                                for name in list_of_names:
                                    value.append(name.strip().strip('"').strip("'"))
                    elif key == 'Medicinal' or key == 'Other':
                        continue
                    setattr(self.plants[plant_name], key.lower().replace(' ', '_'), value)

    def __repr__(self):
        return str(self.plants.values())
    
    def get_similar_plants(self, search_plant):
        similar_plants = []
        search_plant = self.plants[search_plant]
        for plant in self.plants.values():
            if search_plant.latin_name == plant.latin_name:
                continue
            if plant == search_plant:
                similar_plants.append(plant.list_attrs())
        if similar_plants == []:
            return False
        return similar_plants

    def input_new_plant(self, name, attribute, value):
        self.plant[name] = Plant(name)
        setattr(self.plant[name],attribute.lower().replace(' ', '_'),value)

    def delete_plant(self, name):
        if name in self.plants.keys():
            return self.plants.pop(name)
        else:
            return 'This plant is not in the database'

    def headers(self):
        return ['Latin Name', 'Common Name(s)','Habit','Height','Hardiness','Growth','Soil','Sun','Moisture','Edible']

    def listplants(self):
        plantlist = []
        for plant in self.plants.values():
            plantattrs = []
            for values in plant.list_attrs():
                plantattrs.append(values)
            plantlist.append(plantattrs)
        return plantlist

    def plants_in_zone(self,zone):
        plant_list = []
        zone = zone
        for plant in self.plants.values():
            zone_range = plant.hardiness_value()
            if zone_range:
                if zone_range[0] <= zone and zone_range[1] >= zone:
                    plant_list.append(plant.list_attrs())
        return plant_list

    def latin_name_search(self,name):
        suggestions = []
        results = []
        for plant in self.plants.values():
            if name.lower() == plant.latin_name.lower():
                results.append(plant.list_attrs())
            else:
                if name.lower() in plant.latin_name.lower():
                    suggestions.append(plant.list_attrs())
        if results == [] and suggestions == []:
            return False
        elif results == []:
            suggestions.insert(0,False)
            return suggestions
        else:
            results.insert(0,True)
            return results

    def common_name_search(self,name):
        suggestions = []
        results = []
        for plant in self.plants.values(): 
            plant_names = plant.common_name
            if type(plant_names) == list:
                for com_name in plant_names:
                    if name.lower() == com_name.lower():
                        results.append(plant.list_attrs())
                    if name.lower() in com_name.lower():
                        suggestions.append(plant.list_attrs())
            elif plant.common_name == 'None':
                continue
            else:
                if name.lower() == plant_names.lower():
                    results.append(plant.list_attrs())
                if name.lower() in plant_names.lower():
                        suggestions.append(plant.list_attrs())
        if results == [] and suggestions == []:
            return False
        elif results == []:
            suggestions.insert(0,False)
            return suggestions
        else:
            results.insert(0,True)
            return results

class Garden():
    def __init__(self,name):
        self.name = name
        self.garden_plants = []
    
    def add_plant(self, plant):
        self.garden_plants.append(plant_db.plants[plant])


def get_hardiness_zone(zipcode):
    url = f'https://www.plantmaps.com/{zipcode}'
    print(url)
    html = requests.get(url, headers = {'User-Agent':'Test'})
    soup = BeautifulSoup(html.content, "html.parser")
    table_header = soup.thead.td.next_sibling.next_element
    zone_data = []
    for count, text in enumerate(table_header):
        #skips an empty value returned from the website
        if count == 1:
            continue
        zone_data.append(text)
    zone_number = zone_data[0].split()
    number_letter = zone_number[1]
    zone_data.append(number_letter)
    zone_data[0] = int(number_letter[0])
    return zone_data