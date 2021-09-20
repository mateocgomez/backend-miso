from flaskr.tests.fixtures.user_fixtures import UsuarioFixture
from flaskr.modelos import Cancion, db, Acceso
from flaskr.tests import fixtures


class CancionFixture(object):
    def __init__(self) -> None:
        self.default_titulo     = fixtures.RandomStringFixture()
        self.default_minutos    = fixtures.ObjectFixture(3)
        self.default_segundos   = fixtures.ObjectFixture(3)
        self.default_interprete = fixtures.RandomStringFixture()
        self.default_acceso     = fixtures.ObjectFixture(Acceso.PRIVADO)
        self.default_usuario    = UsuarioFixture()

    def create(self):
        titulo = self.default_titulo.create()
        minutos = self.default_minutos.create()
        segundos = self.default_segundos.create()        
        interprete = self.default_interprete.create()
        usuario = self.default_usuario.create()
        acceso = self.default_acceso.create()

        instance = Cancion(titulo=titulo, minutos=minutos, segundos=segundos, interprete=interprete, acceso=acceso, usuario=usuario.id)
        db.session.add(instance)
        db.session.commit()
        return instance
