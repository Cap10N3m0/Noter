from flask import Blueprint,render_template, request, redirect, url_for,g,session
from . import db
from flask_bcrypt import Bcrypt

bp = Blueprint("notes", "notes")
bcrypt = Bcrypt()

@bp.route('/',methods=['POST','GET'])
def login():
    conn = db.get_db()

    if request.method=='POST':
        user_name = request.form['UserName']
        cursor = conn.cursor()
        cursor.execute(f"SELECT passwords,id FROM users WHERE user_name = \'{user_name}\';")
        detail = cursor.fetchone()
        if not detail:
            return render_template("login.html",info='Invalid User')            

        else:
            hashed = detail[0]
            u_id = detail[1]
            pd = request.form['Password']

            if bcrypt.check_password_hash(hashed,pd): 
                session['u_id'] = u_id
                return redirect(url_for('notes_url.notes_u_id'),302)            
            else:
                return render_template("login.html", info='Invalid Password')

    elif request.method=='GET':
        return render_template("login.html")

@bp.route('/register',methods=['GET','POST'])
def register():
    conn = db.get_db()

    if request.method=='POST':
        user_name = request.form['UserName']
        pd = request.form['Password']
        pd_trial = request.form['PasswordTrial']
    
        if pd == pd_trial:
            hased_pd = bcrypt.generate_password_hash(pd).decode('utf-8')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_name, passwords) VALUES (%s,%s);", (user_name, hased_pd))
            conn.commit()
            return redirect(url_for('notes.login'),302)
        
        else:
            return render_template("register.html",info = 'Password in both column should be same')

    else:
        return render_template("register.html")
    

