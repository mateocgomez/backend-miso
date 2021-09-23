import json
from flaskr.tests.fixtures.user_fixtures import UsuarioFixture
from flaskr.tests import BaseCase, fixtures

class TestCancion(BaseCase):

  def test_endpoint_patch_change_acceso_cancion(self):

    # Arrange
    user = UsuarioFixture().create()

    cancion_data = {
        'titulo': 'test cancion 1',
        'minutos': 1,
        'segundos': 1,
        'interprete': 'test interprete 1'
    }

    # Act  
    crear_cancion_response = self.run_authenticated(user, 'post', f'/canciones', data=json.dumps(cancion_data))       
    cancion = crear_cancion_response.json

    cambiar_acceso_data = {
      "acceso": "PUBLICO"
    }

    cambiar_acceso_response = self.run_authenticated(user, 'patch', f'/cancion/{cancion["id"]}', data=json.dumps(cambiar_acceso_data))
    
    cancion_nuevo_acceso_response = self.run_authenticated(user, 'get', f'/cancion/{cancion["id"]}')  
    cancion_nuevo_acceso = cancion_nuevo_acceso_response.json

    # Assert
    self.assertEqual(cancion["acceso"]["valor"], 1)
    self.assertEqual(cambiar_acceso_response.status_code, 204)        
    self.assertEqual(cancion_nuevo_acceso["acceso"]["valor"], 2)

  def test_endpoint_patch_cancion_without_jwt(self):
    # Arrange
    user = UsuarioFixture().create()

    cancion_data = {
        'titulo': 'test cancion 1',
        'minutos': 1,
        'segundos': 1,
        'interprete': 'test interprete 1'
    }

    # Act  
    crear_cancion_response = self.run_authenticated(user, 'post', f'/canciones', data=json.dumps(cancion_data))       
    cancion = crear_cancion_response.json

    cambiar_acceso_data = {
      "acceso": "PUBLICO"
    }

    response = self.client.patch(f'/cancion/{cancion["id"]}', headers={"Content-Type": "application/json"}, data=json.dumps(cambiar_acceso_data))
    
    # Assert
    self.assertEqual(response.status_code, 401)        

  def test_endpoint_patch_cancion_invalid_acceso_value(self):
    # Arrange
    user = UsuarioFixture().create()

    cancion_data = {
        'titulo': 'test cancion 1',
        'minutos': 1,
        'segundos': 1,
        'interprete': 'test interprete 1'
    }

    # Act  
    crear_cancion_response = self.run_authenticated(user, 'post', f'/canciones', data=json.dumps(cancion_data))       
    cancion = crear_cancion_response.json

    cambiar_acceso_data = {
      "acceso": "P_U_B_L_I_C_O"
    }

    response = self.run_authenticated(user, 'patch', f'/cancion/{cancion["id"]}', data=json.dumps(cambiar_acceso_data))
    
    # Assert    
    self.assertEqual(response.status_code, 400)

  def test_create_canciones_and_list_mine(self):
    
    # Arrange
    user1 = UsuarioFixture().create()

    cancion_data_1 = {
        'titulo': 'test cancion 1',
        'minutos': 3,
        'segundos': 45,
        'interprete': 'test interprete 1'
    }

    cancion_data_2 = {
        'titulo': 'test cancion 2',
        'minutos': 4,
        'segundos': 32,
        'interprete': 'test interprete 2'
    }

    user2 = UsuarioFixture().create()
    cancion_data_3 = {
        'titulo': 'test cancion 3',
        'minutos': 2,
        'segundos': 28,
        'interprete': 'test interprete 3'
    }
    
    # Act  
    crear_cancion_response_1 = self.run_authenticated(user1, 'post', f'/canciones', data=json.dumps(cancion_data_1))       
    crear_cancion_response_2 = self.run_authenticated(user1, 'post', f'/canciones', data=json.dumps(cancion_data_2))       
    crear_cancion_response_3 = self.run_authenticated(user2, 'post', f'/canciones', data=json.dumps(cancion_data_3))       
    
    list_canciones_response = self.run_authenticated(user1, 'get', f'/canciones')       
    list_canciones = list_canciones_response.json

    # Assert    
    self.assertEqual(crear_cancion_response_1.status_code, 200)  
    self.assertEqual(crear_cancion_response_2.status_code, 200)  
    self.assertEqual(crear_cancion_response_3.status_code, 200)  
    self.assertEqual(list_canciones_response.status_code, 200)     
    self.assertEqual(len(list_canciones), 2) 

  def test_list_canciones_exists_pertenece_field(self):

    # Arrange
    user = UsuarioFixture().create()

    cancion_data = {
        'titulo': 'test cancion 1',
        'minutos': 3,
        'segundos': 45,
        'interprete': 'test interprete 1'
    }
    
    # Act  
    crear_cancion_response = self.run_authenticated(user, 'post', f'/canciones', data=json.dumps(cancion_data))           
    list_canciones_response = self.run_authenticated(user, 'get', f'/canciones')       
    list_canciones = list_canciones_response.json

    # Assert    
    self.assertEqual(crear_cancion_response.status_code, 200)    
    self.assertEqual(list_canciones_response.status_code, 200)     
    self.assertTrue(all("pertenece" in cancion for cancion in list_canciones))  















