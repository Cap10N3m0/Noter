from flask import Flask,render_template

def create_app():
    app = Flask("notes")
    app.config.from_mapping(DATABASE='notes')