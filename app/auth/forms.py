from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class LoginForm(FlaskForm):

    name = StringField('Nama Pengguna', validators=[DataRequired()])
    password = PasswordField('Kata Kunci', validators=[DataRequired()])
    submit = SubmitField('Masuk')