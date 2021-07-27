from flask import Blueprint,render_template, request, redirect, url_for,g
from . import db
from flask_bcrypt import Bcrypt

bp = Blueprint("notes", "notes")
bcrypt = Bcrypt()

@bp.route('/',methods=['POST','GET'])
def login():
    conn = db.get_db()

    if request.method=='POST':
        user_name = request.form.get['UserName']
        cursor = conn.cursor()
        cursor.execute(f"SELECT passwords,id FROM users WHERE user_name = {user_name}")
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

@bp.route('/register',methods=['GET','POST'])
def register():
    conn = db.get_db()
    if request.method=='POST':
        user_name = request.form.get['UserName']
        pd = request.form.get['Password']
        pd_trial = request.form.get['PasswordTrial']
        if pd == pd_trial:
            hased_pd = bcrypt.generate_password_hash(pd).decode('utf-8')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_name,passwords) VALUES (%s, %s)",(user_name,hased_pd))
            return redirect(url_for('account.login'),302)
    else:
        return render_template("register.html")
    

