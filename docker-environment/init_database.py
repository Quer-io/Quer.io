import numpy as np
from sklearn.datasets import make_regression
from scipy.stats import norm, itemfreq
import pandas as pd
import sys
import time
import argparse
import os
import psycopg2

parser = argparse.ArgumentParser()
parser.add_argument(
    'RowCount', type=int, help='The number of rows to generate'
)
parser.add_argument(
     'Filename', help='Save the data to a file', type=str
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
        'age': age, 'income': income, 'github_stars': github_stars,
        'height': height, 'profession': profession, 'is_client': is_client,
    }
)
print('Max age {0}, min age: {1}'.format(age.max(), age.min()))
print('Max income {0}, min income: {1}'.format(income.max(), income.min()))
print('Max stars {0}, min stars: {1}'.format(github_stars.max(),
                                             github_stars.min()))
print('Max height {0}, min height: {1}'.format(height.max(), height.min()))
print('Profession counts')
print(df.profession.value_counts())
print('Client counts')
print(df.is_client.value_counts())
print(df[0:20])


try:
    conn = psycopg2.connect(host="db", port="5432", user="queriouser",
                            password="pass1", dbname="queriodb")
except (Exception, psycopg2.DatabaseError) as error:
        print("Could not connect to database. Aborting...")
        print(error)
        sys.exit(1)

df.to_csv(args.Filename)

cursor = conn.cursor()

try:

    print("Connected to postgresql in address 0.0.0.0:5432")

    print("Creating table 'person'")
    cursor.execute("DROP TABLE IF EXISTS person;")

    create_person_command = """CREATE TABLE public.person (id integer,
                                                          age decimal,
                                                          income decimal,
                                                          github_stars decimal,
                                                          height decimal,
                                                          profession varchar,
                                                          is_client boolean);
                                                          """

    cursor.execute(create_person_command)

    print("Table 'person' created")

    with open(args.Filename, 'r') as file:
        next(file)
        print("Copying data to database...")
        cursor.copy_from(file, 'person', sep=',')
        print("Data copied!")

    conn.commit()
except Error as e:
    print(e)
finally:
    if os.path.exists(args.Filename):
        os.remove(args.Filename)
    cursor.close()
    conn.close()
