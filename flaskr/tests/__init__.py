import unittest
import tempfile
import json

from flaskr.app import app
from flaskr.modelos import db


class BaseCase(unittest.TestCase):
    db_fd, db_path = tempfile.mkstemp()

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_path}'
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        # Delete Database collections after the test is complete
        db.session.remove()
        db.drop_all()

    def run_authenticated(self, user, method, *args, **kwargs):
        user_payload = json.dumps({
             "nombre": user.nombre,
             "contrasena": user.contrasena
        })
        login_response = self.client.post('/logIn', headers={"Content-Type": "application/json"}, data=user_payload)
        headers={"Content-Type": "application/json", 'Authorization': f"Bearer {login_response.json['token']}"}
        kwargs['headers'] = headers
        if method == 'get':
            return self.client.get(*args, **kwargs)
        if method == 'post':
            return self.client.post(*args, **kwargs)
        if method == 'put':
            return self.client.put(*args, **kwargs)
        if method == 'delete':
            return self.client.delete(*args, **kwargs)
        if method == 'patch':
            return self.client.patch(*args, **kwargs)
