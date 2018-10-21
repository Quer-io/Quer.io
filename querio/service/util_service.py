import numpy as np


def frequency_count(data, values):
    result_list = []
    for value in values:
        list_item = data['%s' % value].values.tolist()
        item_type = type(list_item[0])
        if item_type is int or item_type is float:
            result_list.append(frequency_count_int(data, value))
        elif item_type is str:
            result_list.append(frequency_count_str(data, value))
    return result_list


def frequency_count_int(data, value):
    frequency_values_dict = {}
    feature_list = data['%s' % value].values.tolist()
    y = np.bincount(np.array(feature_list, dtype=int))
    ii = np.nonzero(y)[0]
    tmp_dict = {}
    for val in ii:
        tmp_dict[val] = y[val]
    frequency_values_dict["{} frequencys".format(value)] = tmp_dict
    return frequency_values_dict


def frequency_count_str(data, value):
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
    frequency_values_dict["{} frequencys".format(value)] = tmp_dict
    return frequency_values_dict

