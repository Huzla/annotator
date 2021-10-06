import os

from flask import Flask
from flask_migrate import Migrate

from .models import *
from .views.domains import bp as domains_bp

if __name__ == "__main__":
    manager.run()

def create_app_and_db():
    app = Flask(__name__, instance_relative_config=True)

    app.config["CORS_HEADERS"] = "Content-Type"

    app.config.from_mapping(
        SECRECT_KEY=os.getenv("SECRET_KEY")
    )

    app.config.from_object(os.environ["APP_SETTINGS"])
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    Migrate(app, db)

    app.register_blueprint(domains_bp)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello"

    return [app, db]

def create_app():
    app, _ = create_app_and_db()
    return app    