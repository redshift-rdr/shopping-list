from flask import Blueprint, request, render_template

view = Blueprint('view', __name__, template_folder='templates')

@view.route('/')
def home():
    return render_template("home.html")