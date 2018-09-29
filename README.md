[![Build Status](https://travis-ci.org/Quer-io/Quer.io.svg?branch=master)](https://travis-ci.org/Quer-io/Quer.io)
[![Coverage Status](https://coveralls.io/repos/github/Quer-io/Quer.io/badge.svg?branch=master)](https://coveralls.io/github/Quer-io/Quer.io?branch=master)

# Quer.io

## Documentation links
See [Documentation](https://github.com/Quer-io/Quer.io/tree/master/documentation/) for Documentation

See [Database Schema](https://github.com/Quer-io/Quer.io/tree/master/documentation/database/schema.md) for Database Schema

## Project description


## Installation

This project is done with Python version 3.6

See [Database Installation guide](https://github.com/Quer-io/Quer.io/tree/master/documentation/database/db_readme.md) for information how to install PostgreSQL database dumps as local databases.

### Libraries
Every time a new library is used, the name of the library needs to be added to requirements.txt. Every time you run the project with new libraries the following command is needed. It will install all the necessary libraries to your machine:

`pip3 install --user -r requirements.txt`

### Tests
Currently the project contains tests that are done using the [unittest](https://docs.python.org/3/library/unittest.html) library. Tests can be run with the following command from the project root

`python3 -m unittest discover`

This command will find every test from the project and run it. If you want to run an individual test script it can be done with the following command

`python3 -m unittest [path to file]` 


## Contributors
- [Dennis Ahlfors](https://github.com/Dforssi)
- [Joonas J]()
- [Kim Toivonen](https://github.com/ConstantKrieg)
- [Mauri Frestadius](https://github.com/Suidat)
- [Ossi Räisä](https://github.com/oraisa)
- [Petja Valkama](https://github.com/xbexbex)
