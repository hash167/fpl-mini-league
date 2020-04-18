from flask import Flask
from src.api.main import index_blueprint

application = Flask(__name__)
application.register_blueprint(index_blueprint)