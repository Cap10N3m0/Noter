from flask import Blueprint,render_template, request, redirect, url_for,g
from . import db
from flask_bcrypt import Bcrypt

bp = Blueprint("notes", "notes")

@bp.route('/',methods=['POST','GET'])
def login():
    conn = db.get_db()
    bcrypt = Bcrypt()

    user_name = request.form.get['UserName']
    cursor = conn.cursor()
    cursor.execute(f"SELECT passwords,id FROM users WHERE user_name = {user_name}")
    if request.method=='POST':
        hashed = cursor.fetchall[0]
        u_id = cursor.fetchall[1]
        pd = request.form.get['Password']
        if bcrypt.check_password_hash(hashed,pd): 
            return 'Hello'
            #redirect(f'account/{u_id}/',302)            
        else:
            return render_template("login.html",info='Invalid Password')
    else:
        return render_template("login.html")
