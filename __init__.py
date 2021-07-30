from flask import Flask
from flask_bcrypt import Bcrypt

def create_app():
    app = Flask("notes")
    app.config.from_mapping(DATABASE='notes')
    app.config.from_mapping(SCRET = 'Cap10_N3M0_43v3r')
    app.secret_key = app.config['SCRET']

    from . import db
    db.init_app(app)

    from . import account
    app.register_blueprint(account.bp)

    from . import notes
    app.register_blueprint(notes.notes_url)

    return app