from flaskr.tests.fixtures.user_fixtures import UsuarioFixture
from flaskr.modelos import Album, db, Medio, Acceso
from flaskr.tests import fixtures


class AlbumFixture(object):
    def __init__(self) -> None:
        self.default_titulo = fixtures.RandomStringFixture()
        self.default_anio = fixtures.RandomStringOfNumbers(length=4)
        self.default_descripcion = fixtures.RandomStringFixture()
        self.default_medio = fixtures.ObjectFixture(Medio.DISCO)
        self.default_acceso = fixtures.ObjectFixture(Acceso.PRIVADO)
        self.default_usuario = UsuarioFixture()

    def create(self):
        titulo = self.default_titulo.create()
        anio = self.default_anio.create()
        descripcion = self.default_descripcion.create()
        medio = self.default_medio.create()
        acceso = self.default_acceso.create()
        usuario = self.default_usuario.create()

        instance = Album(titulo=titulo, anio=anio, descripcion=descripcion, medio=medio, acceso=acceso, usuario=usuario.id)
        db.session.add(instance)
        db.session.commit()
        return instance
