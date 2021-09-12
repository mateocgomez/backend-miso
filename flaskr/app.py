from flaskr import create_app
from flask_restful import Api
from .modelos import db
from .vistas import VistaCanciones, VistaCancion, VistaSignIn, VistaAlbum, VistaAlbumsUsuario, VistaCancionesAlbum, VistaLogIn, VistaAlbumesCanciones, VistaComentarioAlbumUsuario
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin, OpenAPIConverter
from flask_apispec.extension import FlaskApiSpec
import marshmallow


class CustomOpenAPIConverter(OpenAPIConverter):
    def field2default(self, field, **kwargs):
        ret = {}
        if "default" in field.metadata:
            ret["default"] = field.metadata["default"]
        else:
            if hasattr(field, 'load_default'):
                default = field.load_default
            else:
                default = field.default
            if default is not marshmallow.missing and not callable(default):
                default = field._serialize(default, None, None)
                ret["default"] = default
        return ret


class CustomMarshmallowPlugin(MarshmallowPlugin):
    Converter = CustomOpenAPIConverter


APISPEC_SWAGGER_URL = '/swagger/'  # URL for exposing Swagger UI (without trailing '/')
APISPEC_SWAGGER_UI_URL = '/swagger-ui/'  # Our API url (can of course be a local resource)

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app)

api = Api(app)

api.add_resource(VistaCanciones, '/canciones')
api.add_resource(VistaCancion, '/cancion/<int:id_cancion>')
api.add_resource(VistaAlbumesCanciones, '/cancion/<int:id_cancion>/albumes')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/logIn')
api.add_resource(VistaAlbumsUsuario, '/usuario/<int:id_usuario>/albumes')
api.add_resource(VistaAlbum, '/album/<int:id_album>')
api.add_resource(VistaCancionesAlbum, '/album/<int:id_album>/canciones')
api.add_resource(VistaComentarioAlbumUsuario, '/album/<int:id_album>/comentarios')

jwt = JWTManager(app)

spec = APISpec(
        title='Proyecto Ionic - Grupo 2 - API Docs',
        version='v1',
        plugins=[CustomMarshmallowPlugin()],
        openapi_version='2.0.0'
    )

app.config.update({
    'APISPEC_SPEC': spec,
    'APISPEC_SWAGGER_URL': APISPEC_SWAGGER_URL,  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': APISPEC_SWAGGER_UI_URL  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)

docs.register(VistaCanciones)
docs.register(VistaCancion)
docs.register(VistaAlbumesCanciones)
docs.register(VistaSignIn)
docs.register(VistaLogIn)
docs.register(VistaAlbumsUsuario)
docs.register(VistaAlbum)
docs.register(VistaCancionesAlbum)
docs.register(VistaComentarioAlbumUsuario)
