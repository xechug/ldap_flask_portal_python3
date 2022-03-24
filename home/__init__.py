from flask import Blueprint, render_template

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

from . import routes