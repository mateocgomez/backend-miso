from flaskr.tests.fixtures.comentario_fixture import ComentarioFixture
from flaskr.tests.fixtures.album_fixture import AlbumFixture
from flaskr.modelos import db


class AlbumComentarioFixture(object):
    def __init__(self) -> None:
        self.default_album = AlbumFixture()
        self.default_comentario = ComentarioFixture()

    def create(self):
        album = self.default_album.create()
        comentario = self.default_comentario.create()

        album.comentarios.append(comentario)
        db.session.commit()
        return comentario
