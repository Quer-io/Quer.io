import numpy as np
from sklearn.datasets import make_regression
from scipy.stats import norm, itemfreq
import pandas as pd
from pandas.io import sql
import sys
import time
import argparse
import os
import psycopg2
from sqlalchemy import create_engine
import random

parser = argparse.ArgumentParser()
parser.add_argument(
    'RowCount', type=int, help='The number of rows to generate'
)

args = parser.parse_args()

id_list = []



try:
    postgres_conn = psycopg2.connect(host="localhost", port="5432", user="postgres",
                            password="", dbname="normaldb")
    postgres_cursor = postgres_conn.cursor()



except (Exception, psycopg2.DatabaseError) as error:
        print("Could not connect to database. Aborting...")
        print(error)
        if postgres_cursor:
            postgres_cursor.close()
        if postgres_conn:
            postgres_conn.close()
        sys.exit(1)

def create_tables():
    postgres_cursor.execute("DROP TABLE IF EXISTS person_github;")
    postgres_cursor.execute("DROP TABLE IF EXISTS person;")
    postgres_cursor.execute("DROP TABLE IF EXISTS person_profession;")
    postgres_cursor.execute("DROP TABLE IF EXISTS github;")

    create_person_profession_command = """
    CREATE TABLE public.person_profession(profession_id INT PRIMARY KEY NOT NULL, 
				      profession_name VARCHAR NOT NULL, 
				      description VARCHAR);
    """

    create_github_command = """
    CREATE TABLE public.github(github_id INT PRIMARY KEY, 
			   stars DECIMAL NOT NULL, 
                           link VARCHAR);
    """
    create_person_github_command = """
    CREATE TABLE public.person_github(github_id INT NOT NULL,
				  person_id INT NOT NULL,
				  CONSTRAINT person_github_github_id_fkey FOREIGN KEY (github_id)
					REFERENCES public.github (github_id) MATCH SIMPLE
					ON UPDATE NO ACTION ON DELETE NO ACTION,
				CONSTRAINT person_github_person_id_fkey FOREIGN KEY (person_id)
					REFERENCES public.person (person_id) MATCH SIMPLE
					ON UPDATE NO ACTION ON DELETE NO ACTION);
    """
    create_person_command = """CREATE TABLE public.person(person_id INT PRIMARY KEY, 
                           age DECIMAL NOT NULL, 
                           height DECIMAL NOT NULL, 
                           income DECIMAL NOT NULL, 
                           is_client BOOLEAN NOT NULL, 
                           profession_id INT NOT NULL,
                           CONSTRAINT person_profession_id_fkey FOREIGN KEY (profession_id)
				           REFERENCES public.person_profession (profession_id) MATCH SIMPLE
				           ON UPDATE NO ACTION ON DELETE NO ACTION);"""
    
    postgres_cursor.execute(create_person_profession_command)
    postgres_cursor.execute(create_github_command)
    postgres_cursor.execute(create_person_command)
    postgres_cursor.execute(create_person_github_command)
    


def save_professions():
    professions = ['president', 'basketball player', 'software architect',
                'programmer', 'reality tv star', 'student', 'soldier', 'unemployed',
                'officer', 'general', 'car salesman']

    i = 1
    for one_profession in professions:
        postgres_cursor.execute("INSERT INTO person_profession(profession_id, profession_name)" + 
                       "VALUES ({}, '{}')".format(str(i), one_profession))
        i = i+1


def create_github_stars(rc):

    github_stars_list = []
    github_name_list = []

    for i in range(0, rc):
        github_stars = random.randint(1, 5) * random.randint(1, 9) + 10 * random.randint(1,17)+ random.randint(1,15) / 6
        github_stars = np.floor(github_stars)
        github_stars_list.append(abs(github_stars))
        github_name_list.append("repo #{}".format(str(i)))

    return pd.DataFrame(
        {
        'github_id': id_list, 'stars': github_stars_list, 'link': github_name_list,
        }
    ) 

def create_person_github():
    return pd.DataFrame(
        {
        'person_id': id_list, 'github_id': id_list,
        }
    )

def create_querio_view():
    postgres_cursor.execute("""CREATE OR REPLACE VIEW querio_view AS
	SELECT 	age,
		height,
		income,
		is_client,
		profession_name,
		stars
	FROM	public.person
		INNER JOIN public.person_profession USING (profession_id)
		INNER JOIN public.person_github USING (person_id)
		INNER JOIN public.github USING (github_id);""")

def pick_profession(age, income,  height):
    if age > 50 and income > 20000:
        return 1
    if height > 190 and income > 5000:
        return 2
    if random.randint(1, 60) > 30:
        if income > 5000:
            return 3
        else:
            return 4
    if age % 2 == 0 and random.randint(1, 20) % 3 == 1:
        return 5
    if age < 20:
        return 6
    if income < 1000:
        if height > 180:
            return 7
        return 8
    if income < 5000 and height > 180:
        return 9
    if height > 180:
        return 10
    return 11

row_count = args.RowCount

for i in range(1, (row_count + 1)):
    id_list.append( i )

age, height = make_regression(row_count, 1, 1, noise=3.3, random_state=42)
age = age.reshape((row_count,))
age = np.log(age * age + 1) * 17 + 20
age = np.floor(age)
height = height * height * 6 + 500

income = norm.rvs(size=row_count, loc=180, scale=10, random_state=42)
xs = -random.randint(0, 20) * income / 10 + age**2 / 2
is_client = (norm.rvs(size=row_count, loc=-100, scale=100) + xs) > 0
profession = [
    pick_profession(age[i], income[i], height[i])
    for i in range(0, row_count)
]

github_df = create_github_stars(row_count)

person_df = pd.DataFrame(
    {
        'person_id': id_list, 'age': age, 'income': income,
        'height': height, 'is_client': is_client, 'profession_id': profession
    }
)
person_github_df = create_person_github()


github_df.to_csv("github.csv", index=False)
person_df.to_csv("persons.csv", index=False)
person_github_df.to_csv("persons_github.csv", index=False) 



try:
    create_tables()
    save_professions()

    print("Connected to postgresql")

    with open("github.csv", 'r') as file:
        next(file)
        print("Copying data to github...")
        postgres_cursor.copy_from(file, 'github', sep=',')
        print("Data copied to github!")

    with open("persons.csv", 'r') as file:
        next(file)
        print("Copying data to person...")
        postgres_cursor.copy_from(file, 'person', sep=',')
        print("Data copied to person!")

    with open("persons_github.csv", 'r') as file:
        next(file)
        print("Copying data to github...")
        postgres_cursor.copy_from(file, 'person_github', sep=',')
        print("Data copied to person_github!")

    create_querio_view()
    postgres_conn.commit()

except Error as e:
    print(e)
finally:
    if os.path.exists("persons.csv"):
        os.remove("persons.csv")
    if os.path.exists("github.csv"):
        os.remove("github.csv")
    if os.path.exists("persons_github.csv"):
        os.remove("persons_github.csv")
    postgres_cursor.close()
    postgres_conn.close()
