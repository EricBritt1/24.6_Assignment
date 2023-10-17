from flask import Flask, request, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LogInForm, FeedbackForm, UpdateFeedbackForm

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///24_6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY _ECHO'] = True
app.config['SECRET_KEY'] = "DFGSDFGDSFGSDFG"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)


@app.route('/')
def redirect_to_register():

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    else:
        return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def show_register_form():
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(f'/users/{username}')

    else:
        return render_template('register-form.html', form=form)


@app.route('/list')
def show_user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def show_login_form():

    form = LogInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template('login-form.html', form=form)
    
    return render_template('login-form.html', form=form)


@app.route('/users/<username>')
def show_user_info(username):
    if 'username' in session and username == session['username']:
        user = User.query.get_or_404(username)
        feedbacks = user.feedbacks
        return render_template('user-information.html', user=user, feedbacks=feedbacks)
    elif 'username' in session and username != session['username']:
        actual_user = session['username']
        return redirect(f'/users/{actual_user}')
    else:
       return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def give_feedback(username):
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_user_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_user_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    elif username == session['username']:
        return render_template('add_feedback.html', form=form, username=username)
    else:
        return redirect('/')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_specific_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    form = UpdateFeedbackForm()
    username = feedback.username
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    elif username == session['username']:
        return render_template('update_feedback.html', form=form, feedback=feedback)
    else:
        return redirect('/')

@app.route('/feedback/<feedback_id>/delete', methods = ['POST'])
def delete_specific_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    username_in_session = session['username']
    if feedback.username == username_in_session:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{username_in_session}')
    else:
        return redirect('/')

@app.route('/users/<username>/delete', methods=['GET'])
def delete_account(username):
    username_in_session = session['username']
    if username == username_in_session:
        return render_template('confirm_deletion.html', username=username)
    else:
        return redirect(f'/users/{username_in_session}')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_account_confirmed(username):
    feedbacks = Feedback.query.filter_by(username=username)
    for feedback in feedbacks:
        specific_feedback = Feedback.query.get_or_404(feedback.id)
        db.session.delete(specific_feedback)
        db.session.commit()

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect('/')

@app.route('/logout')
def log_user_out():
    session.pop("username")

    return redirect('/login')



