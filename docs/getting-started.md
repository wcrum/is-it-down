# Getting Started
- [Getting Started](#getting-started)
- [Requirements](#requirements)
  - [File Structure](#file-structure)
  - [Cloning the repository](#cloning-the-repository)
  - [Python Virtual Environment](#python-virtual-environment)
  - [Setting up the Database](#setting-up-the-database)
  - [Starting Is It Down](#starting-is-it-down)

# Requirements
To get started you will need [Python](https://www.python.org/). Because this application is a Server Side Rendered site you do not need to download anything else.

## File Structure
```
.
├── app
│   ├── models
│   ├── pages
│   ├── routes
│   ├── static
│   ├── templates
│   │   ├── admin
│   │   ├── main
│   │   └── modals
│   └── utils
├── data
├── docs
└── tests
    └── fixtures
```

- `/app`: Contains core application files.
    - `/models`: SQLModel / MySQL schema.
    - `/pages`: Site Static Rendered Markdown Files.
    - `/routes`: Main site path handling and requests.
    - `/static`: Static application files (images, css, js).
    - `/utils`: Utilites used across the application.
- `/data`: Template data sourced from data.gov and defense.gov. Contains web scrapping script.
- `/tests`: PyTest testing files and fixtures.

## Cloning the repository
Ensure you have a up to date copy of the repository. You can do this by simple running the below command.
```
git clone https://github.com/elisoncrum/is-it-down
```
Just like that you have a up to date copy of the site.

## Python Virtual Environment
Containers are amazing, it is recommended that you use a virtual environment for python to ensure you dont run into any issues. Make sure you have Python [venv](https://docs.python.org/3/library/venv.html) installed.

You can install all requirements with the below commands.
```python
python3 -m venv env
```
This should create a directory called `env/`, now to initiate that environment run:
```
source env/bin/activate
```
Now you should should be in a seperate environment. Ensure you have all required python packages running:
```
(venv) pip3 install -r requirements.txt
```

## Setting up the Database
When working with the database it may be difficult to work and test the database if schemas have been changed. To mitigate this in the source directory `database-tools.py` has been created to help import data, drop, or update schema.

See [Database Tools](database-tools.md) for more information.

Starting the database:
```
docker compose up
```
This will create a MySQL instance and a [User Access and Authentication](https://github.com/hortonworks/docker-cloudbreak-uaa) (UAA) instnace. The UAA is the default authentication server that Cloud Foundry utilizes.

The default **username** is `paul` and the default **password** is `wombat`.

Read more [Cloud Foundry - UAA](https://docs.cloudfoundry.org/concepts/architecture/uaa.html).

Setting up and populating the database:
```shell
python3 database-tools.py tables create
python3 database-tools.py import file data/data.txt
```

## Starting Is It Down
With the UAA and MySQL instance started you should have everything ready to start the server. In the local and testing environment it is important to start the worker thread manually as it is a continously running thread. It checks every domain name that was uploading using `database-tools.py`.

You can start the thread by running:
```
python3 worker.py
```

Output from this worker should look something like: It will run until destroyed.
```
server_id=1 datetime=datetime.datetime(2022, 1, 30, 19, 5, 20) response_time=9 url='www.neatdomain.com' id=25 response_code=200 ipaddress='123.123.123.123' error=None
server_id=2 datetime=datetime.datetime(2022, 1, 30, 19, 5, 20) response_time=11 url='www.neatdomain.com' id=26 response_code=200 ipaddress='ffff:ffff:ffff:ffff:ffff:ffff' error=None
server_id=3 datetime=datetime.datetime(2022, 1, 30, 19, 5, 20) response_time=11 url='www.cooldomain.com' id=27 response_code=200 ipaddress='123.123.123.123' error=None
server_id=4 datetime=datetime.datetime(2022, 1, 30, 19, 5, 20) response_time=10 url='www.anotherdomain.com' id=28 response_code=200 ipaddress='ffff:ffff:ffff:ffff:ffff:ffff' error=None
server_id=5 datetime=datetime.datetime(2022, 1, 30, 19, 5, 21) response_time=50 url='www.yourdomain.com' id=29 response_code=403 ipaddress='123.123.123.123' error=None
```

Now that we have a worker populating the data you should now be able to start the application while still seeing live data.
```
python3 main.py
 * Serving Flask app 'main' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://localhost:8000/ (Press CTRL+C to quit)
```
Understand that this is a local test driven environment, see running in production.