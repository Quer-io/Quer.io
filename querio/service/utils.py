import numpy as np


def get_frequency_count(data, values):
    '''Returns frequency count for user defined columns in the database

    :param data: (Pandas) DataFrame
        data from database
    :param values: list of Strings
        Columns that users wants frequency to be counted
    :return:
        list containing dictionaries for each value
    '''
    result_list = []
    for value in values:
        list_item = data['%s' % value].values.tolist()
        item_type = type(list_item[0])
        if item_type is int or item_type is float:
            result_list.append(get_frequency_count_int(data, value))
        elif item_type is str:
            result_list.append(get_frequency_count_str(data, value))
    return result_list


def get_frequency_count_int(data, value):
    '''Counts frequency columns containing int or float numbers

    :param data: (Pandas) DataFrame
        data from database
    :param value: String
        name of the column
    :return:
        dictionary named by the value name and containing all frequencies
        for rows as int values
    '''
    frequency_values_dict = {}
    feature_list = data['%s' % value].values.tolist()
    y = np.bincount(np.array(feature_list, dtype=int))
    ii = np.nonzero(y)[0]
    tmp_dict = {}
    for val in ii:
        tmp_dict[val] = y[val]
    frequency_values_dict["{} frequencies".format(value)] = tmp_dict
    return frequency_values_dict


def get_frequency_count_str(data, value):
    '''Counts frequency for columns containing strings

    :param data: (Pandas) DataFrame
        data from database
    :param value: String
        name of the column
    :return:
        dictionary named by the value name and containing all frequencies
        for rows as int values
    '''
    frequency_values_dict = {}
    tmp_dict = {}
    tmp_set_of_str = {""}
    feature_list = data['%s' % value].values.tolist()
    for feature in feature_list:
        if feature not in tmp_set_of_str:
            tmp_dict[feature] = 1
            tmp_set_of_str.add(feature)
        else:
            tmp_dict[feature] = tmp_dict.get(feature) + 1
    frequency_values_dict["{} frequencies".format(value)] = tmp_dict
    return frequency_values_dict

