# UrlShorten
Objective: Create a webservice which can shorten urls like TinyURL and bit.ly

Getting Started

1. Clone this repository by running

$ https://github.com/Daphnie-Lias/UrlShorten.git

2. Install python from https://python.org or via your favorite package manager
3. Install virtualenv

$ pip3 install virtualenv
4.If you get a note from pip about virtualenv not being in your PATH, you need to perform this step. 
PATH is a variable accessible from any bash terminal you run, and it tells bash where to look for the commands you enter. 
It is a list of directories separated by :. You can see yours by running echo $PATH. To run virtualenv commands, you need to add python’s packages to your PATH by editing or creating the file ~/.bash_profile on MacOS. 
To that file add the following lines:

PATH="<Path from pip message>:$PATH"
export PATH
5. Then you can install dependencies into a virtual environment

$ cd flask_tests_workshop
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

DB Setup:
6. If tables are not created on startup , use the below commands:

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




