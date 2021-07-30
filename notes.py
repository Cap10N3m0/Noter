from flask import Blueprint, render_template, request, redirect, session, url_for, g
from . import db

notes_url = Blueprint("notes_url", __name__,url_prefix='/notes')

@notes_url.route('/')
def notes_u_id():
    conn = db.get_db()
    cursor = conn.cursor()

    if 'u_id' in session:
        cursor.execute(f'''SELECT n.id, n.title, n.created_on, SUBSTR(n.note,1,7)
         FROM notes n, users u, link_users lu
         WHERE n.id = lu.note AND u.id = user_id AND u.id = {session['u_id']} ;''')
        nd = cursor.fetchall()
        if not nd:
            return render_template('user.html')
        else:
            render_template('user.html',nd = nd)
    else:
        return redirect(url_for('notes.login'),302)    

@notes_url.route('/logout')
def logout():
    session.pop('u_id',None)
    return redirect(url_for('notes.login'),302)

@notes_url.route('/create')
def create_note():
    pass