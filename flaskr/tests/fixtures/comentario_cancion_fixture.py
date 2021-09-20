from flaskr.tests.fixtures.comentario_fixture import ComentarioFixture
from flaskr.tests.fixtures.cancion_fixture import CancionFixture
from flaskr.modelos import db


class CancionComentarioFixture(object):
    def __init__(self) -> None:
        self.default_cancion    = CancionFixture()
        self.default_comentario = ComentarioFixture()

    def create(self):
        cancion = self.default_cancion.create()
        comentario = self.default_comentario.create()

        cancion.comentarios.append(comentario)
        db.session.commit()
        return comentario
