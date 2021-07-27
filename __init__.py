from flask import Flask
from flask_bcrypt import Bcrypt

def create_app():
    app = Flask("notes")
    app.config.from_mapping(DATABASE='notes')

    from . import db
    db.init_app(app)

    from . import account
    app.register_blueprint(account.bp)
    
    return app