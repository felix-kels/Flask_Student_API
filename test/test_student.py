import unittest
import json
from api import create_app, db
from api.models import User, Student, Course
from api.schemas import UserSchema, StudentSchema, CourseSchema
from flask_jwt_extended import create_access_token

from api.config import TestingConfig


class TestStudentAPI(unittest.TestCase):

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
        self.student_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
        }
        self.course_data = {
            'name': 'Math',
            'code': 'MAT101',
            'students': []
        }
        self.access_token = create_access_token(identity=1)

    # Destroy the test data base
    def tearDown(self):
        db.drop_all()

        self.app_contxt.pop()
        self.app = None
        self.client = None

    # def test_create_student(self):
    #     # Test creating a new student
    #     response = self.client.post('/students', json=self.student_data, headers={
    #         'Authorization' : f'Bearer {self.access_token}'
    #     })
    #     self.assertEqual(response.status_code, 201)
    # data = json.loads(response.data)
    # self.assertIn('id', data)

    def test_get_all_students(self):
        # Test getting all students
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = self.client.get('/students', headers=headers)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

        # Add a student to the database
        with self.app.app_context():
            student = Student(**self.student_data)
            db.session.add(student)
            db.session.commit()

        # Test getting all students again
        response = self.client.get('/students', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)

    def test_get_one_student(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}

        # Add a student to the database

        student = Student(**self.student_data)
        db.session.add(student)
        db.session.commit()

        # Test getting a specific student
        response = self.client.get('/students/1', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_one_student_not_found(self):
        token = create_access_token(identity='testadmin')

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get('students/1', headers=headers)

        self.assertEqual(response.status_code, 404)

    def test_get_all_courses(self):
        token = create_access_token(identity='testadmin')

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get('courses/', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])
