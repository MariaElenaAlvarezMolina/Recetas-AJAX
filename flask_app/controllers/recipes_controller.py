from flask import render_template, redirect, session, request, flash
from flask_app import app

from flask_app.models.users import User
from flask_app.models.recipes import Recipe

from werkzeug.utils import secure_filename
import os

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id": session['user_id']}
    
    user = User.get_by_id(formulario)

    return render_template('new_recipe.html', user=user)

@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')

    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')

    if 'image' not in request.files:
        flash('No seleccionó ninguna imagen', 'receta')
        return redirect('/new/recipe')

    image = request.files['image']

    if image.filename == '':
        flash('Nombre de imagen vacío', 'receta')
        return redirect('/new/recipe')

    nombre_imagen = secure_filename(image.filename)

    image.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen))

    formulario = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "date_made": request.form['date_made'],
        "under_30": int(request.form['under_30']),
        "user_id": request.form['user_id'],
        "image": nombre_imagen,
    }

    Recipe.save(formulario)
    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id": session['user_id']}
    
    user = User.get_by_id(formulario)

    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)

@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/')

    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['id'])

    Recipe.update(request.form)

    return redirect('/dashboard')

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id": id}
    Recipe.delete(formulario)

    return redirect('/dashboard')

@app.route('/view/recipe/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
        
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario)

    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('show_recipe.html', user=user, recipe=recipe)