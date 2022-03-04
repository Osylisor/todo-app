from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from App.models import Todo
from . import db


views = Blueprint('views', __name__)


@views.route('/home', methods = ['GET', 'POST'])
@login_required
def home():

    if(request.method == 'POST'):

        todo_data = request.form.get('todo')

        try:
            if(todo_data == ''):
                flash("This text box can't be left out empty", category='error')
            else:
                todo = Todo(data = todo_data, user_id = current_user.id)
                db.session.add(todo)
                db.session.commit()
        except:

            return "<h1>Oops, looks like this data could not be added to the database</h1>"



    return render_template('home.html', users = current_user)



@views.route('/delete/<int:id>')
@login_required
def delete(id):

    todo_to_delete = Todo.query.get(id)

    if(todo_to_delete):


        if(todo_to_delete.user_id == current_user.id):
            db.session.delete(todo_to_delete)
            db.session.commit()
    else:

        return "<h1>Oops, could not find this item in the data base</h1>"

    return redirect(url_for('views.home'))


@views.route('/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit(id):

    todo_to_edit = Todo.query.get(id)

    if(request.method == 'POST'):

        new_todo_task = request.form.get('todo')
        


        if(todo_to_edit.user_id == current_user.id):
            todo_to_edit.data = new_todo_task
            db.session.commit()
            return redirect(url_for('views.home'))
          

    return render_template('Edit.html', task = todo_to_edit)
