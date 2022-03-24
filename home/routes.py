# The code above is the code that is run when the application is started. 
# 
# The first line imports the gettext function from the flask_babel module. 
# 
# The next two lines import the render_template and render_template_string functions from the flask
# module. 
# 
# The next two lines import the redirect, url_for, request, session, json, Markup, and flash functions
# from the flask module. 
# 
# The next two lines import the login_user and logout_user functions from the flask_login module.

from gettext import gettext
from flask import render_template, render_template_string, redirect, url_for, request, session, json, Markup, flash
from flask_login import LoginManager, login_user, UserMixin, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask_ldap3_login.forms import LDAPLoginForm
from app import login_manager, ldap_manager, babel, mail,db
from flask_mail import Message
import re
from . import home, functions, forms, apidesk



# Creating a form that will be used to create a notification.
# from .models import User
from .forms import CreateNotify
from .models import Notification


@home.route('/administrator',methods=["POST", "GET"])
def admin():
   # The CreateNotify class is a
   # form that is used to create a new notification.
    forms = CreateNotify()

   # Checking if the user is logged in or not. If not, it redirects the user to the login page.
    if not current_user or current_user.is_anonymous:
        return redirect(url_for('auth_ldap.login'))

    select_admin = current_user.data._store['memberOf']
    admin = False
    for i in select_admin:
        if '[memberOf]' in i:
            admin = True

    if admin == False:
        return redirect(url_for('home.home'))



  # if not

    # This code is retrieving the username LDAP (saMaccountName) of the current user.
    data_user = current_user.data._store['sAMAccountName']

  # This code is checking to see if the request method is a POST. If it is, it will run the code under
  # it, which is the code for the form.

    if request.method == "POST":
        # Determine si los datos del formulario son razonables
        # Si los datos en el formulario satisfacen completamente a todos los validadores, devuelva verdadero, de lo contrario devuelva falso
        if not forms.validate_on_submit():
          # The code above is the code that will be executed when the user clicks the "Submit" button.
            #Capture data to HTML forms
            author = data_user
            datatime_start = forms.datatime_start.data
            datatime_end = forms.datatime_end.data
            type = forms.type.data
            message = forms.message.data
            print("ERROR")
            print(author, datatime_start, datatime_end, type, message)
            return render_template('administrator.html', forms=forms)
        else:
            author = data_user
            datatime_start = forms.datatime_start.data
            datatime_end = forms.datatime_end.data
            type = forms.type.data
            message = forms.message.data
            notify = Notification(author=author,datatime_start=datatime_start,datatime_end=datatime_end,type=type,message=message)
            db.session.add(notify)
            db.session.commit()
            print(author, datatime_start, datatime_end, type, message)
            flash('OK')
            return render_template("administrator.html",forms=forms)


    elif request.method == 'GET':
        return render_template('administrator.html', forms=forms)

    # complementar middleware de función si es admin

    return render_template('administrator.html', forms=forms)


@home.route('/profile')
def profile():
# 1. If the user is not logged in, redirect them to the login page.
# 2. If the user is logged in, render the profile page.
    if not current_user or current_user.is_anonymous:
        return redirect(url_for('auth_ldap.login'))

    apidesk_user = current_user.data._store['cn']
    apidesk_email = current_user.data._store['mail']
    apidesk_phone = current_user.data._store['telephoneNumber']
    apidesk_department = current_user.data._store['department']
    apidesk_title = current_user.data._store['title']
    #apidesk_manager = current_user.data._store['manager']
    apidesk_sama = current_user.data._store['sAMAccountName']

    data_user_profile = apidesk.view_all_requests(apidesk_user)
    data_user_workstation = apidesk.view_asset(apidesk_sama)

    return render_template('profile.html', data_user_workstation=data_user_workstation , data_user_profile=data_user_profile, apidesk_user=apidesk_user, apidesk_email=apidesk_email, apidesk_phone=apidesk_phone, apidesk_department=apidesk_department, apidesk_title=apidesk_title)


@home.route('/status')
def status():
    if not current_user or current_user.is_anonymous:
        return redirect(url_for('auth_ldap.login'))

    return render_template('status.html')

@home.route('/support')
def support():
    # Redirect users who are not logged in.
    if not current_user or current_user.is_anonymous:
        return redirect(url_for('auth_ldap.login'))

    return render_template('support.html')

@home.route('/permissions', methods=['GET', 'POST'])
def permissions():
    # Redirect users who are not logged in.
    if not current_user or current_user.is_anonymous:
        return redirect(url_for('auth_ldap.login'))

    # data = ldap_manager.get_user_groups(dn=current_user.dn,group_search_dn='ou=RemoteAPP')
    data = current_user.data._store['memberOf']
    allowed = []
    for i in data:
        if 'RemoteAPP' in i:
            allowed.append(i)

    # toda esta logica se puede separar en clases o funciones con functions.py

    allowed = [s.replace(",[memberOf]", "") for s in allowed]
    allowed = [s.replace("CN=", "") for s in allowed]
    allowed = [re.sub(",OU=\w+", "", i) for i in allowed]

    manager = current_user.data._store['manager']
    manformat1 = re.search("CN=\w+ [A-Z]\w+", manager, re.IGNORECASE)
    manformat = re.search("CN=\w+ [A-Z]\w+", manager, re.IGNORECASE)
    manformat1 = manformat1.group(0)
    manformat = manformat.group(0)
    manformat = manformat.replace("CN=", '')
    manformat1 = manformat1.replace("CN=", '')
    manformat = manformat.replace(" ", "")
    manformat = manformat.lower() + ""



    return render_template('permissions.html', allowed=allowed)

@home.route('/')
def home():
    form = forms.CreateNotify
    # Redirect users who are not logged in.
    if not current_user or current_user.is_anonymous:
        return redirect(url_for('auth_ldap.login'))

    username= current_user.data._store['sAMAccountName']
    userid = functions.save_user_db(username)

    data = current_user.data._store['memberOf']
    allowed = []
    for i in data:
        if 'RemoteAPP' in i:
            allowed.append(i)

    # toda esta logica se puede separar en clases o funciones con functions.py

    allowed = [s.replace("", "") for s in allowed]
    allowed = [s.replace("CN=", "") for s in allowed]
    allowed = [re.sub(",OU=\w+", "", i) for i in allowed]

    #Realizamos export de todos los permisos
    #functions.save_all_permissions(allowed)

    functions.relationship_permissions(userid,allowed)

    allow_app = functions.only_allow(userid)
    notify = functions.view_notifications()


    # # User is logged in, so show them a page with their cn and dn.
    # template = """
    # <h1>Welcome: {{ current_user.data.cn }}</h1>
    # <h2>{{ current_user.dn }}</h2>
    # """
    return render_template('home.html', allow_app=allow_app, notify=notify)

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'es')
