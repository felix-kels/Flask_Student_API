from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from api.models import User
from api.schemas import UserSchema
from api.routes import student_ns
from api.extensions import db

# Initialize the namespace and schema
auth_ns = Namespace('auth', description='Authentication Field')
user_schema = UserSchema(many=False)

login_model = auth_ns.model(
    'Login',
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True)
    }
)


# User registeration
@auth_ns.route('/register')
class RegisterationResource(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()

        if not data:
            return {"message": "No input data provided"}, 400

        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first() is not None:
            return {"message": "Invalid email or password"}, 409

        new_user = User(email=email, password_hash=password)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 201


# User authentication resource
@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()

        if not data:
            return {"message": "No input data provided"}, 400

        # Check if the user exists and the password is correct
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return {"message": "Invalid email or password"}, 401

        # Create a JWT access token
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200


# Access control using the jwt_required decorator
@auth_ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return {"message": f"Welcome, {user.email}"}, 200
