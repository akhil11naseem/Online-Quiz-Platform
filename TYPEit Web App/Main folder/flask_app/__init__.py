from flask import Flask
from .extensions import db, login_manager
from .commands import create_tables
from .routes.main import main
from .routes.auth import auth
from .models import User

def create_app(config_file = 'settings.py'):

    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    app.app_context().push()
    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)
    app.register_blueprint(auth)

    app.cli.add_command(create_tables)

    return app
