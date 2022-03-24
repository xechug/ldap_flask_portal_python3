# The `auth_ldap` blueprint is created. 
# 
# The `auth_ldap` blueprint is added to the `app` object. 
# 
# The `auth_ldap` blueprint is registered on the `app` object.

from flask import Blueprint, render_template

auth = Blueprint('auth_ldap', __name__, template_folder='templates', static_folder='static')

from . import routes