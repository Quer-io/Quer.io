
def make_into_set(value):
    if isinstance(value, set):
        return value
    elif isinstance(value, list):
        return set(value)
    else:
        return {value}


class Population:
    def __init__(self, samples, mean, variance):
        self.samples = samples
        self.mean = mean
        self.variance = variance


def calculate_mean_and_variance_from_populations(populations):
    total_n = sum([pop.samples for pop in populations])
    value_sums = [pop.mean * pop.samples for pop in populations]
    total_mean = sum(value_sums) / total_n

    square_error_sums = [
        pop.variance * pop.samples + pop.samples * (pop.mean - total_mean)**2
        for pop in populations
    ]
    total_variance = sum(square_error_sums) / total_n
    return (total_mean, total_variance)


def get_feature_min_max_count(data, feature_names):
    feat_dict = {}
    for feat in feature_names:
        feat_dict[feat] = {
            "max": data.max().get('%s' % feat),
            "min": data.min().get('%s' % feat),
            "count": data.count().get('%s' % feat)
        }
    return feat_dict
