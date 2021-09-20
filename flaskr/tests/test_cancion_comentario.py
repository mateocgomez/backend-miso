import json
from flaskr.tests.fixtures.cancion_fixture import CancionFixture
from flaskr.tests.fixtures.cancion_fixture import CancionFixture
from flaskr.tests.fixtures.comentario_cancion_fixture import CancionComentarioFixture
from flaskr.tests.fixtures.user_fixtures import UsuarioFixture
from flaskr.modelos import Acceso
from flaskr.tests import BaseCase, fixtures


class TestCancionComentario(BaseCase):
    def test_given_existing_user_when_add_comment_to_invalid_cancion_then_fail(self):
        """
        Asserts un usuario solo puede agregar comentarios a canciones existentes
        """
        # Arrange
        user = UsuarioFixture().create()
        
        cancion_fixture = CancionFixture()
        cancion_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PRIVADO)
        cancion = cancion_fixture.create()
        
        comentario_data = {
            "texto": "Este es un comentario"
        }

        # Act
        response = self.run_authenticated(user, 'post', f'/cancion/{cancion.id+1}/comentarios', data=json.dumps(comentario_data))

        # Assert
        self.assertEqual(404, response.status_code)

    def test_given_existing_user_when_add_comment_to_private_cancion_then_fail(self):
        """
        Asserts un usuario no puede agregar un comentario a un album privado
        """
        # Arrange
        user = UsuarioFixture().create()
        
        cancion_fixture = CancionFixture()
        cancion_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PRIVADO)
        cancion = cancion_fixture.create()
        
        comentario_data = {
            "texto": "Este es un comentario"
        }

        # Act
        response = self.run_authenticated(user, 'post', f'/cancion/{cancion.id}/comentarios', data=json.dumps(comentario_data))

        # Assert
        self.assertEqual(400, response.status_code)

    def test_given_existing_user_when_add_comment_to_public_cancion_then_success(self):
        """
        Asserts un usuario puede ver agregar un comenario a un album publico
        """
        # Arrange
        user = UsuarioFixture().create()
        
        cancion_fixture = CancionFixture()
        cancion_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PUBLICO)
        cancion = cancion_fixture.create()
        
        comentario_data = {
            "texto": "Este es un comentario"
        }

        # Act
        response = self.run_authenticated(user, 'post', f'/cancion/{cancion.id}/comentarios', data=json.dumps(comentario_data))
        comentario = response.json
        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(comentario['texto'], comentario_data['texto'])

    def test_given_existing_user_when_list_comment_of_private_cancion_then_fail(self):
        """
        Asserts un usuario no puede ver la lista de comentarios de un album privado
        """
        # Arrange
        user = UsuarioFixture().create()
        
        cancion_fixture = CancionFixture()
        cancion_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PRIVADO)
        cancion = cancion_fixture.create()
        
        # Act
        response = self.run_authenticated(user, 'get', f'/cancion/{cancion.id}/comentarios')

        # Assert
        self.assertEqual(400, response.status_code)

    def test_given_existing_user_when_list_comments_of_public_cancion_then_success(self):
        """
        Asserts un usuario puede ver su lista de comentarios de un album
        """
        # Arrange
        user = UsuarioFixture().create()
        
        cancion_fixture = CancionFixture()
        cancion_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PUBLICO)
        cancion = cancion_fixture.create()

        cancion_comentario_fixture = CancionComentarioFixture()
        cancion_comentario_fixture.default_cancion = fixtures.ObjectFixture(cancion) # comentarios para solo para el album creado previamente

        primer_comentario = cancion_comentario_fixture.create()
        segundo_comentario = cancion_comentario_fixture.create()
        tercer_comentario = cancion_comentario_fixture.create()
        
        # Act
        response = self.run_authenticated(user, 'get', f'/cancion/{cancion.id}/comentarios')
        comentarios = response.json
        
        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(comentarios), 3)
        self.assertTrue(any(comentario['id'] == primer_comentario.id for comentario in comentarios))
        self.assertTrue(any(comentario['usuario'] == primer_comentario.usuario for comentario in comentarios))
        self.assertTrue(any(comentario['id'] == segundo_comentario.id for comentario in comentarios))
        self.assertTrue(any(comentario['usuario'] == segundo_comentario.usuario for comentario in comentarios))
        self.assertTrue(any(comentario['id'] == tercer_comentario.id for comentario in comentarios))
        self.assertTrue(any(comentario['usuario'] == tercer_comentario.usuario for comentario in comentarios))

    def test_given_existing_user_when_list_comments_of_public_cancion_then_see_comments_belong_given_cancion_success(self):
        """
        Asserts un usuario puede ver la lista de comentarios de un album si es que existen
        """
        # Arrange
        user = UsuarioFixture().create()
        
        cancion_fixture = CancionFixture()
        cancion_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PUBLICO)
        cancion = cancion_fixture.create()

        cancion_sin_comentarios = cancion_fixture.create()

        cancion_comentario_fixture = CancionComentarioFixture()
        cancion_comentario_fixture.default_cancion = fixtures.ObjectFixture(cancion) # comentarios para solo para el primer album creado
        # comentario para el primer album
        cancion_comentario_fixture.create()        
        
        # Act
        response = self.run_authenticated(user, 'get', f'/cancion/{cancion_sin_comentarios.id}/comentarios')
        comentarios = response.json
        
        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(comentarios), 0)

    def test_given_existing_user_when_list_comments_of_public_cancion_then_see_comments_belong_given_albums_success(self):
        """
        Asserts un usuario puede ver la lista de comentarios de mas de un album publico
        """
        # Arrange
        user = UsuarioFixture().create()
        
        cancion_fixture = CancionFixture()
        cancion_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PUBLICO)
        primer_cancion = cancion_fixture.create()
        segundo_cancion = cancion_fixture.create()

        cancion_comentario_fixture = CancionComentarioFixture()
        cancion_comentario_fixture.default_cancion = fixtures.ObjectFixture(primer_cancion) 
        # dos comentarios para el primer album
        cancion_comentario_fixture.create()
        cancion_comentario_fixture.create()
        
        cancion_comentario_fixture.default_cancion = fixtures.ObjectFixture(segundo_cancion) 
        # un comentario para el segundo album
        cancion_comentario_fixture.create()

        # Act
        response_comentarios_primer_cancion = self.run_authenticated(user, 'get', f'/cancion/{primer_cancion.id}/comentarios')
        comentarios_primer_cancion = response_comentarios_primer_cancion.json
        
        response_comentarios_segundo_cancion = self.run_authenticated(user, 'get', f'/cancion/{segundo_cancion.id}/comentarios')
        comentarios_segundo_cancion = response_comentarios_segundo_cancion.json
        
        # Assert
        self.assertEqual(200, response_comentarios_primer_cancion.status_code)
        self.assertEqual(200, response_comentarios_segundo_cancion.status_code)
        self.assertEqual(len(comentarios_primer_cancion), 2)
        self.assertEqual(len(comentarios_segundo_cancion), 1)
