# Docker for Querio

## Installation
First you have to install Docker-CE and Docker Compose according to following instructions

### Docker CE
  - [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
  - [MacOS](https://docs.docker.com/docker-for-mac/install/)
  - [Windows](https://docs.docker.com/docker-for-windows/install/)

### [Docker Compose](https://docs.docker.com/compose/install/)


 ---

 ## Setting up the environment

 After installing Docker and Docker Compose first thing to do is to navigate to docker folder. This can be done from the project root in any unix based OS by the following command:

 `cd docker-environment`

 Now container can be built and started by issuing the following:

 `docker-compose up`

 This will always set up the database and populate it with 10 million rows
 
 Generating 10 million rows and copying them to the database could take couple of minutes.

 Data is persistent in the Docker container so data needs to be generated only the first time docker-compose is launched. After this you can just start the database without the populator with the following command:

 `docker-compose up db`

 If you manually delete the docker container or the /data-folder it will be necessary to populate the database again

 _Docker command might not work without root access. If this causes problems just add `sudo` in front of the command_

 `docker-compose up` will start all services defined in `docker-compose.yml`. Currently there are two services:
  ### **db** 
  This is a official postgresql container. Postgres is launched to listen address 0.0.0.0 and port 5432. This database can be logged in with username **queriouser** and password **pass1**.
  This service creates a default database which is named **queriodb**

  ### **db-populator**
  This service is a container which is defined in `Dockerfile`. This service is built on top of 
  [frolvlad/alpine-python-machinelearning](https://hub.docker.com/r/frolvlad/alpine-python-machinelearning/)-image. This Docker container has a Python 3.6 run environment with preinstalled Scipy, Pandas, Numpy and Scikit-learn. When this service is built contents of `requirements.txt` are installed exclusively for the **db-populator**-container.

  After it's done with installing everything it will launch `init_db.py`. This python script connects to the postgres database and creates a table named **person**.
  After this it generates a fixed number of rows exactly like the data generator in the tools folder. Rows are saved into a .csv-file and copied to the database. 

  ### **normalized-db-populator**
  This container is identical to db-populator but will create a normalized database with four tables.

 ## Database connection

 After running `docker-compose up`, databases can be connected with the following addresses:

 This is the connection address to the database with one table named *person* with 10 000 000 rows.
 `postgres://queriouser:pass1@localhost:5432/queriodb`

 This is the connection address to the normalized database with 10 000 rows in each table
 `postgres://queriouser:pass1@localhost:5432/normaldb`
  
## Additional steps for Windows

When Git clones a repository it automatically converts line endings in files.

This can be disabled by configuring your Git with the following command: 

`git config --global core.autocrlf input`



