import os
from urllib.parse import urlencode
import pycurl
import atexit
import threading
import requests
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
app.config.from_object('config.ProductionConfig')
#app.config.from_object('config.DevelopmentConfig')
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

def request_task(url, json):
    requests.post(url, json)


def kirim_wa(url, json):
    threading.Thread(target=request_task, args=(url, json)).start()

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
                flash('NIP/NRP Pegawai '+form.nomor.data+' sudah ada, periksa kembali')
                return redirect(url_for('pegawai'))
            else:
                pegawai = Pegawai(name=form.name.data, nip=form.nip.data, hp=form.hp.data, jabatan=form.jabatan.data, pangkat=form.pangkat.data, foto=storage_filename, tmt_kp=form.tmt_kp.data, tmt_kgb=form.tmt_kgb.data, kp_next=kp, kgb_next=kgb)
                db.session.add(pegawai)
                db.session.commit()
                filepath = os.path.join(current_app.root_path, 'static/img/foto', storage_filename) 
                file.save(filepath)
                flash('Pegawai baru '+form.name.data+' telah ditambahkan')
                return redirect(url_for('pegawai'))
            
        else :
            kp = form.tmt_kp.data.replace(year=form.tmt_kp.data.year+4)
            kgb =form.tmt_kgb.data.replace(year=form.tmt_kgb.data.year+2)
            pegawai = Pegawai.query.filter_by(nomor=form.nomor.data).first()
            if pegawai is not None :
                flash('NIP/NRP Pegawai '+form.nomor.data+' sudah ada, periksa kembali')
                return redirect(url_for('pegawai'))
            else:
                pegawai = Pegawai(name=form.name.data, nomor=form.nomor.data, hp=form.hp.data, jabatan=form.jabatan.data, pangkat=form.pangkat.data, tmt_kp=form.tmt_kp.data, tmt_kgb=form.tmt_kgb.data, kp_next=kp, kgb_next=kgb)
                db.session.add(pegawai)
                db.session.commit()
                flash('Pegawai baru '+form.name.data+' telah ditambahkan, foto tidak ada.')
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
            flash('Data Pegawai '+form.name.data+' telah diubah')
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
            flash('Data Pegawai '+form.name.data+' telah diubah ')
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
    flash('Pegawai '+pegawai.name+' telah dihapus')
    return redirect(url_for('pegawai'))

@app.route('/kirim-pesan', methods=['GET', 'POST'])
def kirim_pesan():
    url = "http://ramadani.my.id:5050/waapi/sendImage"
    daftar = Pegawai.query.all()
    admin = Pengguna.query.all()
    pesan1 = []
    pesan2 = []
    for peg in daftar:
        dt = date.today()
        kp = peg.kp_next
        kgb = peg.kgb_next
        time1 = (kp - dt)
        time2 = (kgb - dt)
        dt1 = time1.total_seconds()
        dt2 = time2.total_seconds()
        delta1 = dt1/86400
        delta2 = dt2/86400
        times1 = str(int(delta1))
        times2 = str(int(delta2))
        
        if (30 <= delta1 <= 180):
            msg = '*INFORMASI KENAIKAN PANGKAT*'+os.linesep+os.linesep+'Pegawai atas nama '+peg.name+' ('+peg.nip+'), Kenaikan Pangkat selanjutnya pada '+peg.kp_next.strftime('%d-%m-%Y')+', '+times1+' hari lagi.'+os.linesep+'Mohon segera ditindaklanjuti. Abaikan jika sudah diproses.'+os.linesep+os.linesep+'Salam,'+os.linesep+os.linesep+'_Admin SIMPEL-KEPO PN Labuha_'+os.linesep+os.linesep+os.linesep+os.linesep+'*_catatan_* : _Pesan ini dikirim secara otomatis. Tidak perlu dibalas._'
            for a in admin:
                data = {
                    'to': a.hp,
                    'pesan': msg,
                    'imageurl': 'http://ramadani.my.id:5099/img/pic1.png',
                    'image_name': 'pic.png'
                }
                kirim_wa(url, json=data)
            pesan1.append(peg.id)
            flash('Ada Kenaikan Pangkat Pegawai atas nama '+peg.name+' pada '+peg.kp_next.strftime('%d-%m-%Y')+'. Silahkan ditindaklanjuti')

        if (1 <= delta2 <= 60):
            msg = '*INFORMASI KENAIKAN GAJI BERKALA*'+os.linesep+os.linesep+'Pegawai atas nama '+peg.name+' ('+peg.nip+'), Kenaikan Gaji Berkala selanjutnya pada '+peg.kgb_next.strftime('%d-%m-%Y')+', '+times2+' hari lagi.'+os.linesep+'Mohon segera ditindaklanjuti. Abaikan jika sudah diproses.'+os.linesep+os.linesep+'Salam,'+os.linesep+os.linesep+'_Admin SIMPEL-KEPO PN Labuha_'+os.linesep+os.linesep+os.linesep+os.linesep+'*_catatan_* : _Pesan ini dikirim secara otomatis. Tidak perlu dibalas._'
            for a in admin:
                data = {
                    'to': a.hp,
                    'pesan': msg,
                    'imageurl': 'http://ramadani.my.id:5099/img/pic1.png',
                    'image_name': 'pic.png'
                }
                kirim_wa(url, json=data)
            pesan2.append(peg.id)
            flash('Ada Kenaikan Gaji Berkala Pegawai atas nama '+peg.name+' dalam '+times2+' hari lagi. Silahkan ditindaklanjuti')
    
    if not (pesan1):
        flash('Tidak ada Kenaikan Pangkat 6 bulan kedepan.')

    if not (pesan2): 
        flash('Tidak ada Kenaikan Gaji Berkala 2 bulan kedepan.')

    return redirect(url_for('pegawai'))

