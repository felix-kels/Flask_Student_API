from flask import Flask
from flask_restx import Api
from flask_restx import fields
from flask_restx import Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    app.run(debug=True)


# Defining the Student Model.
student = api.model('Student', {
    'id': fields.Integer(required=True, description='The student ID'),
    'name': fields.String(required=True, description='The student name'),
    'email': fields.String(required=True, description='The student email address')
})


# Creating Endpoints for Creating, Reading, Updating, and Deleting Students.
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='The student name')
parser.add_argument('email', type=str, required=True, help='The student email address')


@api.route('/students')
class StudentList(Resource):
    @api.marshal_list_with(student)
    def get(self):
        pass

    @api.expect(parser)
    @api.marshal_with(student, code=201)
    def post(self):
        pass


@api.route('/students/<int:id>')
@api.response(404, 'Student not found')
class Student(Resource):
    @api.marshal_with(student)
    def get(self, id):
        pass

    @api.expect(parser)
    @api.marshal_with(student)
    def put(self, id):
        pass

    @api.response(204, 'Student deleted')
    def delete(self, id):
        pass


# Defining the Course Model
course = api.model('Course', {
    'id': fields.Integer(required=True, description='The course ID'),
    'name': fields.String(required=True, description='The course name'),
    'teacher': fields.String(required=True, description='The course teacher'),
    'students': fields.List(fields.Nested(student), description='The students registered for the course')
})


# Creating Endpoints for Retrieving Courses and Registered Students
@api.marshal_list_with(course)
def get(self):
    pass


@api.route('/courses/int:id/students')
@api.response(404, 'Course not found')
class CourseStudents(Resource):
    @api.marshal_list_with(student)
    def get(self, id):pass


# Define the Grade Model
grade = api.model('Grade', {
    'course_id': fields.Integer(required=True, description='The course ID'),
    'student_id': fields.Integer(required=True, description='The student ID'),
    'grade': fields.Float(required=True, description='The student grade')
})


# Implementing The GPA Calculation Functionality
@api.route('/students/<int:id>/gpa')
@api.response(404, 'Student not found')
class StudentGPA(Resource):
    @api.doc(params={'courses': 'A comma-separated list of course IDs'})
    def get(self, id):
        pass

# Implementing Authentication and Authorization


app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)


@api.route('/login')
class Login(Resource):
    def post(self):
        pass


@api.route('/protected')
class Protected(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        pass
