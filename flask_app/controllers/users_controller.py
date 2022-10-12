from flask import render_template, redirect, request, session, flash, jsonify
from flask_app import app

from flask_app.models.users import User
from flask_app.models.recipes import Recipe

#Importación de Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
#BCrypt permite la encriptación de contraseñas para evitar que se pueda acceder a ellas en la base de datos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.valida_usuario(request.form):
        return redirect('/')

    #Encriptación de la contraseña y guardado de la misma en la variable "pwd"
    pwd = bcrypt.generate_password_hash(request.form['password'])
#La encriptación se hará cuando se logre la validación del usuario

#El diccionario de datos que se recibe desde el formulario se debe volver a establecer para ingresar la contraseña en formato encriptado    
    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd #Incorporación en el diccionario del password encriptado
    }

    #Recepción del id del nuevo usuario
    id = User.save(formulario)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    #Verificar que el email exista en la base de datos
    user = User.get_by_email(request.form) #"user": Instancia con todos los datos del usuario

    if not user:
        """flash('Email no encontrado', 'login')
        return redirect('/')"""
        return jsonify(message="Email no encontrado")

    if not bcrypt.check_password_hash(user.password, request.form['password']): #Función de bcrypt verifica que la contraseña ingresada por el usuario coincida con la encriptada
        """flash('Password incorrecto', 'login')
        return redirect('/')"""
        return jsonify(message="Contraseña incorrecta")

    session['user_id'] = user.id
    """return redirect('/dashboard')"""
    return jsonify(message="correcto")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    #Recepción de la instancia de usuario en base a su id
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario)

    recipes = Recipe.get_all()
    
    return render_template('dashboard.html', user=user, recipes=recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')