from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from api.extensions import db
from api.models import Student, Course, Grade
from api.schemas import StudentSchema, CourseSchema, GradeSchema
from api.utils import calculate_grade

# Initialize namespaces
student_ns = Namespace('students', description='Student Field')
course_ns = Namespace('courses', description='Course Field')

# Initialize schemas
student_schema = StudentSchema(many=False)
students_schema = StudentSchema(many=True)
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
grade_schema = GradeSchema()
grades_schema = GradeSchema(many=True)


@student_ns.route('')
class StudentListResource(Resource):
    @jwt_required()
    def get(self):
        students = Student.query.all()
        return students_schema.dump(students), 200

    @jwt_required()
    def post(self):
        data = request.get_json()

        if not data:
            return {"message": "No input data provided"}, 400

        student_data, errors = student_schema.load(data)
        if errors:
            return errors, 422

        student = Student(**student_data)
        db.session.add(student)
        db.session.commit()

        return student_schema.dump(student), 201


# Student resource
@student_ns.route('/<int:student_id>')
class StudentResource(Resource):
    @jwt_required()
    def get(self, student_id):
        student = Student.query.get(student_id) # to get one object from the database use query.get() 
        if not student:
            return {"message": "Student not found"}, 404
        return student_schema.dump(student), 200

    @jwt_required()
    def put(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400

        student_data, errors = student_schema.load(data, partial=True)
        if errors:
            return errors, 422

        for key, value in student_data.items():
            setattr(student, key, value)

        db.session.commit()

        return student_schema.dump(student), 200

    @jwt_required()
    def delete(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        db.session.delete(student)
        db.session.commit()

        return {"message": "Student deleted"}, 200


# Course resource
@course_ns.route('/')
class CourseResource(Resource):
    @jwt_required()
    def get(self):
        courses = Course.query.all()
        return courses_schema.dump(courses), 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        errors = course_schema.validate(data)
        if errors:
            return errors, 400
        course = Course(**data)
        db.session.add(course)
        db.session.commit()
        return course_schema.dump(course), 201


# Course registration functionality
@course_ns.route('/<int:course_id>/register/<int:student_id>')
class CourseRegistrationResource(Resource):
    @jwt_required()
    def post(self, course_id, student_id):
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 404

        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        grade = Grade(student_id=student_id, course_id=course_id, grade=0)
        db.session.add(grade)
        db.session.commit()

        return {"message": "Student registered for the course"}, 200


# Endpoints for retrieving all students, all courses, and students registered in a particular course
@course_ns.route('')
class CourseListResource(Resource):
    @jwt_required()
    def get(self):
        courses = Course.query.all()
        return courses_schema.dump(courses), 200


# Student grades resource
@student_ns.route('/<int:student_id>/grades')
class StudentGradesResource(Resource):
    @jwt_required()
    def get(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        # Get the student's numerical grades from the Grade model
        grades = [grade.grade for grade in student.grades]

        # Calculate the student's GPA
        gpa = calculate_grade(grades)

        # Return the calculated GPA along with the student's grades
        return {
                   "grades": grades_schema.dump(student.grades),
                   "gpa": gpa,
               }, 200


# Students registered in a course resource
@course_ns.route('/<int:course_id>/students')
class CourseStudentsResource(Resource):
    @jwt_required()
    def get(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 404

        grades = Grade.query.filter_by(course_id=course_id).all()
        student_ids = [grade.student_id for grade in course.grades]
        students = Student.query.filter(Student.id.in_(student_ids)).all()

        return students_schema.dump(students), 200


@course_ns.route('/int:course_id/grades')
class CourseGradesResource(Resource):
    @jwt_required()
    def get(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 404
        grades = Grade.query.filter_by(course_id=course_id).all()
        grades_data = grades_schema.dump(grades)

        for grade_data in grades_data:
            student = Student.query.get(grade_data['student_id'])
            grade_data['student_name'] = student.name
            grade_data['student_email'] = student.email
        return grades_data, 200


@student_ns.route('/int:student_id/gpa')
class StudentGPAResource(Resource):
    @jwt_required()
    def get(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        grades = Grade.query.filter_by(student_id=student_id).all()
        gpa = calculate_grade(grades)

        return {"gpa": gpa}, 200
