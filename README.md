[![Build Status](https://travis-ci.org/Quer-io/Quer.io.svg?branch=master)](https://travis-ci.org/Quer-io/Quer.io)
[![Coverage Status](https://coveralls.io/repos/github/Quer-io/Quer.io/badge.svg?branch=master)](https://coveralls.io/github/Quer-io/Quer.io?branch=master)

# Quer.io

## Documentation links
See [Documentation](https://github.com/Quer-io/Quer.io/tree/master/documentation/) for Documentation

See [Usage guide](https://github.com/Quer-io/Quer.io/tree/master/documentation/querio101.md) for a basic rundown on how to use Quer.io

See [Database Schema](https://github.com/Quer-io/Quer.io/tree/master/documentation/database/schema.md) for Database Schema

See [ML documentation](https://github.com/Quer-io/Quer.io/tree/master/documentation/ml/model.md) for documentation
of the machine learning model quer.io uses

## Project description

This project is built to the specifications and requirements provided by Prof. Michael Mathioudakis and is a course work project for course TKT20007 Software Engineering Lab at the University of Helsinki, department of Computer Science.

The aim of this project is to build an Approximate Query Processing (AQP) engine -- i.e., a software layer on top of a relational database, that allows us to obtain fast, approximate answers to aggregate queries, with the help of Machine Learning models.

Chosen implementation is Python for the application and Postgres for the database. The Querio library will be importable as a Library. Machine learning components are built using Scikit Learn and the optional graphical user interface and application is build using Kivy.

## Installation

This project is done with Python version 3.6

See [Database Installation guide](https://github.com/Quer-io/Quer.io/tree/master/documentation/database/db_readme.md) for information how to install PostgreSQL database dumps as local databases.

See [Application Installation guide](https://github.com/Quer-io/Quer.io/tree/master/documentation/install.md) for information how to install the application and all its dependencies.

### Tests
Currently the project contains tests that are done using the [unittest](https://docs.python.org/3/library/unittest.html) library. Tests can be run with the following command from the project root

`python3 -m unittest discover`

This command will find every test from the project and run it. If you want to run an individual test script it can be done with the following command

`python3 -m unittest [path to file]`

## FAQ

#### Is this a commercial product?
No, the rights for this project have been relinquished to the University Of Helsinki as per a mutual agreement. The project is also assessed as course work and as of such is a lab project to begin with. The creators of this project do not claim any commercial interest in the final product.

#### Can I use this project for my own purposes?
YES! This project is distributed with The MIT Open Source Licence, which allows usage without restrictions for your own purposes. Read more at [The MIT Licence](https://opensource.org/licenses/MIT).

#### Will you guarantee that the product is operational at all times and all systems?
Unfortunately this is an ongoing project with changing requirements, so usage will depend on how the product evolves. Generally speaking all code that is pushed to GitHub should keep the product operational, but this can not be guaranteed. Your system settings and specs might also affect the use of this project. As per the MIT licence, there is no warranty or responsibility from our side. While we might provide some support if asked, this will be an exception.

#### Can I use your Heroku -database?
No, you will have to requisiton your own database and install from the dump, or install a local database on your computer.

#### Can I contribute to the project?
As for now, no outside contributions will be allowed due to course work assessments.

## Contributors
- [Dennis Ahlfors](https://github.com/Dforssi)
- [Joonas J](https://github.com/JaykobJ)
- [Kim Toivonen](https://github.com/ConstantKrieg)
- [Mauri Frestadius](https://github.com/Suidat)
- [Ossi Räisä](https://github.com/oraisa)
- [Petja Valkama](https://github.com/xbexbex)
