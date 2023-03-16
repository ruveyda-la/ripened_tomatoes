from flask_app.models.show import Show
from flask_app import app
from flask import render_template, redirect, request, session

@app.route('/dashboard')
def display_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    shows=Show.get_all_shows()
    print(shows)
    return render_template('dashboard.html', shows = shows)

@app.route('/show/form')
def display_form():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("create.html")

@app.route('/show/create', methods=['POST'])
def create_show():
    if 'user_id' not in session:
        return redirect('/')
    if not Show.validate_show(request.form):
        return redirect("/show/form")

    id=Show.save(request.form)
    return redirect(f'/show/{id}')

@app.route('/show/<int:id>')
def display_show_by_id(id):
    if 'user_id' not in session:
        return redirect('/')
    data={'id': id}
    return render_template("one_show.html",show=Show.get_show_by_id(data))

@app.route('/show/edit/<int:id>')
def display_edit_form(id):
    if 'user_id' not in session:
        return redirect('/')
    data={'id': id}
    
    return render_template("edit.html",show = Show.get_show_by_id(data))

@app.route('/show/edit/update', methods=['POST'])
def edit_show():
    if 'user_id' not in session:
        return redirect('/')
    Show.update_show(request.form)
    return redirect (f'/show/{request.form["id"]}')


# @app.route('/show/delete/<int:id>')

    



