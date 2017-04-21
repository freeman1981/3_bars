import json
import os
import sys
from math import radians, cos, sin, asin, sqrt


BARS = 'bars.json'


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    earth_radius = 6371
    return c * earth_radius


def load_data(file_path=BARS):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', errors='ignore') as file_handler:
        try:
            return json.load(file_handler)
        except json.decoder.JSONDecodeError:
            return None


def get_biggest_bar(data):
    return sorted(data, key=lambda bar: bar['SeatsCount']).pop()


def get_smallest_bar(data):
    return sorted(data, key=lambda bar: bar['SeatsCount'], reverse=True).pop()


def get_closest_bar(data, longitude, latitude):
    return sorted(data, key=lambda bar: haversine(longitude, latitude,
                  float(bar['Longitude_WGS84']), float(bar['Latitude_WGS84']))).pop()


if __name__ == '__main__':
    try:
        command = sys.argv[1]
    except IndexError:
        print('usage: python3 bars.py [get_biggest_bar|get_smallest_bar|get_closest_bar X Y')
    else:
        bars = load_data()
        if command == 'get_biggest_bar':
            print(get_biggest_bar(bars))
        elif command == 'get_smallest_bar':
            print(get_smallest_bar(bars))
        elif command == 'get_closest_bar':
            try:
                x_coordinate, y_coordinate = float(sys.argv[2]), float(sys.argv[3])
            except (IndexError, ValueError):
                print('usage: python3 bars.py [get_biggest_bar|get_smallest_bar|get_closest_bar X Y')
            else:
                print(get_closest_bar(bars, x_coordinate, y_coordinate))
        else:
            print('usage: python3 bars.py [get_biggest_bar|get_smallest_bar|get_closest_bar X Y')
