import unittest
from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user


from app import create_app
from app.forms import TodoForm , StudentForm , UploadForm
from app.firestore_service import get_users, get_todos ,put_todo  , get_user


from google.cloud import storage
from werkzeug.utils import secure_filename
from os import path
import  csv
import os

import firebase_admin
from firebase_admin import firestore

app = create_app()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('505.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET','POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form
    }

    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)

        flash('Tu tarea se creo con éxito!')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context)




@app.route('/activities', methods=['GET','POST'])
@login_required
def activities():
    user_ip = session.get('user_ip')
    username = current_user.id
    student_form = StudentForm()
    bandera = True
    estatus = 'Inscrito'
    
    
    user_doc1 = get_user(username)
    ap1_from_db = user_doc1.to_dict()['ap_mat']

    user_doc2 = get_user(username)
    ap2_from_db = user_doc2.to_dict()['ap_pat']
    
    
    context = {
        'user_ip': user_ip,
        'username': username,
        'student_form': student_form, 
        'status': estatus , 
        'ap1': ap1_from_db,
        'ap2': ap2_from_db

    }    

    var = 0
    if student_form.validate_on_submit() and var == 0 and bandera==True:
        var = + 1
        bandera=False
        estatus = 'Inscrito'
        flash('Te has inscrito a el programa exitosamente')
    else:
        flash('Ya te has inscrito')
    return render_template('activities.html', **context)



@app.route('/upload' , methods=['GET' ,'POST'])
@login_required
def upload():
    user_ip = session.get('user_ip')
    username = current_user.id
    upload_form = UploadForm()

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'upload_form': upload_form

    }
    
    folder_name = upload_form.Folder_name.data

    if upload_form.validate_on_submit():
            route_name = upload_form.photo.data
            filename = secure_filename(route_name.filename)
            if filename == '':
                flash('No file detected')
            else:    
                for r, d, f in os.walk("c:\\"):
                    for files in f:
                        if files == filename:
                            print (os.path.join(r,files))

                            bucket = "service_bucket_ddani"
                            file_name = os.path.join(r,files)
                            route2 = folder_name

                            storage_client = storage.Client()
                            bucket = storage_client.bucket(bucket)
                            blob = bucket.blob(route2)

                            blob.upload_from_filename(file_name)
                            redirect('upload')
                            flash('archivo subido')
                            break
    else:
        flash('Inserta a continuación tu documento')

    return render_template('upload.html', **context)