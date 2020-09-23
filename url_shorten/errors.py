from flask import Blueprint,jsonify



short = Blueprint('short', __name__)
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