import json
import os
from math import radians, cos, sin, asin, sqrt
import argparse


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


def _get_sorted_list_by_seats_count(data, reverse):
    return sorted(data, key=lambda bar: bar['SeatsCount'], reverse=reverse)


def get_biggest_bar(data):
    return _get_sorted_list_by_seats_count(data, False).pop()


def get_smallest_bar(data):
    return _get_sorted_list_by_seats_count(data, True).pop()


def get_closest_bar(data, longitude, latitude):
    return sorted(data, key=lambda bar: haversine(longitude, latitude,
                  float(bar['Longitude_WGS84']), float(bar['Latitude_WGS84']))).pop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the best bar from different criteria.')
    subparsers = parser.add_subparsers(dest='sub_command_name')
    subparsers.add_parser('get_biggest_bar')
    subparsers.add_parser('get_smallest_bar')
    get_closest_bar_ = subparsers.add_parser('get_closest_bar')
    get_closest_bar_.add_argument('lon', type=float, help='longitude')
    get_closest_bar_.add_argument('lat', type=float, help='latitude')
    args = parser.parse_args()
    bars = load_data()
    if args.sub_command_name == 'get_closest_bar':
        print(get_closest_bar(bars, args.lon, args.lat))
    elif args.sub_command_name == 'get_biggest_bar':
        print(get_biggest_bar(bars))
    elif args.sub_command_name == 'get_smallest_bar':
        print(get_smallest_bar(bars))