@app.route('/cek-whatsapp', methods=['GET', 'POST'])
def po_check():
    url = "http://ramadani.my.id:5050/waapi/sendText"
    msg = "Ini ujicoba Server Whatsapp"
    data = {
        'to': '628113502605',
        'pesan': msg
    }
    kirim_wa(url, json=data)

@app.route('/kirim-whatsapp', methods=['GET', 'POST'])
def do_check():
    url = "http://ramadani.my.id:5050/waapi/sendImage"
    daftar = Pegawai.query.all()
    admin = Pengguna.query.all()
    for peg in daftar:
        dt = date.today()
        kp = peg.kp_next
        kgb = peg.kgb_next
        time1 = (kp - dt)
        time2 = (kgb - dt)
        dt1 = time1.total_seconds()
        dt2 = time2.total_seconds()
        delta1 = dt1/86400
        delta2 = dt2/86400
        times1 = str(int(delta1))
        times2 = str(int(delta2))

        if (30 <= delta1 <= 180):
            msg = '*INFORMASI KENAIKAN PANGKAT*'+os.linesep+os.linesep+'Pegawai atas nama '+peg.name+' ('+peg.nip+'), Kenaikan Pangkat selanjutnya pada '+peg.kp_next.strftime('%d-%m-%Y')+', '+times1+' hari lagi.'+os.linesep+'Mohon segera ditindaklanjuti. Abaikan jika sudah diproses.'+os.linesep+os.linesep+'Salam,'+os.linesep+os.linesep+'_Admin SIMPEL-KEPO PN Labuha_'+os.linesep+os.linesep+os.linesep+os.linesep+'*_catatan_* : _Pesan ini dikirim secara otomatis. Tidak perlu dibalas._'
            for a in admin:
                data = {
                    'to': a.hp,
                    'pesan': msg,
                    'imageurl': 'http://ramadani.my.id:5099/img/pic1.png',
                    'image_name': 'pic.png'
                }
                kirim_wa(url, json=data)
        
        if (1 <= delta2 <= 60):
            msg = '*INFORMASI KENAIKAN GAJI BERKALA*'+os.linesep+os.linesep+'Pegawai atas nama '+peg.name+' ('+peg.nip+'), Kenaikan Gaji Berkala selanjutnya pada '+peg.kgb_next.strftime('%d-%m-%Y')+', '+times2+' hari lagi.'+os.linesep+'Mohon segera ditindaklanjuti. Abaikan jika sudah diproses.'+os.linesep+os.linesep+'Salam,'+os.linesep+os.linesep+'_Admin SIMPEL-KEPO PN Labuha_'+os.linesep+os.linesep+os.linesep+os.linesep+'*_catatan_* : _Pesan ini dikirim secara otomatis. Tidak perlu dibalas._'
            for a in admin:
                data = {
                    'to': a.hp,
                    'pesan': msg,
                    'imageurl': 'http://ramadani.my.id:5099/img/pic1.png',
                    'image_name': 'pic.png'
                }
                kirim_wa(url, json=data)

    return redirect(url_for('pegawai'))

