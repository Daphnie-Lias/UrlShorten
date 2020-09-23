"""This script is used to initialize the Database tables."""

from url_shorten import create_app
from url_shorten.extensions import db
from url_shorten.models import Url

with create_app.test_request_context():
    db.create_all(app=create_app())