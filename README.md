
# api-server-v1

mySQL
-------
Make sure mysql is installed first and has the following:
1. User named stogora_dev
2. stogora_dev has password 'stogora'
3. There is a database named 'stogora_dev'

How to install mySQL
-------
1. Ubuntu: sudo apt-get install mysql-server libmysqlclient-dev; export PATH=/usr/bin/mysql/:$PATH;
2. MacOS: http://www.macminivault.com/mysql-yosemite/ or http://www.macminivault.com/mysql-mavericks/

Setup
-------
1. create a virtual environment via "virtualenv venv"
2. Second soruce the environment via "source venv/bin/activate"
3. In the project root run: "pip install -r requirements.txt" while in the virtual environment
4. replace 'xxxx' in config.py with keys and urls

Run python "manage.py database reset" to populate mock data

Running the Server
-------
Use the following commands:
1. source venv/bin/activate
2. ./manage.py runserver -d
