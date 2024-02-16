from flask import Blueprint, flash, redirect, render_template, request, jsonify, session

from app.forms import AddFeedbackForm, AddUserForm, LoginUserForm

from .models import Feedback, User, db

rts = Blueprint('rts', __name__)

@rts.route("/", methods=['GET'])
def home():
    return redirect('/register')

@rts.route('/register', methods=['GET', 'POST'])
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
        session['user_id'] = user.id
        flash(f'User {username} added.')
        return redirect('/secret')
    else:
        return render_template('register.html', form=form)
    
@rts.route('/login', methods=['GET','POST'])
def login():
    if session['user_id']:
        user = User.query.filter_by(id=session['user_id']).first()
        flash(f'You are currently logged in as {user.username}')
        return redirect('/')
    form = LoginUserForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        user = User.authenticate(username=username,password=password)
        if user:
            session['user_id'] = user.id
            return redirect('/secret')
        else:
            form.username.errors['Invalid credentials']
            # flash('Invalid credentials')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@rts.route('/logout')
def logout():
    session.pop('user_id')
    flash('You have successfully logged out.')
    return redirect('/')

@rts.route('/users/<username>', methods=['GET'])
def user_info(username):
    user = User.query.filter_by(username=username).first()
    if user.id == session['user_id']:
        return render_template('user.html', user)
    elif user:
        return "You are not authorized to view this page."
    else: 
        return "Cannot find this user!"
    
@rts.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    # Is a user logged in?
    if session['user_id']:
        # Get the user by id
        user = User.query.filter_by(username=username).first()
        # TODO: Remove feedback
        User.query.filter_by(username=username).delete()
        session.pop('user_id')
        flash('User deleted.')
        return redirect("/")
        
@rts.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    # Is a user logged in?
    if session['user_id']:
        # Get the user by id
        user = User.query.filter_by(id=session['user_id']).first()
        form = AddFeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            # Keep this?
            username = username
            feedback = Feedback(title=title,content=content,username=username)
            db.session.add(feedback)
            db.session.commit()
    else:
        return render_template('add-feedback.html', form=form)
    
@rts.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    form = AddFeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback.query.get(feedback_id).first()
        feedback.title = form.title.data
        feedback.content = form.content.data
        # Update username?
        db.session.add(feedback)
        db.session.commit()
    else:
        feedback = Feedback.query.get(feedback_id).first()
        

        
        

