import unittest
from url_shorten.views import short
from unittest import mock
import datetime,pytest,json
from http import HTTPStatus
from url_shorten import create_app

class TestUrlShorten(unittest.TestCase):
    #client = create_app.test_client()

    def test_index(self):
        res = self.get('/')
        assert res.status_code == 200
        expected = {'hello': 'world'}
        assert expected == json.loads(res.get_data(as_text=True))


    def test_shorten(self):
        post_data = { "url": "https://www.energyworx.com/", "shortcode": "ewx123" }
        body = short.shorten(post_data)
        response = self.fetch(r'/shorten', method='POST', body=body)
        self.assertEqual(response.code, 201)
        self.assertEqual(response.body, b'{"shortcode": "ewx123')


    @pytest.mark.parametrize('url', [
        'https://flask.palletsprojects.com/en/1.1.x/testing/'
        'https://realpython.com/python-web-applications-with-flask-part-iii/',
        'http://foo.com/blah_blah_(wikipedia)',

    ])
    def test_valid_url(url):
        #url ="https://www.google.com"
        url.assertTrue(short.uri_validate(url))

    def test_missing_url(self):

        response = self.get('https://some-id/missing-url/')
        assert response.status_code == HTTPStatus.NOT_FOUND, 'Url not present'
        assert response.json['code']
        assert response.json['message']

    def test_empty_url_not_valid(self):
        url = ''

        self.assertFalse(short.uri_validate(url))

    def test_generate_shortcode(self):

        code = short.generate_short_link()
        assert any(substr.isdigit() or substr.isalpha() for substr in code)



    # def test_date_format(self):
    #
    #     #return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    #     assert(self.test_date_format())