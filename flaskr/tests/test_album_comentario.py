import json
from flaskr.tests.fixtures.album_fixture import AlbumFixture
from flaskr.tests.fixtures.comentario_album_fixture import AlbumComentarioFixture
from flaskr.tests.fixtures.user_fixtures import UsuarioFixture
from flaskr.modelos import Acceso
from flaskr.tests import BaseCase, fixtures


class TestAlbumComentario(BaseCase):
    def test_given_existing_user_when_add_comment_to_invalid_album_then_fail(self):
        """
        Asserts un usuario solo puede agregar comentarios a albumes existentes
        """
        # Arrange
        user = UsuarioFixture().create()
        
        album_fixture = AlbumFixture()
        album_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PRIVADO)
        album = album_fixture.create()
        
        comentario_data = {
            "texto": "Este es un comentario"
        }

        # Act
        response = self.run_authenticated(user, 'post', f'/album/{album.id+1}/comentarios', data=json.dumps(comentario_data))

        # Assert
        self.assertEqual(404, response.status_code)

    def test_given_existing_user_when_add_comment_to_private_album_then_fail(self):
        """
        Asserts un usuario no puede agregar un comentario a un album privado
        """
        # Arrange
        user = UsuarioFixture().create()
        
        album_fixture = AlbumFixture()
        album_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PRIVADO)
        album = album_fixture.create()
        
        comentario_data = {
            "texto": "Este es un comentario"
        }

        # Act
        response = self.run_authenticated(user, 'post', f'/album/{album.id}/comentarios', data=json.dumps(comentario_data))

        # Assert
        self.assertEqual(400, response.status_code)

    def test_given_existing_user_when_add_comment_to_public_album_then_success(self):
        """
        Asserts un usuario puede ver agregar un comenario a un album publico
        """
        # Arrange
        user = UsuarioFixture().create()
        
        album_fixture = AlbumFixture()
        album_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PUBLICO)
        album = album_fixture.create()
        
        comentario_data = {
            "texto": "Este es un comentario"
        }

        # Act
        response = self.run_authenticated(user, 'post', f'/album/{album.id}/comentarios', data=json.dumps(comentario_data))
        comentario = response.json
        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(comentario['texto'], comentario_data['texto'])

    def test_given_existing_user_when_list_comment_of_private_album_then_fail(self):
        """
        Asserts un usuario no puede ver la lista de comentarios de un album privado
        """
        # Arrange
        user = UsuarioFixture().create()
        
        album_fixture = AlbumFixture()
        album_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PRIVADO)
        album = album_fixture.create()
        
        # Act
        response = self.run_authenticated(user, 'get', f'/album/{album.id}/comentarios')

        # Assert
        self.assertEqual(400, response.status_code)

    def test_given_existing_user_when_list_comments_of_public_album_then_success(self):
        """
        Asserts un usuario puede ver su lista de comentarios de un album
        """
        # Arrange
        user = UsuarioFixture().create()
        
        album_fixture = AlbumFixture()
        album_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PUBLICO)
        album = album_fixture.create()

        album_comentario_fixture = AlbumComentarioFixture()
        album_comentario_fixture.default_album = fixtures.ObjectFixture(album) # comentarios para solo para el album creado previamente

        primer_comentario = album_comentario_fixture.create()
        segundo_comentario = album_comentario_fixture.create()
        tercer_comentario = album_comentario_fixture.create()
        
        # Act
        response = self.run_authenticated(user, 'get', f'/album/{album.id}/comentarios')
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

    def test_given_existing_user_when_list_comments_of_public_album_then_see_comments_belong_given_album_success(self):
        """
        Asserts un usuario puede ver la lista de comentarios de un album si es que existen
        """
        # Arrange
        user = UsuarioFixture().create()
        
        album_fixture = AlbumFixture()
        album_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PUBLICO)
        album = album_fixture.create()

        album_sin_comentarios = album_fixture.create()

        album_comentario_fixture = AlbumComentarioFixture()
        album_comentario_fixture.default_album = fixtures.ObjectFixture(album) # comentarios para solo para el primer album creado
        # comentario para el primer album
        album_comentario_fixture.create()        
        
        # Act
        response = self.run_authenticated(user, 'get', f'/album/{album_sin_comentarios.id}/comentarios')
        comentarios = response.json
        
        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(comentarios), 0)

    def test_given_existing_user_when_list_comments_of_public_album_then_see_comments_belong_given_albums_success(self):
        """
        Asserts un usuario puede ver la lista de comentarios de mas de un album publico
        """
        # Arrange
        user = UsuarioFixture().create()
        
        album_fixture = AlbumFixture()
        album_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PUBLICO)
        primer_album = album_fixture.create()
        segundo_album = album_fixture.create()

        album_comentario_fixture = AlbumComentarioFixture()
        album_comentario_fixture.default_album = fixtures.ObjectFixture(primer_album) 
        # dos comentarios para el primer album
        album_comentario_fixture.create()
        album_comentario_fixture.create()
        
        album_comentario_fixture.default_album = fixtures.ObjectFixture(segundo_album) 
        # un comentario para el segundo album
        album_comentario_fixture.create()

        # Act
        response_comentarios_primer_album = self.run_authenticated(user, 'get', f'/album/{primer_album.id}/comentarios')
        comentarios_primer_album = response_comentarios_primer_album.json
        
        response_comentarios_segundo_album = self.run_authenticated(user, 'get', f'/album/{segundo_album.id}/comentarios')
        comentarios_segundo_album = response_comentarios_segundo_album.json
        
        # Assert
        self.assertEqual(200, response_comentarios_primer_album.status_code)
        self.assertEqual(200, response_comentarios_segundo_album.status_code)
        self.assertEqual(len(comentarios_primer_album), 2)
        self.assertEqual(len(comentarios_segundo_album), 1)
