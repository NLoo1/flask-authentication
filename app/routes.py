from flask import Blueprint, flash, redirect, render_template, request, jsonify, session

from app.forms import AddFeedbackForm, AddUserForm, LoginUserForm

from .models import Feedback, User, db

rts = Blueprint('rts', __name__)

@rts.route("/", methods=['GET'])
def home():
    if session.get('user_id', False):
        user = User.query.filter_by(id=session.get('user_id')).first()
        feedback = Feedback.query.all()
        return render_template('home.html', feedback=feedback, user=user)
    else:
        return redirect('/register')

@rts.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        flash('You are already logged in!')
        return redirect('/')
    form = AddUserForm()

    # Create new user
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data
        user = User.register(username=username,pwd=password,email=email,first_name=first_name,last_name=last_name)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        flash(f'User {username} added.')
        return redirect(f'/users/{user.username}')
    else:
        return render_template('register.html', form=form)
    
@rts.route('/login', methods=['GET','POST'])
def login():

    # Check if user is already logged in
    if session.get('user_id'):
        user = User.query.filter_by(id=session['user_id']).first()
        flash(f'You are currently logged in as {user.username}')
        return redirect('/')
    
    # Try to login a user, or return an error
    form = LoginUserForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        user = User.authenticate(username=username,pwd=password)
        if user:
            session['user_id'] = user.id
            return redirect('/')
        else:
            flash('Invalid credentials')
            return render_template('login.html', form=form)
    # Otherwise, render template
    else: 
        return render_template('login.html', form=form)

@rts.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have successfully logged out.')
    return redirect('/')

@rts.route('/users/<username>', methods=['GET'])
def user_info(username):
    user = User.query.filter_by(username=username).first()
    feedbacks = Feedback.query.filter_by(username=username).all()
    if user:
        return render_template('user.html', user=user, feedbacks=feedbacks)
    else: 
        flash("Cannot find this user!")
        return redirect('/')
    
@rts.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    # Is a user logged in?
    if session.get('user_id'):
        # Get the user by id
        user = User.query.filter_by(username=username).first()
        # Only the user being deleted should be able to delete their account
        # TODO: Add admin privileges to override this
        if user.id == session.get('user_id'): 
            Feedback.query.filter_by(username=username).delete()
            User.query.filter_by(username=username).delete()
            db.session.commit()
            session.pop('user_id')
            flash('User deleted.')
            return redirect("/")
        
@rts.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    # Is a user logged in?
    if session.get('user_id'):
        # Get the user by id
        user = User.query.filter_by(id=session['user_id']).first()
        # Check if user is correctly trying to add under their own username
        if user.id == session.get('user_id'): 
            form = AddFeedbackForm()
            if form.validate_on_submit():
                title = form.title.data
                content = form.content.data
                username = user.username
                feedback = Feedback(title=title,content=content,username=username)
                db.session.add(feedback)
                db.session.commit()
                flash('Feedback posted')
                return redirect(f'/users/{user.username}')
        # If another user tries to add feedback under another username
        else:
            flash('Unauthorized user.')
            return render_template('feedback.html', form=form)
    return render_template('feedback.html', form=form)
    
@rts.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    # Check if logged in
    if session.get('user_id'):
        user = User.query.filter_by(id=session['user_id']).first()
        # Check if correct user
        if user.id == session.get('user_id'): 
            form = AddFeedbackForm()
            feedback = Feedback.query.filter_by(id=feedback_id).first()
            # If posting:
            if form.validate_on_submit():
                feedback = Feedback.query.get(feedback_id)
                feedback.title = form.title.data
                feedback.content = form.content.data
                db.session.add(feedback)
                db.session.commit()
                flash('Feedback updated')
                return redirect(f'/users/{user.username}')
            # Else, get template to update relevant form
            else:
                # TODO: Get the form
                return render_template('update-feedback.html', form=form, feedback=feedback, user=user)
            
@rts.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    # Check if logged in
    if session.get('user_id'):
        user = User.query.filter_by(id=session['user_id']).first()
        # Check if correct user
        if user.id == session.get('user_id'): 
            Feedback.query.filter_by(id=feedback_id).delete()
            db.session.commit()
            flash('Post deleted.')
            return redirect('/')
        else: 
            flash("Unauthorized")
            return redirect('/')
    else:
        flash('You are not logged in!')
        return redirect('/register')

        

        
        

