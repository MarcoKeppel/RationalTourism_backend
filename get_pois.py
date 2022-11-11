import requests
import json


all_types = [
    'bars cafes bistros' , # -> Bars/Cafés/Bistros
    'restaurants' , # -> Restaurants
    'restaurants gasthäuser' , # -> Restaurants & Taverns
    'e-bike ladestation' , # -> E-bike charging station
    'kirchen' , # -> Churches
    'klöster' , # -> Monasteries
    'burgen schlösser' , # -> Forts & Castles
    'architektur' , # -> Architecture
    'essen trinken' , # -> Wineries
    'e-tankstellen ladestationen' , # -> Electric charging stations
    'kirchen klöster' , # -> Churches & Monasteries
]

restaurant_types = [
    'bars cafes bistros' , # -> Bars/Cafés/Bistros
    'restaurants' , # -> Restaurants
    'restaurants gasthäuser' , # -> Restaurants & Taverns
    'essen trinken' , # -> Wineries
]

electric_station_tyes = [
    'e-tankstellen ladestationen' , # -> Electric charging stations
    'e-bike ladestation' , # -> E-bike charging stations
]

castles_monasteries_types = [
    'kirchen' , # -> Churches
    'klöster' , # -> Monasteries
    'burgen schlösser' , # -> Forts & Castles
    'architektur' , # -> Architecture
    'kirchen klöster' , # -> Churches & Monasterie
]

def get_pois(types, latitudine = None, longitude = None, radius = None):
    params = {
        'pagenumber' : 1,
        'pagesize' : 100,
        'langfilter' : 'en',
        'removenullvalues' : True,
        'latitude' : latitudine, 
        'longitude' : longitude, 
        'radius' : radius, 

    }

    url = 'https://tourism.opendatahub.bz.it/v1/ODHActivityPoi'
    results = {}
    for typ in types:
        params['type'] = typ
        data = requests.get(url, params=params).text
        data_json = json.loads(data)
        print(typ,data_json['TotalResults'])
        items = data_json['Items']
        result = {}
        language = 'en' # Assume all the titles are the same for every language
        for item in items:
            try: 
                details = item['Detail']
                title = details[language]['Title']
                gps_info = item['GpsInfo'][0]
                altitude = gps_info['Altitude']
                latitude = gps_info['Latitude']
                longitude = gps_info['Longitude']
                location_info = item['LocationInfo']['TvInfo']['Name'][language]
                #category = ','.join([x['Shortname'] for x in item['CategoryCodes']]).encode("ascii", "ignore").decode()

                
                results[title] = {
                    'altitude' : altitude,
                    'latitude' : latitude,
                    'longitude' : longitude,
                    'location_name' : location_info,
                    'type' : typ
                }
            except Exception as e:
                print("Key error: " + str(e))

        # Interesting files we are not considering because this is an hackathon
        # ImageGallery
    return results

# Example
# get_pois(all_types)
# get_pois(restaurant_types)
# get_pois(electric_station_tyes)
# get_pois(castles_monasteries_types)
print(get_pois(all_types, latitudine = 46.673175, longitude = 10.569963, radius = 100))

