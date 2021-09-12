from flaskr.tests.fixtures.user_fixtures import UsuarioFixture
from flaskr.modelos import Comentario, db
from flaskr.tests import fixtures


class ComentarioFixture(object):
    def __init__(self) -> None:
        self.default_texto = fixtures.RandomStringFixture()
        self.default_usuario = UsuarioFixture()

    def create(self):
        texto = self.default_texto.create()
        usuario = self.default_usuario.create()

        instance = Comentario(texto=texto, usuario=usuario.id)
        db.session.add(instance)
        db.session.commit()
        return instance
