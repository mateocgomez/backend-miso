from flask import request
from ..modelos import db, Usuario, UsuarioSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from sqlalchemy import or_
from sqlalchemy.sql.expression import case
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs


usuario_schema = UsuarioSchema()


@doc(description='Crear nueva cuenta, cambiar contrasena y borrar cuenta', tags=['UsuarioManagement'])
class VistaSignIn(MethodResource, Resource):
    
    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity = nuevo_usuario.id)
        return {"mensaje":"usuario creado exitosamente", "token":token_de_acceso}


    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '',204


@doc(description='Iniciar sesion en Ionic', tags=['UsuarioLogin'])
class VistaLogIn(MethodResource, Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"], Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity = usuario.id)
            return {"mensaje":"Inicio de sesión exitoso", "token": token_de_acceso}
