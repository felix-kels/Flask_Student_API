from marshmallow import Schema, fields, validate


# Add the following class to your schemas.py file
class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(min=1, max=100))
    # noinspection PyTypeChecker
    password = fields.String(required=True, validate=validate.Length(min=8, max=100), load_only=True)


class StudentSchema(Schema):
    id = fields.Integer(dump_only=True)
    # noinspection PyTypeChecker
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    # noinspection PyTypeChecker
    email = fields.Email(required=True, validate=validate.Length(min=1, max=100))


class CourseSchema(Schema):
    id = fields.Integer(dump_only=True)
    # noinspection PyTypeChecker
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    # noinspection PyTypeChecker
    teacher = fields.String(required=True, validate=validate.Length(min=1, max=100))


class GradeSchema(Schema):
    id = fields.Integer(dump_only=True)
    student_id = fields.Integer(required=True)
    course_id = fields.Integer(required=True)
    grade = fields.Float(required=True, validate=validate.Range(min=0, max=4.0))