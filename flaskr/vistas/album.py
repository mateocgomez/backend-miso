from flaskr.modelos.modelos import Acceso
from flask import request
from ..modelos import db, Cancion, Usuario, Album, AlbumSchema, AlbumPatchSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from sqlalchemy import or_
from sqlalchemy.sql.expression import case
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import fields


album_schema = AlbumSchema()


@doc(description='Leer los albumes de una cancion', tags=['AlbumesCanciones'])
class VistaAlbumesCanciones(MethodResource, Resource):
    def get(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        return [album_schema.dump(al) for al in cancion.albumes]


@doc(description='Permite al usuario crear un album en su cuenta y tambien ver la lista de sus albumes y albumes publicos', tags=['AlbumUsuario'])
class VistaAlbumsUsuario(MethodResource, Resource):

    @jwt_required()
    @marshal_with(AlbumSchema(), code=200, description='Album creado')
    def post(self, id_usuario):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"], descripcion=request.json["descripcion"], medio=request.json["medio"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre',409

        return album_schema.dump(nuevo_album)

    @jwt_required()
    @marshal_with(AlbumSchema(many=True), code=200, description='Lista de albumes')
    def get(self, id_usuario):
        Usuario.query.get_or_404(id_usuario)
        query = db.session.query(Album, case([(Album.usuario==id_usuario, True)], else_=False).label('pertenece'))\
            .join(Usuario).filter(or_(Usuario.id == id_usuario, Album.acceso == Acceso.PUBLICO))
        
        def dump(album, pertenece):
            album.pertenece = pertenece
            serialized = album_schema.dump(album)
            return serialized
        return [dump(al, pertenece) for al, pertenece in query]


@doc(description='Actualizar, Leer y Borrar album', tags=['Album'])
class VistaAlbum(MethodResource, Resource):

    def get(self, id_album):
        return album_schema.dump(Album.query.get_or_404(id_album))

    def put(self, id_album):
        album = Album.query.get_or_404(id_album)
        album.titulo = request.json.get("titulo",album.titulo)
        album.anio = request.json.get("anio", album.anio)
        album.descripcion = request.json.get("descripcion", album.descripcion)
        album.medio = request.json.get("medio", album.medio)
        db.session.commit()
        return album_schema.dump(album)
    
    @jwt_required()
    def delete(self, id_album):
        album = Album.query.get_or_404(id_album)
        db.session.delete(album)
        db.session.commit()
        return '',204

    @doc(description='Permite cambiar el tipo de acceso a un album existente', tags=['Album'])
    @marshal_with(AlbumPatchSchema, code=204, description='Se actualizo correctamente')
    @marshal_with(AlbumPatchSchema, code=404, description='Album no existe')
    @marshal_with(AlbumPatchSchema, code=401, description='Usuario no autenticado')
    @jwt_required()
    def patch(self, id_album):
        album = Album.query.get_or_404(id_album)
        id_usuario = get_jwt_identity()

        if album.usuario != id_usuario:
            return {"usuario": "No puede cambiar el acceso del album."}, 400
        
        album.acceso = request.json.get("acceso", album.acceso)
        db.session.commit()
        return '',204

