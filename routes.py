# The `auth` blueprint is defined in the `__init__.py` file of the `app/auth` directory. 
# 
# The `auth` blueprint is registered with the `app` object in the `__init__.py` file of the `app`
# directory. 
# 
# The `auth` blueprint has a `url_prefix` of `/auth`. 
# 
# The `auth` blueprint has a `template_folder` of `templates`. 
# 
# The `auth` blueprint has a `static_folder` of `static
from flask import render_template, render_template_string, redirect, url_for, request, session
from flask_login import LoginManager, login_user, UserMixin, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask_ldap3_login.forms import LDAPLoginForm
from app import login_manager, ldap_manager, babel
from . import auth
from .models import User

# Create a variable save data user parametres in array
users = {}

# Assign route to login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # The user is logged in if they're already logged in, or if they're successfully logged in via
    # LDAP.
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    else:

        # Instantiate a LDAPLoginForm which has a validator to check if the user
        # exists in LDAP.
        form = LDAPLoginForm()

        if form.validate_on_submit():
            # Successfully logged in, We can now access the saved user object
            # via form.user.
            login_user(form.user)  # Tell flask-login to log them in.
            return redirect('/')  # Send them home
        return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
  # This is a function that will log out the user and redirect them to the home page.
    logout_user()
    return redirect(url_for('home.home'))


@login_manager.user_loader
def load_user(id):
 # This is a function that takes in an id and returns the user associated with that id.
    if id in users:
        return users[id]
    return None

@ldap_manager.save_user
def save_user(dn, username, data, memberships):
# The above code is creating a user object and adding it to the users dictionary.
    user = User(dn, username, data)
    users[dn] = user
    return user

@babel.localeselector
def get_locale():
# This is a function that will return the language that the user is using.
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'es')

