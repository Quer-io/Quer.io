
def make_into_list_if_scalar(list_or_scalar):
    if isinstance(list_or_scalar, list):
        return list_or_scalar
    else:
        return [list_or_scalar]


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
