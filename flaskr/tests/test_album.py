import json
from flaskr.tests.fixtures.album_fixture import AlbumFixture
from flaskr.tests.fixtures.user_fixtures import UsuarioFixture
from flaskr.modelos import Acceso, Medio
from flaskr.tests import BaseCase, fixtures


class TestAlbum(BaseCase):
    def test_given_existing_user_that_creates_new_album_when_login_and_retrieve_album_list_then_success(self):
        """
        Asserts un usuario puede ver su lista de albumes
        """
        # Arrange
        user = UsuarioFixture().create()
        album_data = {
            'titulo': 'Test',
            'descripcion': 'Test',
            'medio': Medio.CASETE.name,
            'anio': 2020
        }

        # Act        
        crear_album_response = self.run_authenticated(user, 'post', f'/usuario/{user.id}/albumes', data=json.dumps(album_data))
        response = self.run_authenticated(user, 'get', f'/usuario/{user.id}/albumes')

        new_album = crear_album_response.json
        albums = response.json
        
        # Assert
        self.assertEqual(200, crear_album_response.status_code)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(albums), 1)
        self.assertEqual(new_album['acceso']['llave'], Acceso.PRIVADO.name)
        self.assertEqual(new_album['titulo'], album_data['titulo'])
        self.assertTrue(any(album['id'] is new_album['id'] for album in albums))

    def test_given_existing_user_that_have_albums_when_login_and_retrieve_album_list_then_success(self):
        """
        Asserts un usuario puede ver su lista de albumes
        """
        # Arrange
        user = UsuarioFixture().create()
        album_fixture = AlbumFixture()
        album_fixture.default_usuario = fixtures.ObjectFixture(user)

        first_album = album_fixture.create()
        second_album = album_fixture.create()

        # Act        
        response = self.run_authenticated(user, 'get', f'/usuario/{user.id}/albumes')
        albums = response.json
        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(albums), 2)
        self.assertTrue(any(album['id'] is first_album.id for album in albums))
        self.assertTrue(any(album['id'] is second_album.id for album in albums))

    def test_given_existing_user_that_have_albums_and_public_albums_exists_when_login_and_retrieve_album_list_then_success(self):
        """
        Asserts que en la lista de albumes de un usuario puede ver sus albumes y los albumes publicos
        """
        # Arrange
        user_fixture = UsuarioFixture()
        first_user = user_fixture.create()
        album_fixture = AlbumFixture()
        album_fixture.default_usuario = fixtures.ObjectFixture(first_user)

        private_first_album = album_fixture.create()
        private_second_album = album_fixture.create()

        # otro usuario que tendrá albumes publicos
        second_user = user_fixture.create()
        album_fixture.default_usuario = fixtures.ObjectFixture(second_user)
        
        private_album = album_fixture.create()
        
        album_fixture.default_acceso = fixtures.ObjectFixture(Acceso.PUBLICO)
        public_first_album = album_fixture.create()


        # Act        
        response = self.run_authenticated(first_user, 'get', f'/usuario/{first_user.id}/albumes')
        albums = response.json
        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(albums), 3)
        self.assertTrue(any(album['id'] is private_first_album.id for album in albums))
        self.assertTrue(any(album['id'] is private_second_album.id for album in albums))
        self.assertTrue(any(album['id'] is public_first_album.id and album['pertenece'] == False for album in albums)) # album publico que pertenece a otro coleccionista

    def test_given_existing_user_that_makes_an_existing_album_to_public_then_success(self):
        """
        Asserts un usuario puede ver su lista de albumes, incluidos sus albumes publicos
        """
        # Arrange
        user = UsuarioFixture().create()
        album_fixture = AlbumFixture()
        album_fixture.default_usuario = fixtures.ObjectFixture(user)

        first_album = album_fixture.create()
        second_album = album_fixture.create()

        # Act        
        update_response = self.run_authenticated(user, 'patch', f'/album/{first_album.id}', data=json.dumps({'acceso': Acceso.PUBLICO.name}))
        
        albums_response = self.run_authenticated(user, 'get', f'/usuario/{user.id}/albumes')
        albums = albums_response.json

        # Assert
        self.assertEqual(204, update_response.status_code)
        self.assertEqual(len(albums), 2)
        self.assertTrue(any(album['id'] is first_album.id and album['acceso']['llave'] == Acceso.PUBLICO.name for album in albums)) # el album se hizo publico 
        self.assertTrue(any(album['id'] is second_album.id for album in albums))

    def test_given_existing_user_that_is_not_owner_of_public_album_when_mark_album_as_public_then_fail(self):
        """
        Asserts un usuario puede ver su lista de albumes, incluidos sus albumes publicos
        """
        # Arrange
        user = UsuarioFixture().create()
        
        album_fixture = AlbumFixture()
        first_album = album_fixture.create()

        # Act        
        update_response = self.run_authenticated(user, 'patch', f'/album/{first_album.id}', data=json.dumps({'acceso': Acceso.PUBLICO.name}))
        
        # Assert
        error_response = update_response.json
        self.assertEqual(400, update_response.status_code)
        self.assertEqual('No puede cambiar el acceso del album.', error_response['usuario'])
