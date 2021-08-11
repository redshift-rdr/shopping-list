import datetime
import functions, config
from flask import Flask, render_template
from api import api
from view import view

app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(view)

functions.log(f'[INFO] application started at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

if __name__ == "__main__":
    app.run('0.0.0.0', 5001)