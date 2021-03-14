import os
from urllib.parse import urlencode
import pycurl
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, datetime
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
from .forms import PegawaiForm, PenggunaForm, PasswordForm
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def kirim_wa_kp(id):
    admin = Pengguna.query.all()
    p = Pegawai.query.get_or_404(id)
    for a in admin:
        msg = '*Mohon Perhatian*'+os.linesep+os.linesep+'Informasi Pegawai atas nama '+p.name+' ('+p.nip+'), Kenaikan Pangkat selanjutnya pada '+p.kp_next.strftime('%d-%m-%Y')+'.'+os.linesep+'Mohon segera ditindaklanjuti. Abaikan jika sudah diproses.'+os.linesep+os.linesep+'Salam,'+os.linesep+os.linesep+'_Admin SIMPEL-KEPO PN Labuha_'+os.linesep+os.linesep+os.linesep+os.linesep+'*_catatan_* : _Pesan ini dikirim secara otomatis. Tidak perlu dibalas._'
        crl = pycurl.Curl()
        crl.setopt(crl.URL, 'http://ramadani.my.id:5050/waapi/sendImage')
        json = {
            'to': a.hp,
            'pesan': msg,
            'imageurl': 'http://ramadani.my.id:5099/img/pic.png',
            'image_name': 'pic.png'
            }
        pf = urlencode(json)
        crl.setopt(crl.POSTFIELDS, pf)
        crl.perform()
        crl.close()

def kirim_wa_kgb(id):
    admin = Pengguna.query.all()
    p = Pegawai.query.get_or_404(id)
    for a in admin:
        msg = '*Mohon Perhatian*'+os.linesep+os.linesep+'Informasi Pegawai atas nama '+p.name+' ('+p.nip+'), Kenaikan Gaji Berkala selanjutnya pada '+p.kgb_next.strftime('%d-%m-%Y')+'.'+os.linesep+'Mohon segera ditindaklanjuti. Abaikan jika sudah diproses.'+os.linesep+os.linesep+'Salam,'+os.linesep+os.linesep+'_Admin SIMPEL-KEPO PN Labuha_'+os.linesep+os.linesep+os.linesep+os.linesep+'*_catatan_* : _Pesan ini dikirim secara otomatis. Tidak perlu dibalas._'
        crl = pycurl.Curl()
        crl.setopt(crl.URL, 'http://ramadani.my.id:5050/waapi/sendImage')
        json = {
            'to': a.hp,
            'pesan': msg,
            'imageurl': 'http://ramadani.my.id:5099/img/pic.png',
            'image_name': 'pic.png'
            }
        pf = urlencode(json)
        crl.setopt(crl.POSTFIELDS, pf)
        crl.perform()
        crl.close()

def do_check_kp():
    daftar = Pegawai.query.all()
    for peg in daftar:
        dt = date.today()
        kp = peg.kp_next
        time = (kp - dt)
        dt = time.total_seconds()
        delta = dt/86400
        times = str(int(delta))
        #kirim_wa_kp(peg.id)
        #kirim_wa_kgb(peg.id)

        if (delta == 180):
            kirim_wa_kp(peg.id)
        elif (delta == 150):
            kirim_wa_kp(peg.id)
        elif (delta == 120):
            kirim_wa_kp(peg.id)
        elif (delta == 90):
            kirim_wa_kp(peg.id)
        elif (delta == 60):
            kirim_wa_kp(peg.id)
        elif (delta == 55):
            kirim_wa_kp(peg.id)
        elif (delta == 50):
            kirim_wa_kp(peg.id)
        elif (delta == 45):
            kirim_wa_kp(peg.id)
        elif (delta == 40):
            kirim_wa_kp(peg.id)


def do_check_kgb():
    daftar = Pegawai.query.all()
    for peg in daftar:
        dt = date.today()
        kgb = peg.kgb_next
        time = (kgb - dt)
        dt = time.total_seconds()
        delta = dt/86400
        times = str(int(delta))
        #kirim_wa_kp(peg.id)
        #kirim_wa_kgb(peg.id)

        if (delta == 90):
            kirim_wa_kgb(peg.id)
        elif (delta == 80):
            kirim_wa_kgb(peg.id)
        elif (delta == 70):
            kirim_wa_kgb(peg.id)
        elif (delta == 60):
            kirim_wa_kgb(peg.id)
        elif (delta == 50):
            kirim_wa_kgb(peg.id)
        elif (delta == 40):
            kirim_wa_kgb(peg.id)
        elif (delta == 30):
            kirim_wa_kgb(peg.id)
        elif (delta == 20):
            kirim_wa_kgb(peg.id)
        elif (delta == 10):
            kirim_wa_kgb(peg.id)


'''
sched = BackgroundScheduler(daemon=True)
sched.add_job(do_check,'interval',minutes=1)
sched.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: sched.shutdown())
'''

