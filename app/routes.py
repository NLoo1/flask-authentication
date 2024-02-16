from flask import Blueprint, flash, redirect, render_template, request, jsonify, session

from app.forms import AddUserForm

from .models import User, db

rts = Blueprint('rts', __name__)

@rts.route("/", methods=['GET'])
def home():
    return redirect('/register')

@rts.route('register', methods=['GET', 'POST'])
def register():
    form = AddUserForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data
        user = User.register(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
        db.session.add(user)
        db.session.commit()
        flash(f'User {username} added.')
        return redirect('/')
    else:
        return render_template('register.html', form=form)

@rts.route('/logout')
def logout():
    session.pop('user_id')
    flash('You have successfully logged out.')
    return redirect('/')