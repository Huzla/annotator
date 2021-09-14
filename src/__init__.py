import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

if __name__ == "__main__":
    manager.run()
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRECT_KEY=os.getenv("SECRET_KEY")
    )

    app.config.from_object(os.environ["APP_SETTINGS"])
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = SQLAlchemy(app)

    migrate = Migrate(app, db)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello"

    return app
    