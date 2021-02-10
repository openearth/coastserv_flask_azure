import os
from flask import Flask
from flask_bcrypt import Bcrypt
from coastserv.config import Config
from flask_sqlalchemy import SQLAlchemy
import shutil
# from azure.storage.file import FileService
from netCDF4 import Dataset

bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app(config_class = Config):
    # file_service = FileService(account_name='coastservstorage',
    #                            account_key='HOBOcLV1nEDevDKfHMVq9N0TsgNrh4AXI2Qyxt4QAmvDi+oSUD9R6xnI8UEz7AVduzMill3+ymlNlj11jC58vw==')
    # generator = file_service.list_directories_and_files('static/FES')
    #
    #
    # for file_or_dir in generator:
    #     if file_or_dir.name.endswith('nc'):
    #         print(file_or_dir)
    #         file_service.get_file_to_path('static/FES', None, file_or_dir.name, 'out.nc')





    app = Flask(__name__)
    app.config.from_object(Config)
    #check if out directory exists, if so remove:
    out_fp = os.path.join(os.path.dirname(__file__), 'static', 'out')

    if os.path.exists(out_fp):
        shutil.rmtree(out_fp)
    os.mkdir(out_fp)

    bcrypt.init_app(app)
    db.init_app(app)
    
    from coastserv.main.routes import main
    from coastserv.requests.routes import requests
    
    app.register_blueprint(main)
    app.register_blueprint(requests)

    with app.app_context():
        if not os.path.exists('site.db'):
            db.create_all()
    
    return app