from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
api = Api(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'users_auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = "Пожалйуста аутентифицируйтесь для доступа к сайту."

# noinspection PyUnresolvedReferences
from library.views_rest_api.api_routes import register_api_routes # noqa E402
from library.views.register_blueprints import register_blueprints # noqa E402

register_blueprints(app)
register_api_routes(api)

# noinspection PyUnresolvedReferences
import library.models.user # noqa E402
# noinspection PyUnresolvedReferences
import library.models.author # noqa E402
# noinspection PyUnresolvedReferences
import library.models.book # noqa E402

migrate = Migrate(app, db)
migrate.init_app(app, db)

