from flask import Flask
from flask_restx import Api
from api.auth import auth_ns
from api.extensions import db, jwt, migrate
from .model_api import ModelApi

# Import views
from api.routes import student_ns, course_ns


# Initialize the Flask application and configure it
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize the extensions with the app
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Initialize the API and add namespaces
    api = ModelApi(app, title='Student Management System', version='1.0',
                   description='An API for student management')
    api.add_namespace(student_ns, path='/students')
    api.add_namespace(course_ns, path='/courses')
    api.add_namespace(auth_ns, path='/auth')

    if __name__ == '__main__':
        app.run(debug=True)

    return app
