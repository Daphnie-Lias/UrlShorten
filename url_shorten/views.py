from flask import Blueprint, render_template, request,redirect,jsonify,abort
from .extensions import db
from .models import Url
from .forms import UrlShortenForm
import string,datetime,re,requests
from random import choices


short = Blueprint('short', __name__)

@short.route('/<shortcode>')
def redirect_to_url(shortcode):

    """GET endpoint that takes a short code and redirects if successfull, with Location set as Response header
    Otherwise returns a bad request.
    Arguments:
    shortcode, the string representing a shortened url.
    Return values:
    A Flask redirect, with code 302.
    """
    link = Url.query.filter_by(short_url=shortcode).first_or_404()
    link.visits = link.visits + 1
    db.session.add(link)
    db.session.commit()
    response = jsonify()
    response.status_code = 302
    response.headers['Location'] = link.original_url
    response.autocorrect_location_header = False


    return jsonify({ 'Location' : link.original_url }) ,302


@short.route('/')
def index():
    return render_template('index.html')

@short.route('/shorten', methods=['POST'])
def shorten():
    """Shortens a url by generating a 6 digit short code using generate_short_link().
    Parameters:
    url - the url to be shortened.
    shortcode - User supplied shortcode (optional)
    Return values:
    Alphanumeric string, the unique shortened url, acting as a key for the entered long url.
    """
    if request.mimetype == 'application/json':
        data = request.get_json()
        original_url = data['url']
        code = data['shortcode']
    else:
        original_url = request.form['url']
        code =request.form['shortcode']

    if request.method == 'POST' :
        if not code:
          ''' Check if original input url is a valid url '''
          uri_exists = uri_validate(original_url)
          if(uri_exists == False):
            abort(400)
          else:
            code = generate_short_link()
            link = Url(original_url=original_url,short_url=code)
            db.session.add(link)
            db.session.commit()

        else:
            ''' Short_code validation '''
            short_code_exists = db.session.query(db.exists().where(Url.short_url == code)).scalar()
            short_code_valid = bool(shortcode_validate(code))

            if  short_code_valid == False:
                abort(412)

            elif  short_code_exists :
                abort(409)

            elif not short_code_exists and short_code_valid == True:
                link = Url(original_url=original_url,short_url=code)
                db.session.add(link)
                db.session.commit()

        return jsonify({'shortcode': code}), 201

    else:
        return render_template("index.html")



def generate_short_link():
    """
    Return values: Generates the short code;
    Future scope: To generate unique short_code using base64 encoding and datastore (Redis)
    """
    chars = string.ascii_letters + string.digits
    code = ''.join(choices(chars, k=6))
    exists = db.session.query(
    db.exists().where(Url.short_url == code)).scalar()
    if not exists:
        return code
    else:
        generate_short_link()


@short.route('/<shortcode>/stats',methods =['GET'])
def stats(shortcode):
    """
    Lists the stats for specific short_code
    Returns: Created_Date , lastRedirect ,redirectCount
    """
    links = Url.query.with_entities(Url.created_at,Url.last_access,Url.visits).filter_by(short_url=shortcode).first_or_404()
    return jsonify({ 'created' : format_date_iso(links.created_at),  'lastRedirect' : format_date_iso(links.last_access) ,  'redirectCount' : links.visits })

def format_date_iso(date):
    """
    Formats Date into ISO8601
    """
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

def uri_validate(uri: str) -> bool:
    """Validates if provided long url is valid
    Parameters:
    url - Original url.
    Return values:
    Boolean, indicating the validity of the url.
    """
    try:
        with requests.get(uri, stream=True) as response:
            try:
                response.raise_for_status()
                return True
            except requests.exceptions.HTTPError:
                return False
    except requests.exceptions.ConnectionError:
        return False

def shortcode_validate(shortcode):
    """Validates short code by parsing it with a regular expression.
    Parameters:
    url - shortened url.
    Return values:
    Boolean, indicating the validity of the shortcode.
    """
    pattern = re.compile('^\w{6}$')
    status = re.match(pattern, shortcode)

    return status

@short.errorhandler(400)
def url_not_found(e):
    return jsonify(error='URL Not Present'), 400


@short.errorhandler(409)
def shortcode_in_use(e):
    return jsonify(error='Shortcode already in use'), 409


@short.errorhandler(412)
def shortcode_invalide(e):
    return jsonify(error='The provided shortcode is invalid'), 412


@short.errorhandler(404)
def shortcode_not_found(e):
    return jsonify(error='Shortcode not found'), 404