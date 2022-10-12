from flask import Flask

app = Flask(__name__)

app.secret_key = "Llave ultra secreta"

app.config['UPLOAD_FOLDER'] = 'flask_app/static/img'