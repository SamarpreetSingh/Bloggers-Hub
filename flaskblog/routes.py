from flask import render_template, url_for, redirect, flash
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt

posts = [
    {
        'author': 'Samar',
        'title': "Blog Post 1",
        'content': "This is my first blog post",
        'date_posted': "April, 2020"
    },
    {
        'author': 'Jon snow',
        'title': "Blog Post 2",
        'content': "This is my first blog post",
        'date_posted': "April, 2021"
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title="home")


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, password=hash_pw, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully! You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("Logged In Successfully", "success")
            return redirect('/')
        else:
            flash("Login Failed! Check username and password.", "danger")
    return render_template('login.html', title="Login", form=form)
