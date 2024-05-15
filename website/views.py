from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort
from flask_login import login_required, current_user
from .models import Note
from . import db
import json 
import string, random

characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
#blueprint for flask app
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) #decorator
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note') #retrieves note from html form
        color = request.form.get('color')
        if len(note) < 2:
            flash('Note is too short', category='error')
        else:
            # new_note = Note(data=note, user_id=current_user.id)
            new_note = Note(data=note, user_id=current_user.id, color=color)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    
    return render_template("home.html", user=current_user) # allows you to reference current user and check if it is authenticated

@views.route('/update-note-color/<int:note_id>/<string:color>', methods=['POST'])
@login_required
def update_note_color(note_id, color):
    note = Note.query.get_or_404(note_id)
    
    # checking if the note belongs to the current user
    if note.user_id != current_user.id:
        abort(403)
    
    # update note color
    note.color = color
    db.session.commit()
    flash('Note color updated successfully!', category='success')
    
    return redirect(url_for('views.home'))


# @views.route('/edit-note/<int:note_id>', methods=['GET', 'POST'])
# @login_required
# def edit_note(note_id):
#     note = Note.query.get_or_404(note_id)
    
#     if request.method == 'POST':
#         note.data = request.form.get('data')
#         note.color = request.form.get('color') #Updating the color information
#         db.session.commit()
#         flash('Note updated successfully!', category='success')
#         return redirect(url_for('views.home'))
#     return render_template('edit_note.html', note=note)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note Deleted!', category='success')
        
    return jsonify({})

# Password generation 
@views.route('/popup')
def popup():
    return render_template("popup.html") 

def signup():
    password = request.args.get('password')
    return render_template('signup.html', password=password)

@views.route('/generate-password', methods=['GET', 'POST'])
def generate_password():
    if request.method == 'POST':
        password_length = int(request.form['password_length'])
    else:
        password_length = int(request.args.get('password_length'))
    random.shuffle(characters)
    password = "".join(random.choices(characters, k=password_length))
    return render_template('popup.html', password=password)
    # if password:
    #     return redirect(url_for('auth.sign_up', password=password))
    # else:
    #     return  render_template('popup.html', password=password)    

@views.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
       password_length = int(request.form['password_length'])
       password, error = generate_password(password_length)
       if password:
           return render_template('popup.html', password=password, error=None)
       else:
           return render_template('popup.html', password=None, error=error)
   else:
        return render_template('popup.html', password=None, error=None)

@views.route('/regenerate',methods=['POST'])
def regenerate():
    return generate_password()

