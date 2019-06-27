from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models


@app.route('/')
def index_html():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
