from datetime import datetime, date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField, DateField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.widgets.html5 import DateInput, NumberInput

from flask_wtf.file import FileField, FileAllowed, FileRequired

from .models import Pegawai, Pengguna, Jabatan, Pangkat

class PenggunaForm(FlaskForm):
    name = StringField('Nama Pengguna', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    hp = StringField('Nomor WA (menggunakanan awalan 62)', validators=[DataRequired()])
    pegawai = QuerySelectField('Pegawai', query_factory=lambda: Pegawai.query.all(), get_label='name', allow_blank=True)
    submit = SubmitField('Simpan')

class PasswordForm(FlaskForm):
    password = PasswordField('Password Baru', validators=[DataRequired()])
    confirm_password = PasswordField('Konfirmasi Password Baru', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Ganti Password')

class PegawaiForm(FlaskForm):
    name = StringField('Nama Pegawai', validators=[DataRequired()])
    nip = IntegerField('NIP/NRP', validators=[DataRequired()])
    hp = IntegerField('Nomor WA (menggunakanan awalan 62)', validators=[DataRequired()])
    jabatan = QuerySelectField('Jabatan', query_factory=lambda: Jabatan.query.all(), get_label='name', allow_blank=True)
    pangkat = QuerySelectField('Pangkat', query_factory=lambda: Pangkat.query.all(), get_label='name', allow_blank=True)
    foto = FileField('Upload Foto', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'File gambar saja')])
    tmt_kp = DateField('TMT Kenaikan Pangkat (mm/dd/yyy)', widget=DateInput())
    tmt_kgb = DateField('TMT Kenaikan Gaji Berkala (mm/dd/yyy)', widget=DateInput())
    submit = SubmitField('Simpan')

class JabatanForm(FlaskForm):
    name = StringField('Nama Jabatan', validators=[DataRequired()])
    desc = TextAreaField('Keterangan')
    level = IntegerField('Level', widget=NumberInput(), validators=[DataRequired()])
    submit = SubmitField('Simpan')

class PangkatForm(FlaskForm):
    name = StringField('Nama Pangkat', validators=[DataRequired()])
    desc = TextAreaField('Keterangan')
    level = IntegerField('Level', widget=NumberInput(), validators=[DataRequired()])
    submit = SubmitField('Simpan')