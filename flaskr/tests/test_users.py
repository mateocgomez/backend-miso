import json

from flaskr.tests import BaseCase

class TestUserLogin(BaseCase):

    def test_given_non_existing_user_when_login_then_fail(self):
        # Arrange
        email = "paurakh011@gmail.com"
        password = "mycoolpassword"
        user_payload = json.dumps({
            "nombre": email,
            "contrasena": password
        })

        # Act
        response = self.client.post('/logIn', headers={"Content-Type": "application/json"}, data=user_payload)

        # Assert
        self.assertEqual(404, response.status_code)
        self.assertEqual('El usuario no existe', response.json)

    def test_given_a_new_registered_user_when_login_then_success(self):
        # Arrange
        email = "paurakh011@gmail.com"
        password = "mycoolpassword"
        
        user_payload = json.dumps({
            "nombre": email,
            "contrasena": password
        })

        # Act
        signin_response = self.client.post('/signin', headers={"Content-Type": "application/json"}, data=user_payload)
        login_response = self.client.post('/logIn', headers={"Content-Type": "application/json"}, data=user_payload)

        # Assert
        self.assertEqual(200, signin_response.status_code)
        self.assertEqual(200, login_response.status_code)
