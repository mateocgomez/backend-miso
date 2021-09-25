import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema
import enum

db = SQLAlchemy()


class Medio(enum.Enum):
   DISCO = 1
   CASETE = 2
   CD = 3


class Acceso(enum.Enum):
   PRIVADO = 1
   PUBLICO = 2


albumes_canciones = db.Table('album_cancion',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key = True),
    db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key = True))

albumes_comentarios = db.Table('album_comentario',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key = True),
    db.Column('comentario_id', db.Integer, db.ForeignKey('comentario.id'), primary_key = True))


canciones_comentarios = db.Table('cancion_comentario',
    db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key = True),
    db.Column('comentario_id', db.Integer, db.ForeignKey('comentario.id'), primary_key = True))


class Cancion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(128))
    minutos = db.Column(db.Integer)
    segundos = db.Column(db.Integer)
    interprete = db.Column(db.String(128))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    acceso = db.Column(db.Enum(Acceso), default=Acceso.PRIVADO)
    albumes = db.relationship('Album', secondary = 'album_cancion', back_populates="canciones")
    comentarios = db.relationship('Comentario', secondary = 'cancion_comentario', back_populates="canciones")


class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(50), default=datetime.datetime.utcnow)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    albumes = db.relationship('Album', secondary = 'album_comentario', back_populates="comentarios")
    canciones = db.relationship('Cancion', secondary = 'cancion_comentario', back_populates="comentarios")

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(128))
    anio = db.Column(db.Integer)
    descripcion = db.Column(db.String(512))
    medio = db.Column(db.Enum(Medio))
    acceso = db.Column(db.Enum(Acceso), default=Acceso.PRIVADO)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    canciones = db.relationship('Cancion', secondary = 'album_cancion', back_populates="albumes")
    comentarios = db.relationship('Comentario', secondary = 'album_comentario', back_populates="albumes")


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    albumes = db.relationship('Album', cascade='all, delete, delete-orphan')
    comentarios = db.relationship('Comentario', cascade='all, delete, delete-orphan')
    canciones = db.relationship('Cancion', cascade='all, delete, delete-orphan')


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if isinstance(value, dict):
            return value
        return {"llave": value.name, "valor": value.value}

class CancionSchema(SQLAlchemyAutoSchema):
    acceso = EnumADiccionario(attribute=("acceso"))
    pertenece = fields.Boolean()
        
    class Meta:
         model = Cancion
         include_relationships = True
         load_instance = True

class AlbumSchema(SQLAlchemyAutoSchema):
    medio = EnumADiccionario(attribute=("medio"))
    acceso = EnumADiccionario(attribute=("acceso"))
    pertenece = fields.Boolean()

    class Meta:
         model = Album
         include_relationships = True
         load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True

class CancionPatchSchema(Schema):
    acceso = fields.String(load_default=Acceso.PRIVADO)

class AlbumPatchSchema(Schema):
    acceso = fields.String(load_default=Acceso.PRIVADO)


class ComentarioSchema(SQLAlchemyAutoSchema):
    usuario = fields.String()
    class Meta:
        model = Comentario
