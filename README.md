# UrlShorten
Objective: Create a webservice which can shorten urls like TinyURL and bit.ly

**Getting Started**

1. Clone this repository by running

$ https://github.com/Daphnie-Lias/UrlShorten.git

2. Install python from https://python.org or via your favorite package manager (homebrew for MAC)
   brew install python
  
   Verify python version: 
   >python3 -V 
   >Python 3.7.6


2. Install Pipenv Globally
Open Terminal in (Applications/Utilities/Terminal) and upgrade pip:

python3.7.6 -m pip install pip --upgrade
Another option to upgade, is pip3 install pip --upgrade

Install Pipenv:

python3.7.6 -m pip install pipenv

3. Create Virtual Environment with Pipenv
Open Terminal in (Applications/Utilities/Terminal)

Make directory :mkdir urlproj

Activate the Virtual Environment:

pipenv shell
 
$ pip install -r requirements.txt

4. DB Setup:
 If tables are not created on startup , use the below commands: (one time) 

$ On Terminal-> python
$ > from url_shorten import create_app
>from url_shorten.extensions import db
>from url_shorten.models import Url
> db.create_all(app=create_app())

7. To check if tables are created 
$ > sqlite3 url_shorten/db.sqlite3
$ > .tables

8. To run the application from Terminal 
> flask run

Expected Output:
(urlproj) (base) daphnie@bb-system-1128 urlproj % flask run
 * Serving Flask app "url_shorten" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 288-614-491

Deliverables

● Source code - COMPLETE

● Simple way to to setup a virtual environment with the necessary python libraries -COMPLETE

● Instructions to start the application -COMPLETE

● Instructions to run unit test(s) - IN PROGRESS / INCOMPLETE


Improvements:

1. To use an in-memory datastore like Redis, to fetch the auto-increment Id's and use a strong encryption algorithm like Base62 / MDF 5 to generate the short codes.

2. To complete the unit tests and validation 

3. To run a performance test , to able to test the application concurrently atleast to support 10 active threads.

4. Dockerize the application for easier portability.

4. Deploy the application in Heroku - with production configuration

