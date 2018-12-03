[![Build Status](https://travis-ci.org/Quer-io/Quer.io.svg?branch=master)](https://travis-ci.org/Quer-io/Quer.io)
[![Coverage Status](https://coveralls.io/repos/github/Quer-io/Quer.io/badge.svg?branch=master)](https://coveralls.io/github/Quer-io/Quer.io?branch=master)

# Quer.io

## Documentation links
See [Documentation](https://github.com/Quer-io/Quer.io/tree/master/documentation/) for Documentation

See [Usage guide](https://github.com/Quer-io/Quer.io/tree/master/documentation/querio101.md) for a basic rundown on how to use Quer.io

See [Database Schema 1](https://github.com/Quer-io/Quer.io/tree/master/documentation/database/schema.md) for single table sample database schema

See [Database Schema 2](https://github.com/Quer-io/Quer.io/blob/db/normalized/documentation/database/normalized_schema.md) for normalized sample database schema

See [ML documentation](https://github.com/Quer-io/Quer.io/tree/master/documentation/ml/model.md) for documentation
of the machine learning model quer.io uses

## Project description

This project is built to the specifications and requirements provided by Prof. Michael Mathioudakis and is a course work project for course TKT20007 Software Engineering Lab at the University of Helsinki, department of Computer Science.

The aim of this project is to build an Approximate Query Processing (AQP) engine -- i.e., a software layer on top of a relational database, that allows us to obtain fast, approximate answers to aggregate queries, with the help of Machine Learning models.

Chosen implementation is Python for the application and Postgres for the database. The Querio library will be importable as a Library. Machine learning components are built using Scikit Learn and the optional graphical user interface and application is build using Kivy.

## Installation

This project is done with Python version 3.6

See [Database Installation guide](https://github.com/Quer-io/Quer.io/tree/master/documentation/database/db_readme.md) for information how to install the sample databases this application was tested on.

See [Application Installation guide](https://github.com/Quer-io/Quer.io/tree/master/documentation/install.md) for information how to install the application and all its dependencies.

### Tests
Currently the project contains tests that are done using the [unittest](https://docs.python.org/3/library/unittest.html) library. Tests can be run with the following command from the project root

`python3 -m unittest discover`

This command will find every test from the project and run it. If you want to run an individual test script it can be done with the following command

`python3 -m unittest [path to file]`

## Contributors
- [Dennis Ahlfors](https://github.com/Dforssi)
- [Joonas J](https://github.com/JaykobJ)
- [Kim Toivonen](https://github.com/ConstantKrieg)
- [Mauri Frestadius](https://github.com/Suidat)
- [Ossi Räisä](https://github.com/oraisa)
- [Petja Valkama](https://github.com/xbexbex)
