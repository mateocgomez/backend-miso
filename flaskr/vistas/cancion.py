from flaskr.modelos.modelos import Acceso
from flask import request
from ..modelos import db, Cancion, CancionSchema, Usuario, Album
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from sqlalchemy import or_
from sqlalchemy.sql.expression import case
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import fields


cancion_schema = CancionSchema()


@doc(description='Crear y Leer canciones', tags=['Canciones'])
class VistaCanciones(MethodResource, Resource):
    @jwt_required()
    @marshal_with(CancionSchema, code=201, description='Cancion creada')
    def post(self):
        nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
        id_usuario = get_jwt_identity()
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.canciones.append(nueva_cancion)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene una canción con dicho nombre',409

        return cancion_schema.dump(nueva_cancion)

    @jwt_required()
    @marshal_with(CancionSchema(many=True), code=200, description='Lista de canciones')
    def get(self):                        
        id_usuario = get_jwt_identity()
        Usuario.query.get_or_404(id_usuario)
        query = db.session.query(Cancion, case([(Cancion.usuario==id_usuario, True)], else_=False).label('pertenece'))\
            .join(Usuario).filter(or_(Usuario.id == id_usuario, Cancion.acceso == Acceso.PUBLICO))

        def dump(cancion, pertenece):
            cancion.pertenece = pertenece
            serialized = cancion_schema.dump(cancion)
            return serialized
        
        return [dump(canc, pertenece) for canc, pertenece in query]

@doc(description='Actualizar, Leer y Borrar cancion', tags=['Cancion'])
class VistaCancion(MethodResource, Resource):

    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion))

    def put(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        cancion.titulo = request.json.get("titulo",cancion.titulo)
        cancion.minutos = request.json.get("minutos",cancion.minutos)
        cancion.segundos = request.json.get("segundos",cancion.segundos)
        cancion.interprete = request.json.get("interprete",cancion.interprete)
        db.session.commit()
        return cancion_schema.dump(cancion)

    def delete(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        db.session.delete(cancion)
        db.session.commit()
        return '',204
        
    @jwt_required()
    def patch(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)

        id_usuario = get_jwt_identity()
        
        belongAlbums = cancion.albumes        
        
        if len(belongAlbums):
            canChange = False

            for album in belongAlbums:
                if album.usuario == id_usuario:                    
                    canChange = album.acceso == Acceso.PUBLICO
                    break
            
            if canChange: 
                acceso = request.json.get("acceso")

                if not acceso in Acceso._member_names_:
                    return { "mensajes": "{} no es parte de los valores disponibles de Acceso".format(acceso) }, 400

                cancion.acceso = acceso
                db.session.commit()
                return '',204

            else:
                return {"mensaje": "No puede cambiar el acceso de la cancíón."}, 400

        else:
            return {"mensaje": "No puede cambiar el acceso de la cancíón."}, 400


@doc(description='Leer las canciones de un album y asociar una cancion existente o nueva a un album', tags=['CancionesAlbum'])
class VistaCancionesAlbum(MethodResource, Resource):

    def post(self, id_album):
        album = Album.query.get_or_404(id_album)
        
        if "id_cancion" in request.json.keys():
            
            nueva_cancion = Cancion.query.get(request.json["id_cancion"])
            if nueva_cancion is not None:
                album.canciones.append(nueva_cancion)
                db.session.commit()
            else:
                return 'Canción errónea',404
        else: 
            nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.canciones.append(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)
       
    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [cancion_schema.dump(ca) for ca in album.canciones]