@app.route('/')
def index():
    daftar = Pegawai.query.all()

    return render_template('index.html', daftar=daftar, title='Halaman Utama')

@app.route('/beranda', methods=['GET', 'POST'])
@login_required
def dashboard():

    return render_template('dashboard.html', title='Beranda')

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
                pegawai = Pegawai(name=form.name.data, nip=form.nip.data, hp=form.hp.data, jabatan=form.jabatan.data, pangkat=form.pangkat.data, foto=storage_filename, tmt_kp=form.tmt_kp.data, tmt_kgb=form.tmt_kgb.data, kp_next=kp, kgb_next=kgb)
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
                pegawai = Pegawai(name=form.name.data, nomor=form.nomor.data, hp=form.hp.data, jabatan=form.jabatan.data, pangkat=form.pangkat.data, tmt_kp=form.tmt_kp.data, tmt_kgb=form.tmt_kgb.data, kp_next=kp, kgb_next=kgb)
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
            pegawai.hp = form.hp.data
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
            pegawai.hp = form.hp.data
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
    form.hp.data = pegawai.hp
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

@app.route('/kirim-pesan', methods=['GET', 'POST'])
def kirim_pesan():
    do_check_kp()
    do_check_kgb()
    return redirect(url_for('pegawai'))

@app.route('/kirim-notif/<id>', methods=['GET', 'POST'])
def kirim_notif(id):
    p = Pegawai.query.get_or_404(id)
    msg = '*Mohon Perhatian*'+os.linesep+os.linesep+'Informasi Pegawai atas nama '+p.name+' ('+p.nip+'), Kenaikan Pangkat selanjutnya pada '+p.kp_next.strftime('%d-%m-%Y')+'.'+os.linesep+'Mohon segera ditindaklanjuti. Abaikan jika sudah diproses.'+os.linesep+os.linesep+'Salam,'+os.linesep+os.linesep+'_Admin SIMPEL-KEPO PN Labuha_'+os.linesep+os.linesep+os.linesep+os.linesep+'*_catatan_* : _Pesan ini dikirim secara otomatis. Tidak perlu dibalas._'
    crl = pycurl.Curl()
    crl.setopt(crl.URL, 'http://ramadani.my.id:5050/waapi/sendText')
    json = {
        'to': p.hp,
        'pesan': msg
        }
    pf = urlencode(json)
    crl.setopt(crl.POSTFIELDS, pf)
    crl.perform()
    crl.close()

    flash('Pesan Whatsapp telah dikirim!')
    return redirect(url_for('pegawai'))

### Pengguna
@app.route('/pengguna', methods=['GET', 'POST'])
@login_required
def user():

    daftar = Pengguna.query.all()
    daftar = enumerate(daftar, start=1)
    form = PenggunaForm()
    if form.validate_on_submit() :
        pengguna = Pengguna(name=form.name.data, email=form.email.data,
                            hp=form.hp.data, pegawai=form.pegawai.data,
                            password=form.name.data)
        db.session.add(pengguna)
        db.session.commit()
        flash('Pengguna baru telah ditambahkan')
        return redirect(url_for('user'))

    return render_template('pengguna.html', form=form, daftar=daftar, title='Pengguna')

@app.route('/pengguna/<id>', methods=['GET', 'POST'])
@login_required
def user_edit(id):

    pengguna = Pengguna.query.get_or_404(id)
    form = PenggunaForm(obj=pengguna)
    if form.validate_on_submit():
        pengguna.name = form.name.data
        pengguna.email = form.email.data
        pengguna.hp = form.hp.data
        pengguna.pegawai = form.pegawai.data

        db.session.commit()
        flash('Data pengguna telah diubah')
        return redirect(url_for('user'))
    
    form.name.data = pengguna.name
    form.email.data = pengguna.email
    form.hp.data = pengguna.hp
    form.pegawai.data = pengguna.pegawai
    return render_template('pengguna-edit.html', pengguna=pengguna, form=form, title="Ubah Pengguna")

@app.route('/pengguna/<id>/hapus', methods=['GET', 'POST'])
@login_required
def user_del(id):
    check_admin()
    pengguna = Pengguna.query.get_or_404(id)
    db.session.delete(pengguna)
    db.session.commit()
    flash('Pengguna telah dihapus')

    return redirect(url_for('user'))

@app.route('/pengguna/<id>/ganti-password', methods=['GET', 'POST'])
@login_required
def user_password(id):
    check_admin()
    pengguna = Pengguna.query.get_or_404(id)
    form = PasswordForm(obj=pengguna)
    if form.validate_on_submit():
        pengguna.password = form.password.data
        db.session.commit()
        flash('Password telah diganti')
        return redirect(url_for('user_edit', id=pengguna.id))
    
    return render_template('ganti-password.html', form=form, pengguna=pengguna, title='Ganti Password')
### End of Pengguna
    
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