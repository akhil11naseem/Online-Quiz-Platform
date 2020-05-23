from flask import Flask
from .extensions import db, login_manager
from .commands import create_tables
from .routes.main import main
from .routes.auth import auth
from .models import User
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


def create_app(config_file = 'settings.py'):
    #create an app and configure it
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    app.app_context().push()
   


    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    db.init_app(app)
    
    
    #Configure the login_manager object 
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)
    app.register_blueprint(auth)

    app.cli.add_command(create_tables)

    return app
