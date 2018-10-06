
def make_into_list_if_scalar(list_or_scalar):
    if isinstance(list_or_scalar, list):
        return list_or_scalar
    else:
        return [list_or_scalar]
