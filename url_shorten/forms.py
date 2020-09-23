from flask_wtf import FlaskForm
import wtforms_json
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL,Length,Optional,Regexp

wtforms_json.init()
class UrlShortenForm(FlaskForm):
    original_url = StringField('LongUrl' , validators=[DataRequired(),URL(message='Must be a valid URL')])
    short_url = StringField('shortcode', validators=[Optional(),
                                                     Regexp('^\w+$', message="Short-code must contain only letters numbers or underscore"),
                                                     Length(min=6,max=6, message=('Short-code must be 6 chars'))])
    submit = SubmitField("Submit")

    def save_url(self, url):
        self.populate_obj(url)
        if not "http" in url.original_url:
            url.original_url = "https://" + url.original_url
        if not "." in url.original_url:
            url.original_url = url.original_url + ".com/"
        return url
