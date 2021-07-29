from flask import Blueprint, render_template, request, redirect, url_for, g
from . import db

bp = Blueprint("notes", "notes")                                                                                                                                                                                                                                                                    