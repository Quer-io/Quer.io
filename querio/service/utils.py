import numpy as np


def get_frequency_count(data, values):
    """Returns frequency count for user defined columns in the database

     :param data: (Pandas) DataFrame
        data from database
    :param values: list of strings
        columns that users wants frequency to be counted from
    :return:
        list containing dictionaries for values
    """
    result_list = []
    for value in values:
        values_list = data['%s' % value].values.tolist()
        item_type = type(values_list[0])
        if item_type is int or item_type is float:
            result_list.append(get_frequency_count_int(values_list, value))
        elif item_type is str:
            result_list.append(get_frequency_count_str(values_list, value))
        elif item_type is bool:
            result_list.append(get_frequency_count_bool(values_list, value))
    return result_list


def get_frequency_count_int(values_list, value):
    """Counts frequency columns containing int or float numbers

     :param values_list: list
        list of all the values
    :param value: string
        name of the column
    :return:
        dictionary named by the value name and containing all frequencies
        for rows as integer values
    """
    frequency_values_dict = {}
    y = np.bincount(np.array(values_list, dtype=int))
    ii = np.nonzero(y)[0]
    tmp_dict = {}
    for val in ii:
        tmp_dict[val] = y[val]
    frequency_values_dict["{} frequencies".format(value)] = tmp_dict
    return frequency_values_dict


def get_frequency_count_str(values_list, value):
    """Counts frequency for columns containing strings

     :param values_list: list
        list of all the values
    :param value: string
        name of the column
    :return:
        dictionary named by the value name and containing all frequencies
        for rows as integer values
    """
    frequency_values_dict = {}
    tmp_dict = {}
    tmp_set_of_str = {""}
    for feature in values_list:
        if feature not in tmp_set_of_str:
            tmp_dict[feature] = 1
            tmp_set_of_str.add(feature)
        else:
            tmp_dict[feature] = tmp_dict.get(feature) + 1
    frequency_values_dict["{} frequencies".format(value)] = tmp_dict
    return frequency_values_dict


def get_frequency_count_bool(values_list, value):
    """Counts frequency for columns containing type boolean

         :param values_list: list
        list of all the values
        :param value: string
            name of the column
        :return:
            dictionary named by the value name and containing all frequencies
            for rows as integer values
        """
    frequency_values_dict = {}
    tmp_dict = {}
    for feature in values_list:
        if feature not in tmp_dict:
            tmp_dict[feature] = 1
        else:
            tmp_dict[feature] = tmp_dict.get(feature) + 1
    frequency_values_dict["{} frequencies".format(value)] = tmp_dict
    return frequency_values_dict
