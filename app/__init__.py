import os
from datetime import date
from flask import Flask, render_template, redirect, url_for, send_from_directory, request, current_app, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__)

# Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('config.ProductionConfig')
app.config.from_object('config.DevelopmentConfig')
#app.config.from_object('config.TestingConfig')

Bootstrap(app)
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"
migrate = Migrate(app, db)

from app import models
from .models import Pengguna, Pegawai
from .forms import PegawaiForm
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    daftar = Pegawai.query.all()

    return render_template('index.html', daftar=daftar, title='Halaman Utama')

@app.route('/beranda')
@login_required
def dashboard():
    peg = Pegawai.query.get_or_404(1)
    form = PegawaiForm(obj=peg)

    return render_template('dashboard.html', peg=peg, form=form, title='Beranda')

@app.route('/<path:resource>')
def serveStaticResource(resource):
	return send_from_directory('static/', resource)

@app.route('/pegawai', methods=['GET', 'POST'])
@login_required
def pegawai():
    daftar = Pegawai.query.all()
    form = PegawaiForm()
    if form.validate_on_submit() :
        file = request.files['foto']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext_type = filename.split('.')[-1]
            file_name = form.nip.data
            storage_filename = str(file_name) + '.' +ext_type
            kp = form.tmt_kp.data.replace(year=form.tmt_kp.data.year+4)
            kgb =form.tmt_kgb.data.replace(year=form.tmt_kgb.data.year+2)
            pegawai = Pegawai.query.filter_by(nip=form.nip.data).first()
            if pegawai is not None :
                flash('NIP/NRP Pegawai sudah ada, periksa kembali')
                return redirect(url_for('pegawai'))
            else:
                pegawai = Pegawai(name=form.name.data, nip=form.nip.data, jabatan=form.jabatan.data, pangkat=form.pangkat.data, foto=storage_filename, tmt_kp=form.tmt_kp.data, tmt_kgb=form.tmt_kgb.data, kp_next=kp, kgb_next=kgb)
                db.session.add(pegawai)
                db.session.commit()
                filepath = os.path.join(current_app.root_path, 'static/img/foto', storage_filename) 
                file.save(filepath)
                flash('Pegawai baru telah ditambahkan')
                return redirect(url_for('pegawai'))
            
        else :
            kp = form.tmt_kp.data.replace(year=form.tmt_kp.data.year+4)
            kgb =form.tmt_kgb.data.replace(year=form.tmt_kgb.data.year+2)
            pegawai = Pegawai.query.filter_by(nomor=form.nomor.data).first()
            if pegawai is not None :
                flash('NIP/NRP Pegawai sudah ada, periksa kembali')
                return redirect(url_for('pegawai'))
            else:
                pegawai = Pegawai(name=form.name.data, nomor=form.nomor.data, jabatan=form.jabatan.data, pangkat=form.pangkat.data, tmt_kp=form.tmt_kp.data, tmt_kgb=form.tmt_kgb.data, kp_next=kp, kgb_next=kgb)
                db.session.add(pegawai)
                db.session.commit()
                flash('Pegawai baru telah ditambahkan, foto tidak ada.')
                return redirect(url_for('pegawai'))

    return render_template('pegawai.html', form=form, daftar=daftar, title='Daftar Pegawai')

@app.route('/pegawai/<id>', methods=['GET', 'POST'])
@login_required
def pegawai_edit(id):
    pegawai = Pegawai.query.get_or_404(id)
    form=PegawaiForm(obj=pegawai)
    if form.validate_on_submit() :
        file = request.files['foto']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext_type = filename.split('.')[-1]
            file_name = form.nip.data
            storage_filename = str(file_name) + '.' +ext_type
            pegawai.name = form.name.data
            pegawai.nip = form.nip.data
            pegawai.jabatan = form.jabatan.data
            pegawai.pangkat = form.pangkat.data
            pegawai.tmt_kp = form.tmt_kp.data
            pegawai.tmt_kgb = form.tmt_kgb.data
            pegawai.foto = storage_filename
            pegawai.kp_next = form.tmt_kp.data.replace(year=form.tmt_kp.data.year+4)
            pegawai.kgb_next = form.tmt_kgb.data.replace(year=form.tmt_kgb.data.year+2)
            db.session.commit()
            filepath = os.path.join(current_app.root_path, 'static/img/foto', storage_filename) 
            file.save(filepath)
            flash('Data Pegawai telah diubah'+ pegawai.kp_next)
            return redirect(url_for('pegawai_edit', id=pegawai.id))
        else :
            pegawai.name = form.name.data
            pegawai.nip = form.nip.data
            pegawai.jabatan = form.jabatan.data
            pegawai.pangkat = form.pangkat.data
            pegawai.tmt_kp = form.tmt_kp.data
            pegawai.tmt_kgb = form.tmt_kgb.data
            pegawai.kp_next = form.tmt_kp.data.replace(year=form.tmt_kp.data.year+4)
            pegawai.kgb_next = form.tmt_kgb.data.replace(year=form.tmt_kgb.data.year+2)
            db.session.commit()
            flash('Data Pegawai telah diubah '+ str(pegawai.kp_next))
            return redirect(url_for('pegawai'))

    form.name.data = pegawai.name
    form.nip.data = pegawai.nip
    form.jabatan.data = pegawai.jabatan
    form.pangkat.data = pegawai.pangkat
    form.tmt_kp.data = pegawai.tmt_kp
    form.tmt_kgb = pegawai.tmt_kgb

    return render_template('pegawai-edit.html', form=form, pegawai=pegawai, title='Ubah Pegawai')

@app.route('/pegawai/<id>/hapus', methods=['GET', 'POST'])
@login_required
def pegawai_del(id):
    pegawai = Pegawai.query.get_or_404(id)
    if pegawai.foto is not None :
        filepath = os.path.join(current_app.root_path, 'static/img/foto', pegawai.foto)
        os.remove(filepath)
    db.session.delete(pegawai)
    db.session.commit()
    flash('Pegawai telah dihapus')
    return redirect(url_for('pegawai'))


from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', title='Akses Ditolak'), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Halaman Tidak Ditemukan'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title='Server Internal Eror'), 500