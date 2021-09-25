from flaskr.modelos.modelos import Acceso
from flask import request
from ..modelos import db, Cancion, Usuario, Album, Comentario, ComentarioSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from sqlalchemy import or_
from sqlalchemy.sql.expression import case
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import fields


comentario_schema = ComentarioSchema()


@doc(description='Permite al usuario crear un comentario para album', tags=['AlbumUsuario'])
class VistaComentarioAlbumUsuario(MethodResource, Resource):
    
    @jwt_required()
    def post(self, id_album):
        album = Album.query.get_or_404(id_album)
        usuario = get_jwt_identity()

        if album.acceso != Acceso.PUBLICO:
            return {"usuario": "El album no es publico. No puede agregar comentarios"}, 400

        comentario = Comentario(texto=request.json["texto"], usuario=usuario)
        album.comentarios.append(comentario)
        db.session.commit()
        return comentario_schema.dump(comentario)
    
    @jwt_required()
    def get(self, id_album):
        album = Album.query.get_or_404(id_album)

        if album.acceso != Acceso.PUBLICO:
            return {"usuario": "El album no es publico. No puede ver los comentarios"}, 400

        query = db.session.query(Comentario, Usuario).\
            join(Usuario).\
            join(Comentario.albumes).\
            filter(Album.acceso == Acceso.PUBLICO).\
            filter(Album.id == id_album)

        def dump(comentario, usuario):
            comentario.usuario = usuario.nombre
            serialized = comentario_schema.dump(comentario)
            return serialized

        return [dump(comentario, usuario) for comentario, usuario in query]


@doc(description='Permite al usuario crear un comentario para cancion', tags=['CancionUsuario'])
class VistaComentarioCancionUsuario(MethodResource, Resource):
    
    @jwt_required()
    def post(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        usuario = get_jwt_identity()

        if cancion.acceso != Acceso.PUBLICO:
            return {"usuario": "La canción no es pública. No puede agregar comentarios"}, 400

        comentario = Comentario(texto=request.json["texto"], usuario=usuario)
        cancion.comentarios.append(comentario)
        db.session.commit()
        return comentario_schema.dump(comentario)
    
    @jwt_required()
    def get(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)

        if cancion.acceso != Acceso.PUBLICO:
            return {"usuario": "La canción no es pública. No puede ver los comentarios"}, 400

        query = db.session.query(Comentario, Usuario).\
            join(Usuario).\
            join(Comentario.canciones).\
            filter(Cancion.acceso == Acceso.PUBLICO).\
            filter(Cancion.id == id_cancion)

        def dump(comentario, usuario):
            comentario.usuario = usuario.nombre
            serialized = comentario_schema.dump(comentario)
            return serialized

        return [dump(comentario, usuario) for comentario, usuario in query]
