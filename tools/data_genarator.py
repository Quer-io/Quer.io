import numpy as np
from sklearn.datasets import make_regression
from scipy.stats import norm, itemfreq
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    'RowCount', type=int, help='The number of rows to generate'
)
parser.add_argument(
    '--show-graph',
    help='Show a graph of the results, -x and -y must be given',
    action='store_true'
)
parser.add_argument(
    '-x', help='The x-axis of the graph', type=str,
    choices=['Age', 'Income', 'Height', 'Github_stars']
)
parser.add_argument(
    '-y', help='The y-axis of the graph', type=str,
    choices=['Age', 'Income', 'Height', 'Github_stars']
)
parser.add_argument(
    '-f', '--file', help='Save the data to a file', type=str
)
args = parser.parse_args()


def pick_profession(age, income, github_stars, height):
    if age > 50 and income > 20000:
        return 'president'
    if height > 190 and income > 5000:
        return 'basketball player'
    if github_stars > 30:
        if income > 20000:
            return 'software architect'
        else:
            return 'programmer'
    if age % 2 == 0 and github_stars % 3 == 1:
        return 'reality tv star'
    if age < 20:
        return 'student'
    if income < 1000:
        if height > 180:
            return 'soldier'
        return 'unemployed'
    if income < 5000 and height > 180:
        return 'officer'
    if height > 180:
        return 'general'
    return 'car salesman'


row_count = args.RowCount
age, income = make_regression(row_count, 1, 1, noise=3.3, random_state=42)
age = age.reshape((row_count,))
age = np.log(age * age + 1) * 17 + 20
age = np.floor(age)
income = income * income * 6 + 500
github_stars = -0.169 * age * age + 10 * age + income / 750 - 130
github_stars = np.floor(github_stars)
height = norm.rvs(size=row_count, loc=180, scale=10, random_state=42)
xs = -github_stars * height / 10 + age**2 / 2
is_client = (norm.rvs(size=row_count, loc=-100, scale=100) + xs) > 0
profession = [
    pick_profession(age[i], income[i], github_stars[i], height[i])
    for i in range(0, row_count)
]
df = pd.DataFrame(
    {
        'Age': age, 'Income': income, 'Github_stars': github_stars,
        'Height': height, 'Profession': profession, 'Is_client': is_client,
    }
)
print('Max age {0}, min age: {1}'.format(age.max(), age.min()))
print('Max income {0}, min income: {1}'.format(income.max(), income.min()))
print('Max stars {0}, min stars: {1}'.format(github_stars.max(), github_stars.min()))
print('Max height {0}, min height: {1}'.format(height.max(), height.min()))
print('Profession counts')
print(df.Profession.value_counts())
print('Client counts')
print(df.Is_client.value_counts())
print(df[0:20])
if args.show_graph:
    plt.plot(df[args.x], df[args.y], 'o')
    plt.show()
if args.file is not None:
    df.to_csv(args.file)
