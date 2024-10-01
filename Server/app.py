import sys
import os

myDir = os.getcwd()
sys.path.append(myDir)
from pathlib import Path

path = Path(myDir)
a = str(path.parent.absolute())
sys.path.append(a)

from flask import Flask
from mongoengine import connect

from routes.model import model_bp
from routes.statistics import get_statistics_bp, put_statistics_bp
from routes.user import register_bp
from routes.token import login_bp

# Connect to MongoDB
connect('SafeDriveDataBase', host='localhost', port=27017)

app = Flask(__name__)


app.register_blueprint(register_bp, url_prefix='/api')
app.register_blueprint(login_bp, url_prefix='/api')
app.register_blueprint(get_statistics_bp, url_prefix='/api')
app.register_blueprint(put_statistics_bp, url_prefix='/api')
app.register_blueprint(model_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
