import unittest
import json
from api import create_app
from api.extensions import db
from api.models import User
from flask_jwt_extended import create_access_token

from werkzeug.security import generate_password_hash
from api.config import TestingConfig


class TestAuth(unittest.TestCase):

    def setUp(self):
        # Create a test app
        self.app = create_app(config=TestingConfig)

        # create an app context
        self.app_contxt = self.app.app_context()
        self.app_contxt.push()
        self.client = self.app.test_client()

        # Create a test database
        db.create_all()

        # Create some test data
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        self.access_token = create_access_token(identity=1)

    # Destroy the test data base
    def tearDown(self):
        db.drop_all()

        self.app_contxt.pop()
        self.app = None
        self.client = None

    def test_login(self):
        # Extract the user details from the user_data dictionary
        email = self.user_data['email']
        password = self.user_data['password']

        # create a new instance of the User class for testing
        user = User(email=email, password_hash=password)
        user.set_password(password)

        # commit the new user data
        db.session.add(user)
        db.session.commit()

        # test the response from the login enpoint as 200
        response = self.client.post('/auth/login', json=self.user_data)
        self.assertEqual(response.status_code, 200)

    def test_protected(self):
        # Extract the user details from the user_data dictionary
        email = self.user_data['email']
        password = self.user_data['password']

        # create a new instance of the User class for testing
        user = User(email=email, password_hash=password)
        user.set_password(password)

        # commit the new user data
        db.session.add(user)
        db.session.commit()

        # test the response from the protected route as 200
        response = self.client.get('/auth/protected', headers={
            'Authorization': f'Bearer {self.access_token}'
        })
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        # Extract the user details from the user_data dictionary
        email = self.user_data['email']
        password = self.user_data['password']

        # create a new instance of the User class for testing
        user = User(email=email, password_hash=password)
        user.set_password(password)

        # commit the new user data
        db.session.add(user)
        db.session.commit()

        # test the response from the login enpoint as 200
        response = self.client.post('/auth/login', json=self.user_data)
        self.assertEqual(response.status_code, 200)

    def test_registeration(self):
        response = self.client.post('/auth/register', json=self.user_data)
        self.assertEqual(response.status_code, 201)
