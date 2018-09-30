# Application installation guide

This guide is written for Linux and Mac users who are familiar with CLI commands and git.

Required tools for installing are:
+ Access to a CLI shell
+ Python
+ Pip (included in Python versions > 3.4)
+ Git CLI

### Python

Should you for some reason NOT have Python already included in your distribution of Linux, you should install Python 3.6 using your packet manager of choice. Python3 should be included in all releases of Mac OS X for Mac users.

### Git

Navigate to the [Repository](https://github.com/Quer-io/Quer.io). You can find the repository link at the green "Clone or Download" button. Copy this link and navigate to the folder where you want to clone this project to.

```
$> git clone <link from repo> <project_folder>
```

You now have a working copy of the project files on your own computer.

### Installation

Navigate to the folder you just created by cloning the git project. Next step is to activate Python virtual environment, do this with the following command:
```python
source venv/bin/activate
```

If this succeeds, your path marker with now look like:

```
(venv) $>
```

Now you can install the requirements from requirements.txt file, do this by running the following command:

```python
(venv) $> pip install -r requirements.txt
```

This will install all the required dependencies on your local machine. Next navigate to /application folder and run the project with following command:

```python
(venv) $> python3 querio.py
```

The application should now start and is ready to use!

### Libraries
Every time a new library is used, the name of the library needs to be added to requirements.txt. Every time you run the project with new libraries the following command is needed. It will install all the necessary libraries to your machine:

`pip3 install --user -r requirements.txt`