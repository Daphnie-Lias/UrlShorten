import json

import pytest

from sqlalchemy_utils.functions import create_database, database_exists, \
    drop_database

from url_shorten import create_app
from url_shorten.extensions import db
from url_shorten.models import Url


@pytest.fixture(scope='session')
def app(request):

    with create_app.app_context():

        if not database_exists(db.engine.url):
            create_database(db.engine.url)
            db.create_all()

        yield create_app

        drop_database(db.engine.url)



def test_shorten_url_returns_404_when_invalid_url(app):
    with app.test_client() as c:
        response = c.post(
            '/shorten',
            content_type='application/json',
            data=json.dumps({ 'url': 'https://www.ener.com/', 'shortcode': 'ewx123' }),
        )

    assert response.status_code == 404
    assert json.loads(response.data) == {u'message': u'Url not present'}


def test_shorten_url_returns_404_when_url_over_2000_chars(app):
    with app.test_client() as c:
        response = c.post(
            '/shorten',
            content_type='application/json',
            data=json.dumps({
                'url': 'http://test.com?foo=' + 'bar' * 2000,
            }),
        )

    assert response.status_code == 404
    assert json.loads(response.data) == {u'message': u'the url is too long - maximum is 2000 characters'}


def test_shorten_url_returns_201_when_ok(app):
    with app.test_client() as c:
        response = c.post(
            '/shorten',
            content_type='application/json',
            data=json.dumps({ "url": "https://www.energyworx.com/", "shortcode": "ewx123" }),
        )

    assert response.status_code == 201

    url = Url.query.filter_by(url="https://www.energyworx.com/").all()
    assert url


def test_get_url_returns_404_when_not_found(app):
    with app.test_client() as c:
        response = c.get('/foo')

    assert response.status_code == 404


def test_get_url_redirects(app):
    with app.test_client() as c:
        response = c.post(
            '/shorten',
            content_type='application/json',
            data=json.dumps({
                'url': 'http://127.0.0.1:5000/qBA3F1',
            }),
        )
        assert response.status_code == 201

        short_url = json.loads(response.data)

        response = c.get(short_url['shortened_url'])

        assert response.status_code == 302
        assert response.location == "https://www.energyworx.com/"


