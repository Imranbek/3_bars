import json
import os
import sys
from json import JSONDecodeError
from math import sqrt


def main():
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        exit('Try again with right format "$ python bars.py <path to file>"')

    bars = get_list_from_file(path)
    if bars is None:
        exit('File was not found')
    elif bars is False:
        exit('Data in the current file is not a dictionary')

    bars = bars['features']
    assert bars is not None, \
        'There is no data in file, try another file'
    assert type(bars) is list, \
        'There is no list of bar data in file, try another file'
    user_location = get_user_location()

    for point in user_location:
        assert point is not None, 'Wrong format of location parameter. Please try again.'

    print('\nThe closest bar is: ')
    print_bar_info(get_closest_bar(bars, user_location))
    print('\nThe biggest bar is: ')
    print_bar_info(get_biggest_bar_from_list(bars))
    print('\nThe smallest bar is: ')
    print_bar_info(get_smallest_bar(bars))


def get_biggest_bar_from_list(bars: list):
    the_biggest_bar = max(bars,
                          key=lambda k: k['properties']
                          ['Attributes']['SeatsCount'])

    return the_biggest_bar


def get_smallest_bar(bars: list):
    the_smallest_bar = min(bars,
                           key=lambda k: k['properties']
                           ['Attributes']['SeatsCount'])

    return the_smallest_bar


def get_closest_bar(bars: list, user_location: list):
    nearest_bar = min(bars,
                      key=lambda b:
                      get_distance_between_points(b['geometry']['coordinates'],
                                                  user_location))

    return nearest_bar


def get_distance_between_points(first_point: list,
                                second_point: list):
    assert len(first_point) == 2 and \
           len(second_point) == 2, 'Wrong format of location points'
    x_difference = first_point[0] - second_point[0]
    y_difference = first_point[1] - second_point[1]
    distance = sqrt(x_difference ** 2 + y_difference ** 2)
    return distance


def get_list_from_file(path):
    file_data = load_file_data(file_path=path)
    if file_data is None:
        return None
    try:
        json_file_data = json.loads(file_data)
        return json_file_data
    except JSONDecodeError:
        return False


def get_user_location():
    print('Please input your latitude and longitude of your location.\n'
          'Use only digits and dot as separator.')
    coordinates = {'latitude': 0,
                   'longitude': 0}

    for name, mark in coordinates.items():
        print('{} (example: 10.1241231) :'.format(name))
        location_param = input()
        try:
            coordinates[name] = float(location_param)
        except ValueError:
            coordinates[name] = None
            exit('Wrong format of location parameter. Please try again.')

    return [coordinates['latitude'], coordinates['longitude']]


def load_file_data(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as file:
        return file.read()


def print_bar_info(bar: dict):
    print('\tBar name - {}'.format(bar['properties']
                                   ['Attributes']['Name']))
    print('\tBar address - {}'.format(bar['properties']
                                      ['Attributes']['Address']))
    print('\tBar phone - {}'.format(bar['properties']
                                    ['Attributes']['PublicPhone']
                                    [0]['PublicPhone']))


if __name__ == '__main__':
    main()