@app.route('/kirim-whatsapp-pegawai', methods=['GET', 'POST'])
def to_check():
    url = 'http://ramadani.my.id:5050/waapi/sendText'
    daftar = Pegawai.query.all()
    for peg in daftar:
        dt = date.today()
        kp = peg.kp_next
        kgb = peg.kgb_next
        time1 = (kp - dt)
        time2 = (kgb - dt)
        dt1 = time1.total_seconds()
        dt2 = time2.total_seconds()
        delta1 = dt1/86400
        delta2 = dt2/86400
        times1 = str(int(delta1))
        times2 = str(int(delta2))

        if (30 <= delta1 <= 180):
            msg = '*INFORMASI KENAIKAN PANGKAT*'+os.linesep+os.linesep+'Pegawai atas nama '+peg.name+' ('+peg.nip+'), Kenaikan Pangkat selanjutnya pada '+peg.kp_next.strftime('%d-%m-%Y')+', '+times1+' hari lagi.'+os.linesep+'Mohon segera ditindaklanjuti. Abaikan jika sudah diproses.'+os.linesep+os.linesep+'Salam,'+os.linesep+os.linesep+'_Admin SIMPEL-KEPO PN Labuha_'+os.linesep+os.linesep+os.linesep+os.linesep+'*_catatan_* : _Pesan ini dikirim secara otomatis. Tidak perlu dibalas._'
            data = {
                'to': peg.hp,
                'pesan': msg
            }
            kirim_wa(url, json=data)
            
        if (1 <= delta2 <= 60):
            msg = '*INFORMASI KENAIKAN GAJI BERKALA*'+os.linesep+os.linesep+'Pegawai atas nama '+peg.name+' ('+peg.nip+'), Kenaikan Gaji Berkala selanjutnya pada '+peg.kgb_next.strftime('%d-%m-%Y')+', '+times2+' hari lagi.'+os.linesep+'Mohon segera ditindaklanjuti. Abaikan jika sudah diproses.'+os.linesep+os.linesep+'Salam,'+os.linesep+os.linesep+'_Admin SIMPEL-KEPO PN Labuha_'+os.linesep+os.linesep+os.linesep+os.linesep+'*_catatan_* : _Pesan ini dikirim secara otomatis. Tidak perlu dibalas._'
            data = {
                'to': peg.hp,
                'pesan': msg
            }
            kirim_wa(url, json=data)
            
    return redirect(url_for('pegawai'))
            
@app.route('/kirim-notif/<id>', methods=['GET', 'POST'])
def kirim_notif(id):
    url = 'http://ramadani.my.id:5050/waapi/sendText'
    p = Pegawai.query.get_or_404(id)
    dt = date.today()
    kp = p.kp_next
    kgb = p.kgb_next
    time1 = (kp - dt)
    time2 = (kgb - dt)
    dt1 = time1.total_seconds()
    dt2 = time2.total_seconds()
    delta1 = dt1/86400
    delta2 = dt2/86400
    times1 = str(int(delta1))
    times2 = str(int(delta2))
    msg = '*INFORMASI*'+os.linesep+os.linesep+'Berikut informasi anda:'+os.linesep+os.linesep+'Nama :'+p.name+os.linesep+'NIP : '+p.nip+os.linesep+'Kenaikan Pangkat selanjutnya pada *'+p.kp_next.strftime('%d-%m-%Y')+'*, '+times1+' hari lagi'+os.linesep+'Kenaikan Gaji Berkala selanjutnya pada *'+p.kgb_next.strftime('%d-%m-%Y')+'*, '+times2+' hari lagi'+os.linesep+os.linesep+'Ingatkan kepada Sub Bagian Kepegawaian dan Ortala agar segera diproses.'+os.linesep+os.linesep+'Salam,'+os.linesep+os.linesep+'_Admin SIMPEL-KEPO PN Labuha_'+os.linesep+os.linesep+os.linesep+os.linesep+'*_catatan_* : _Pesan ini dikirim secara otomatis. Tidak perlu dibalas._'
    data = {
        'to': p.hp,
        'pesan': msg
    }
    kirim_wa(url, json=data)

    flash('Notififikasi Whatsapp kepada '+p.name+' telah dikirim!')
    return redirect(url_for('pegawai'))

