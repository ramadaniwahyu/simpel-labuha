from datetime import datetime, date, time

from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declared_attr

from  app import db, login_manager


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    dibuat_pada = db.Column(db.DateTime, default=datetime.now)
    diubah_pada = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class Pengguna(Base, UserMixin):
    name = db.Column(db.String(60))
    password_hash = db.Column(db.String(128))
    email =  db.Column(db.String(100), nullable=False)
    pegawai_id = db.Column(db.Integer, db.ForeignKey('pegawai.id'))

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password  
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{}'.format(self.name)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Pengguna.query.get(int(user_id))

class Pegawai(Base):
    name = db.Column(db.String(100))
    nip = db.Column(db.String(60))
    foto = db.Column(db.String(200))
    jabatan_id = db.Column(db.Integer, db.ForeignKey('jabatan.id'))
    pangkat_id = db.Column(db.Integer, db.ForeignKey('pangkat.id'))
    tmt_kp = db.Column(db.Date)
    tmt_kgb = db.Column(db.Date)
    kp_next = db.Column(db.Date)
    kgb_next = db.Column(db.Date)
    pengguna = db.relationship('Pengguna', backref='pegawai')

    def __repr__(self):
        return '{}'.format(self.name)

class Jabatan(Base):
    name = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.Text)
    level = db.Column(db.Integer, nullable=False)
    pegawai = db.relationship('Pegawai', backref='jabatan')

    def __repr__(self):
        return '{}'.format(self.name)

class Pangkat(Base):
    name = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.Text)
    level = db.Column(db.Integer, nullable=False)
    pegawai = db.relationship('Pegawai', backref='pangkat')

    def __repr__(self):
        return '{}'.format(self.name)