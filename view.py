import db
from flask import Blueprint, request, render_template

view = Blueprint('view', __name__, template_folder='templates')

@view.route('/')
def current():
    current_list = db.get_current_list()

    return render_template("current_list.html", current_list=current_list)