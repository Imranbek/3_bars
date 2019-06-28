import json
import os
from json import JSONDecodeError
from math import sqrt


def main():
    path = 'bard_data.txt'

    bars_data = get_dict_from_file(path)
    if bars_data is None:
        exit('File was not found')
    elif bars_data is False:
        exit('Data in the current file is not a dictionary')

    list_of_bars_data = bars_data['features']
    user_location = get_user_location_data()

    print("\nThe closest bar is: ")
    print_bar_data_from_dict(get_closest_bar(list_of_bars_data,
                                             user_location))
    print("\nThe biggest bar is: ")
    print_bar_data_from_dict(get_biggest_bar_from_list(list_of_bars_data))
    print("\nThe smallest bar is: ")
    print_bar_data_from_dict(get_smallest_bar(list_of_bars_data))


def get_biggest_bar_from_list(list_of_bars_data: list):
    assert list_of_bars_data is not None, \
        'There is no data in file, try another file'
    assert type(list_of_bars_data) is list, \
        'There is no list of bar data in file, try another file'
    the_biggest_bar = max(list_of_bars_data,
                          key=lambda k: k['properties']
                          ['Attributes']['SeatsCount'])

    return the_biggest_bar


def get_smallest_bar(list_of_bars_data: list):
    assert list_of_bars_data is not None, \
        'There is no data in file, try another file'
    assert type(list_of_bars_data) is list, \
        'There is no list of bar data in file, try another file'
    the_smallest_bar = min(list_of_bars_data,
                           key=lambda k: k['properties']
                           ['Attributes']['SeatsCount'])

    return the_smallest_bar


def get_closest_bar(bar_data: list, user_location: list):
    nearest_bar = bar_data[0]
    bar_location = nearest_bar['geometry']['coordinates']
    nearest_bar_distance = get_distance_between_two_points(bar_location,
                                                           user_location)
    for bar in bar_data:
        bar_location = bar['geometry']['coordinates']
        current_bar_distance = get_distance_between_two_points(bar_location,
                                                               user_location)
        if current_bar_distance < nearest_bar_distance:
            nearest_bar = bar
            nearest_bar_distance = current_bar_distance
    return nearest_bar


def get_distance_between_two_points(fist_point_location: list,
                                    second_point_location: list):
    assert len(fist_point_location) == 2 and len(second_point_location) == 2, \
        'Wrong format of location points'
    x_difference = fist_point_location[0] - second_point_location[0]
    y_difference = fist_point_location[1] - second_point_location[1]
    distance = sqrt(x_difference ** 2 + y_difference ** 2)
    return distance


def get_dict_from_file(path):
    file_data = load_file_data(file_path=path)
    if file_data is None:
        return None
    try:
        dict_file_data = json.loads(file_data)
        return dict_file_data
    except JSONDecodeError:
        return False


def get_user_location_data():
    print('Please input your latitude and longitude of your location\n')
    mark_dict = {'Latitude': 0,
                 'Longitude': 0}
    attempts_limit = 15

    for name, mark in mark_dict.items():
        attempts_counter = 0
        while type(mark_dict[name]) is int:
            assert attempts_counter < attempts_limit, \
                'Number of attempts exceeded. Try to restart the script.'
            print('{} (example: 10.1241231) :'.format(name))
            location_param = input()
            try:
                mark_dict[name] = float(location_param)
            except ValueError:
                attempts_counter += 1

    return [mark_dict['Latitude'], mark_dict['Longitude']]


def load_file_data(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as file:
        return file.read()


def print_bar_data_from_dict(bard_data: dict):
    print('\tBar name - {}'.format(bard_data['properties']
                                   ['Attributes']['Name']))
    print('\tBar address - {}'.format(bard_data['properties']
                                      ['Attributes']['Address']))
    print('\tBar phone - {}'.format(bard_data['properties']
                                    ['Attributes']['PublicPhone']
                                    [0]['PublicPhone']))


if __name__ == "__main__":
    main()
