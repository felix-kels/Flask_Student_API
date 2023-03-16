grade_scale = {
    'A': 4,
    'B': 3,
    'C': 2,
    'D': 1,
    'F': 0
}


def get_grade(score):
    if not isinstance(score, (int, float)) or score < 0 or score > 100:
        return None  # return None for invalid input

    if score >= 70:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 50:
        return 'C'
    elif score >= 45:
        return 'D'
    else:
        return 'F'


def calculate_grade(student, course):
    total_quality_points = 0
    total_course_units = 0
    for item in student.student_grades:
        item.grade = get_grade(item.score)
        course_units = course.query.get_or_404(item.course_id).units
        quality_points = course_units * grade_scale.get(item.grade)
        total_quality_points = total_quality_points + quality_points
        item.course = item.grade_course
        total_course_units = total_course_units + course_units
    if total_course_units and total_quality_points:
        student.GPA = round((total_quality_points / total_course_units), 2)