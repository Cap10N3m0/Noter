from datetime import datetime
from flask import Blueprint, render_template, request, redirect, session, url_for, g
from . import db

notes_url = Blueprint("notes_url", __name__,url_prefix='/notes')

@notes_url.route('/')
def notes_u_id():
    conn = db.get_db()
    cursor = conn.cursor()

    if 'u_id' in session:
        cursor.execute(f'''SELECT n.id, n.title, n.created_on, SUBSTR(n.note,1,50)
         FROM notes n, users u, link_users lu 
         WHERE n.id = lu.n_id AND u.id = lu.u_id AND u.id = {session['u_id']} ORDER BY n.created_on DESC;''')
        nd = cursor.fetchall()
        conn.commit()
        if not nd:
            return render_template('user.html')
        else:
            return render_template('user.html',nd = nd)
    else:
        return redirect(url_for('notes.login'),302)    

@notes_url.route('/logout')
def logout():
    session.pop('u_id',None)
    return redirect(url_for('notes.login'),302)

def lu(title,note,created_on,u_id):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute(f'''SELECT id FROM notes WHERE title = \'{title}\'
    AND note = \'{note}\' AND created_on = \'{created_on}\';''')
    n_id = cursor.fetchone()
    cursor.execute('''INSERT INTO link_users (u_id,n_id) VALUES(%s,%s);''',(u_id,n_id))
    conn.commit()

@notes_url.route('/create', methods=['GET', 'POST'])
def create_note():
    conn = db.get_db()
    cursor = conn.cursor()
    
 
    if request.method == "GET":
        return render_template("create_note.html")
    
    elif request.method == "POST":
        note = request.form.get("note")
        u_id = session['u_id']
        title = request.form.get("title")
        tags = request.form.get('tags')
        created_on = datetime.today()

        cursor.execute('''INSERT INTO notes (title,note,tags,created_on) 
        VALUES (%s,%s,%s,%s);''',(title,note,tags,created_on)) 
        conn.commit()

        lu(title, note, created_on, u_id)
        return redirect(url_for('notes_url.notes_u_id'),302)

@notes_url.route('/<n_id>')
def display(n_id):
    if 'u_id' in session:
        conn = db.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''SELECT n.title,n.tags,n.note
         FROM notes n, users u, link_users lu 
         WHERE n.id = lu.n_id AND u.id = lu.u_id AND u.id = {session['u_id']} AND n.id={n_id};''')
        
        note = cursor.fetchone()
        title = note[0]
        tags = [i.strip() for i in note[1].split(',')]
        note_txt = note[2]
        conn.commit()

        return render_template('display_note.html',title=title,tags=tags,note=note_txt,id=n_id)

    else:
        return redirect(url_for('notes.login'),302)

@notes_url.route('/<n_id>/edit',methods=["GET", "POST",])
def edit_note(n_id):
    if 'u_id' in session:
        conn = db.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''SELECT n.title,n.tags,n.note
         FROM notes n, users u, link_users lu 
         WHERE n.id = lu.n_id AND u.id = lu.u_id AND u.id = {session['u_id']} AND n.id={n_id};''')
        note = cursor.fetchone()
        print
        if note is not None:
            if request.method == "GET":
                title,tags,note_txt = note
                return render_template('note_edit.html',title=title,tags=tags,note=note_txt,id=n_id)

            elif request.method =="POST":
                note = request.form.get("note")
                title = request.form.get("title")
                tags = request.form.get('tags')
                created_on = datetime.today()
                cursor.execute(
                    "update notes set title = %s, tags=%s,note=%s, created_on=%s where id=%s", (title, tags, note,created_on,n_id))
                conn.commit()


        return redirect(url_for('notes_url.notes_u_id'), 302)
    
    return redirect(url_for('notes.login'),302)


@notes_url.route('/search', methods=["GET", "POST", ])
def search():
    if 'u_id' in session:
        conn = db.get_db()
        cursor = conn.cursor()
        details = None
        if request.method == "POST":
            search_by = request.form.get("search")
            if search_by == 'tag':
                tag = request.form.get("sfor")
                tag = "%"+tag+"%"
                cursor.execute('''SELECT n.id, n.title, n.created_on, SUBSTR(n.note,1,50)
                FROM notes n, users u, link_users lu 
                WHERE n.id = lu.n_id AND u.id = lu.u_id AND u.id = %s AND n.tags LIKE %s;''', (session['u_id'],tag))
                details = cursor.fetchall()             
                print(details)  
            

            elif search_by == 'note':
                note = request.form.get("sfor")
                note = "%"+note+"%"
                cursor.execute('''SELECT n.id, n.title, n.created_on, SUBSTR(n.note,1,50)
                FROM notes n, users u, link_users lu 
                WHERE n.id = lu.n_id AND u.id = lu.u_id AND u.id = %s AND n.note LIKE %s;''', (session['u_id'], note))
                details = cursor.fetchall()
                print(details)
        conn.commit()
        return render_template('search.html', details=details)

    return redirect(url_for('notes.login'), 302)
    

