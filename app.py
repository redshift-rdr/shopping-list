import datetime
import functions, config
from flask import Flask, render_template
from api import api

app = Flask(__name__)
app.register_blueprint(api)

functions.log(f'[INFO] application started at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

@app.route('/')
def home():
    return 'hello world'

if __name__ == "__main__":
    app.run('0.0.0.0', 5001)