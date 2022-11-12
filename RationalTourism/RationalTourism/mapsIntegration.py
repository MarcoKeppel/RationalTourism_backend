import requests
from django.conf import settings
import json


def get_travel_directions(origin_latitude, origin_longitude, destination_latitude, destination_longitude,
                          transit_mode='driving'):
    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        'origin': f'{origin_latitude},{origin_longitude}',
        'destination': f'{destination_latitude},{destination_longitude}',
        'key': 'AIzaSyDf_ePj68dLqkQQo5ZvWiSOvOxB3OrPKGE',
        'mode': transit_mode
    }

    response_json = json.loads(requests.get(url, params=params).text)
    response_json = response_json['routes'][0]['legs'][0]

    distance_text = response_json['distance']['text']
    duration_text = response_json['duration']['text']
    if transit_mode == 'driving':
        energy_spent = (response_json['distance'][
                            'value'] / 1.609344) * 0.24  # Tesla Model 3, with 24 kWh/100 mi (or 0.24kWh per mile), https://ecocostsavings.com/average-electric-car-kwh-per-mile/
    else:
        energy_spent = (((response_json['distance'][
            'value']) * 0.03) * 8.5) / 20  # 30 liters per 100 km, 8,5 kWh per liter, 20 persons on a bus
    energy_spent = round(energy_spent, 2)  # + " kWh"
    return {'distance': distance_text, 'duration': duration_text, 'energy': energy_spent}


if __name__ == '__main__':
    # transit
    print(get_travel_directions(46.1408235, 11.0922949, 46.0720192345279, 11.119535018566223, 'transit'))

    # driving
    print(get_travel_directions(46.1408235, 11.0922949, 46.0720192345279, 11.119535018566223, 'driving'))
