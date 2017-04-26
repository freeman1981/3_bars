import json
import os
import sys
import argparse
from math import sqrt


def distance_between_points(longitude1, latitude1, longitude2, latitude2):
    """We are using euclidean distance
    https://en.wikipedia.org/wiki/Euclidean_distance
    """
    return sqrt((longitude1 - longitude2) ** 2 + (latitude1 - latitude2) ** 2)


def load_data(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='cp1251') as file_handler:
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
    return sorted(data, key=lambda bar: distance_between_points(
        longitude, latitude,
        float(bar['Longitude_WGS84']), float(bar['Latitude_WGS84']))).pop()


def get_args():
    """Prepare parser and parse args from command line"""
    parser = argparse.ArgumentParser(description='Find the best bar from different criteria.')
    parser.add_argument('path', type=str, help='path to json bars')
    parser.add_argument('lon', type=float, help='longitude')
    parser.add_argument('lat', type=float, help='latitude')
    return parser.parse_args()


def _get_name_and_address_from_json_bar_object(bar_json_object):
    return bar_json_object['Name'], bar_json_object['Address']


def print_json_bar_with_prefix_message(message, bar_json_object):
    bar_name, bar_address = _get_name_and_address_from_json_bar_object(bar_json_object)
    print('{message}: {bar_name}, адресс: {bar_address}'.format(
        message=message, bar_name=bar_name, bar_address=bar_address
    ))


if __name__ == '__main__':
    args = get_args()
    bars = load_data(args.path)
    if bars is None:
        print('path {} does not exists or not json'.format(args.path))
        sys.exit(1)
    try:
        print_json_bar_with_prefix_message('Самый близкий бар', get_closest_bar(bars, args.lon, args.lat))
        print_json_bar_with_prefix_message('Самый большой бар', get_biggest_bar(bars))
        print_json_bar_with_prefix_message('Самый маленький бар', get_smallest_bar(bars))
    except KeyError:
        print('script receive unexpected json')
        sys.exit(1)