### Pengguna
@app.route('/pengguna', methods=['GET', 'POST'])
@login_required
def user():

    daftar = Pengguna.query.all()
    daftar = enumerate(daftar, start=1)
    form = PenggunaForm()
    if form.validate_on_submit() :
        file = request.files['foto']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            pengguna = Pengguna.query.filter_by(name=form.name.data).first()
            if pengguna is not None :
                flash('Nama pengguna '+form.name.data+' sudah ada, periksa kembali')
                return redirect(url_for('user'))
            else:
                pengguna = Pengguna(name=form.name.data, email=form.email.data,
                                hp=form.hp.data, pegawai=form.pegawai.data,
                                password=form.name.data, foto=filename)
                db.session.add(pengguna)
                db.session.commit()
                filepath = os.path.join(current_app.root_path, 'static/img', filename) 
                file.save(filepath)
                flash('Pengguna baru "'+form.name.data+'" telah ditambahkan')
                return redirect(url_for('user'))
            
        else :
            pengguna = Pengguna.query.filter_by(name=form.name.data).first()
            if pengguna is not None :
                flash('Nama pengguna '+form.name.data+' sudah ada, periksa kembali')
                return redirect(url_for('user'))
            else:
                pengguna = Pengguna(name=form.name.data, email=form.email.data,
                                hp=form.hp.data, pegawai=form.pegawai.data,
                                password=form.name.data)
                db.session.add(pengguna)
                db.session.commit()
                flash('Pengguna baru "'+form.name.data+'" telah ditambahkan, tidak ada foto profil.')
                return redirect(url_for('user'))
        
    return render_template('pengguna.html', form=form, daftar=daftar, title='Pengguna')

@app.route('/pengguna/<id>', methods=['GET', 'POST'])
@login_required
def user_edit(id):

    pengguna = Pengguna.query.get_or_404(id)
    form = PenggunaForm(obj=pengguna)
    if form.validate_on_submit():
        file = request.files['foto']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            pengguna.name = form.name.data
            pengguna.email = form.email.data
            pengguna.hp = form.hp.data
            pengguna.pegawai = form.pegawai.data
            pengguna.foto = filename
            db.session.commit()
            filepath = os.path.join(current_app.root_path, 'static/img', filename) 
            file.save(filepath)
            flash('Data pengguna '+pengguna.name+' telah diubah')
            return redirect(url_for('user'))
        else:
            pengguna.name = form.name.data
            pengguna.email = form.email.data
            pengguna.hp = form.hp.data
            pengguna.pegawai = form.pegawai.data

            db.session.commit()
            flash('Data pengguna '+pengguna.name+' telah diubah')
            return redirect(url_for('user'))
    
    form.name.data = pengguna.name
    form.email.data = pengguna.email
    form.hp.data = pengguna.hp
    form.pegawai.data = pengguna.pegawai
    return render_template('pengguna-edit.html', pengguna=pengguna, form=form, title="Ubah Pengguna")

@app.route('/pengguna/<id>/hapus', methods=['GET', 'POST'])
@login_required
def user_del(id):
    pengguna = Pengguna.query.get_or_404(id)
    if pengguna.foto is not None :
        filepath = os.path.join(current_app.root_path, 'static/img', pengguna.foto)
        os.remove(filepath)
    db.session.delete(pengguna)
    db.session.commit()
    flash('Pengguna telah dihapus')

    return redirect(url_for('user'))

@app.route('/pengguna/<id>/ganti-password', methods=['GET', 'POST'])
@login_required
def user_password(id):
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