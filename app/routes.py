from app import app
from flask import render_template
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User, dayPerformance
from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from flask_login import logout_user
from app import db
from app.forms import RegistrationForm, ProgressForm


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    form = ProgressForm()
    print(current_user.get_id())

    #individual numbers
    progress = dayPerformance.query.all()
    for value in progress:
        value.username = User.query.filter_by(id=value.user_id).first().username

    #sum of numbers
    users = User.query.all()
    for user in users:
        list_values = dayPerformance.query.filter_by(user_id=user.id)
        sum_values = 0
        for value in list_values:
            sum_values = sum_values + value.amount
        user.sum_values = sum_values


    if request.method == 'POST':
        if form.validate_on_submit():
            p = dayPerformance(amount=form.amount.data, user_id=current_user.get_id())
            print("data:")
            print(form.amount)
            print(type(form.amount))
            db.session.add(p)
            db.session.commit()
            print(current_user)
            progress = dayPerformance.query.all()
            return redirect('/login')
    return render_template("index.html", progress=progress, users=users, title='Home Page', form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)