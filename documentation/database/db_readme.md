# How to install a local copy of the sample database

We recommend using docker.

## Installing the docker container with built in example database of 10 000 000 rows

See [Docker readme and install guide](https://github.com/Quer-io/Quer.io/blob/master/docker-environment/README.md)

## Installing a local Postgres instance with a DB of 1000 rows:

NOTE! '< >' refer to user specific values and should be changed accordingly!

### Prerequisites
- Basic CLI knowledge

- Valid and installed version of PostgreSQL on your machine.

```
$> sudo apt-get install postgresql
```

- Current database dump is set to public as default

### Installing a sample database through a dump file
- Download the the dump file

- Create a new empty database

```
$> createdb <database_name>
```

- Should you have permission problems, you might want to use the following command with admin user postgres:

```
$> sudo -u postgres createdb <database_name>
```

- Initialize the dump file to the new (empty) database

```
$> psql <database_name> < ~/<folder>/dump_1000
```

- You will now see the database initialize and should be usable after that

- You can now connect to the database filled with dump data with normal psql CLI commands

```
$> psql <database_name>
```
 - Data is located in public schema, accessible by default (no set search_path required!)

 - You can check if the database intialized correctly with the following command, that should return table information

```sql
database_name=> \d person
```

- Database can be queried with standard SQL commands

- Should you have problems, don't hesitate to contact the team!

