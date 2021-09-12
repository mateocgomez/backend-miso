from flaskr.modelos import Usuario, db
from flaskr.tests import fixtures


class UsuarioFixture(object):
    def __init__(self) -> None:
        self.default_nombre = fixtures.RandomStringFixture()
        self.default_contrasena = fixtures.RandomStringFixture()

    def create(self):
        nombre = self.default_nombre.create()
        contrasena = self.default_contrasena.create()
        instance = Usuario(nombre=nombre, contrasena=contrasena)
        db.session.add(instance)
        db.session.commit()
        return instance
