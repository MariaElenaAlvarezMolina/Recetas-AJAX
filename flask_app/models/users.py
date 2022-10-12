from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def valida_usuario(formulario):
        es_valido = True

        if len(formulario['first_name']) < 2:
            flash('El Nombre debe tener al menos 2 caracteres', 'registro')
            es_valido = False

        if len(formulario['last_name']) < 2:
            flash('El Apellido debe tener al menos 2 caracteres', 'registro')
            es_valido = False

        if len(formulario['password']) < 6:
            flash('La Contraseña debe tener al menos 6 caracteres', 'registro')
            es_valido = False

        #Verificación de coincidencia de contraseñas (con campo "Confirmar Contraseña" en HTML)
        if formulario['password'] != formulario['confirm_password']:
            flash('Las Contraseñas no coinciden', 'registro')
            es_valido = False

        if not EMAIL_REGEX.match(formulario['email']):
            flash('Email inválido', 'registro')
            es_valido = False

        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('esquema_recetas').query_db(query, formulario)
        if len(results) >= 1:
            flash('Email registrado previamente', 'registro')
            es_valido = False

        return es_valido

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        return result

    #Verificación de existencia del email en la base de datos
    @classmethod
    def get_by_email(cls, formulario):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)

        if len(result) < 1: #Consulta si la lista dada por el query SELECT está vacía
            return False
        else:
            user = cls(result[0])
            return user

    #Recepción del usuario a partir de su id
    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        user = cls(result[0])
        return user