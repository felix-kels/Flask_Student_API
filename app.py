from api import create_app, student_ns, course_ns
from api.config import Config
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_restx import Api, fields, Resource, reqparse


config = Config

app, api = create_app(config=config)

student_parser = reqparse.RequestParser()
student_parser.add_argument('name', type=str, required=True, help='Student name is required')
student_parser.add_argument('id', type=int, required=True, help='Student ID is required')
student_parser.add_argument('email', type=str, required=True, help='Student email is required')
student_parser.add_argument('courses', type=list, location='json', help='List of course IDs is required')


course_parser = reqparse.RequestParser()
course_parser.add_argument('name', type=str, required=True, help='Course name is required')
course_parser.add_argument('id', type=int, required=True, help='Course ID is required')
course_parser.add_argument('teacher', type=str, required=True, help='Teacher name is required')
course_parser.add_argument('students', type=list, location='json', help='List of student IDs is required')


student_model = api.model('Student', {
    'name': fields.String(required=True, description='Student Name'),
    'id': fields.Integer(required=True, description='Student ID'),
    'email': fields.String(required=True, description='Student Email')
})


course_model = api.model('Course', {
    'name': fields.String(required=True, description='Course Name'),
    'id': fields.Integer(required=True, description='Course ID'),
    'teacher': fields.String(required=True, description='Teacher Name'),
    'students': fields.List(fields.Nested(student_model), description='List of Students')
})


@student_ns.route('/students')
class StudentList(Resource):
    @student_ns.marshal_with(student_model)
    def get(self):
        # Return all students
        pass

    @student_ns.expect(student_model)
    @student_ns.marshal_with(student_model)
    def post(self):
        # args = student_parser.parse_args()
        # name = args['name']
        # id = args['id']
        # email = args['email']
        # Create a new student
        pass


@student_ns.route('/students/<id>')
class Student(Resource):
    @student_ns.marshal_with(student_model)
    def get(self, id):
        # Return a specific student
        pass

    @student_ns.expect(student_parser)
    @student_ns.marshal_with(student_model)
    def put(self, id):
        # Update a specific student
        pass

    @student_ns.response(204, "Student Deleted Successfully")
    def delete(self, id):
        # Delete a specific student
        pass


@course_ns.route('/courses')
class CourseList(Resource):
    @course_ns.marshal_with(course_model)
    def get(self):
        # Return all courses
        pass

    @course_ns.expect(course_model)
    @course_ns.marshal_with(course_model)
    def post(self):
        pass


@course_ns.route('/courses/<id>')
class Course(Resource):
    @course_ns.marshal_with(course_model)
    def get(self, id):
        # Return a specific course
        pass

    @course_ns.expect(course_parser)
    @course_ns.marshal_with(course_model)
    def put(self, id):
        # Update a specific course
        pass

    @course_ns.response(204, "Course Deleted Successfully")
    def delete(self, id):
        # Delete a specific course
        pass


@course_ns.route('/courses/<id>/students')
class CourseStudents(Resource):
    @course_ns.marshal_with(student_model)
    def get(self, id):
        # Return all students registered in a specific course
        pass

    @course_ns.expect(student_model)
    @course_ns.marshal_with(student_model)
    def post(self, id):
        # Register a new student for a specific course
        pass


grade_model = api.model('Grade', {
    'student_id': fields.String(required=True),
    'course_id': fields.String(required=True),
    'grade': fields.Float(required=True)
})


@api.route('/grades')
class GradeList(Resource):
    @api.expect(grade_model)
    @api.marshal_with(grade_model)
    def post(self):
        # Add a grade for a specific student in a specific course
        pass


@api.route('/students/<id>/grades')
class StudentGrades(Resource):
    @api.marshal_with(grade_model)
    def get(self, id):
        # Return all grades for a specific student
        pass

    def delete(self, id):
        # Delete all grades for a specific student
        pass


@api.route('/courses/<id>/grades')
class CourseGrades(Resource):
    @api.marshal_with(grade_model)
    def get(self, id):
        # Return all grades for a specific course
        pass


@api.route('/students/<id>/gpa')
class StudentGPA(Resource):
    def get(self, id):
        # Calculate the GPA for a specific student
        pass
#
#
# @jwt._user_claims_callback
# def add_claims_to_access_token(identity):
#     # Retrieve user info from database based on the identity
#     user = User.query.filter_by(id=identity).first()
#     return {'name': 'role', 'value': user.role}
#
#
# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user['id']


@api.route('/login')
class Login(Resource):
    def post(self):
        # Authenticate and generate JWT token
        pass


@api.route('/protected')
class Protected(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        # Access protected resource
        pass


if __name__ == "__main__":
    app.run(debug=True, port=5001)

