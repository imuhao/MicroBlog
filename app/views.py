from app import app
from flask import render_template, redirect, flash
from .forms import LoginFrom


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Smile'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title="MicroBlog",
                           user=user,
                           posts=posts)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.is_submitted():
        flash("Login requested for OpenID=" + form.openid.data + ",remember_me=" + str(form.remember_me.data))
        return redirect('/index')

    return render_template('login.html',
                           title="Sign In",
                           form=form,
                           providers=app.config["OPENID_PROVIDERS"]
                           )

