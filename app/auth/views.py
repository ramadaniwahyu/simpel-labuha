from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from ..models import Pengguna
from .forms import LoginForm
from .. import db


@auth.route('/masuk', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    next= request.args.get('next')
    form = LoginForm()
    if form.validate_on_submit():

        user = Pengguna.query.filter_by(name=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)

            if next :
                return redirect(next)
            else:
                return redirect(url_for('dashboard'))

        else:
            flash('Nama Pengguna dan/atau password salah.')

    return render_template('auth/login.html', form=form, title='Halaman Login')

@auth.route('/keluar')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('Anda telah berhasil keluar dari sistem.')

    # redirect to the login page
    return redirect(url_for('auth.login'))
