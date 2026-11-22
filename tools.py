import os

# ---------------------------------------------------------------------------
# PUCIT grade bands
# ---------------------------------------------------------------------------
GRADE_BANDS = [
    (85, 100, 4.0),
    (80, 84, 3.7),
    (75, 79, 3.3),
    (70, 74, 3.0),
    (65, 69, 2.7),
    (61, 64, 2.3),
    (58, 60, 2.0),
    (55, 57, 1.7),
    (50, 54, 1.0),
    (0, 49, 0.0),
]


COURSES = {
    1: [("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation - I", 0.5),
        ("GE-190", "Functional English", 3.0)],

    2: [("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation - II", 0.5)],

    3: [("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation - III", 0.5)],

    4: [("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0)],

    5: [("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation - V", 0.5)],

    6: [("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation - VI", 0.5)],

    7: [("CC-411", "Final Year Project - I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation - VII", 0.5)],

    8: [("CC-412", "Final Year Project - II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation - VIII", 0.5)],
}


MD_COURSES = {"MD-001", "MD-002"}


def marks_to_grade_points(marks: float) -> float | str:
    """
    Convert numeric marks (0-100) to a PUCIT grade point using the
    official grade bands (see §5.1). Use this any time a user gives you
    raw marks for a course and you need the grade point before running
    a GPA calculation.
    """
    if not isinstance(marks, (int, float)) or marks < 0 or marks > 100:
        return "Error: marks must be between 0 and 100"
    for low, high, gp in GRADE_BANDS:
        if low <= marks <= high:
            return gp
    return "Error: marks must be between 0 and 100"


def calculate_semester_gpa(grade_points: list[float], credit_hours: list[float]) -> float | str:
    """
    Calculate one semester's credit-weighted GPA from a list of grade
    points and the matching list of credit hours. Use this once you have
    the grade point (via marks_to_grade_points, or given directly) and
    the credit hours for every course the user took in a single semester.
    The two lists must be the same length and in matching order.
    """
    if not grade_points or not credit_hours:
        return "Error: grade_points and credit_hours must not be empty"
    if len(grade_points) != len(credit_hours):
        return "Error: grade_points and credit_hours must be the same length"
    if any(ch <= 0 for ch in credit_hours):
        return "Error: credit_hours must all be positive"
    total_points = sum(gp * ch for gp, ch in zip(grade_points, credit_hours))
    total_hours = sum(credit_hours)
    return round(total_points / total_hours, 3)


def calculate_new_cgpa(current_cgpa: float, completed_credit_hours: float,
                        semester_gpa: float, semester_credit_hours: float) -> float | str:
    """
    Project a student's new CGPA after completing one more semester.
    Use this when the user gives you their current CGPA, how many credit
    hours they've already completed, and the GPA + credit hours of the
    semester they just finished (or plan to finish).
    """
    if completed_credit_hours < 0 or semester_credit_hours <= 0:
        return "Error: credit hours must be positive"
    if not (0.0 <= current_cgpa <= 4.0) or not (0.0 <= semester_gpa <= 4.0):
        return "Error: GPA/CGPA values must be between 0.0 and 4.0"
    new_cgpa = (
        (current_cgpa * completed_credit_hours) + (semester_gpa * semester_credit_hours)
    ) / (completed_credit_hours + semester_credit_hours)
    return round(new_cgpa, 3)


def required_gpa_for_target(target_cgpa: float, current_cgpa: float,
                             current_credit_hours: float, remaining_credit_hours: float) -> float | str:
    """
    Calculate the GPA a student needs to earn over their remaining credit
    hours to reach a target CGPA. Use this when the user states a target
    CGPA and gives you their current CGPA, completed credit hours, and
    remaining credit hours. The result can come out above 4.0, which
    means the target is impossible over that horizon — report it as such,
    do not present it as an achievable answer.
    """
    if remaining_credit_hours <= 0:
        return "Error: remaining_credit_hours must be positive"
    if not (0.0 <= target_cgpa <= 4.0) or not (0.0 <= current_cgpa <= 4.0):
        return "Error: GPA/CGPA values must be between 0.0 and 4.0"
    required = (
        (target_cgpa * (current_credit_hours + remaining_credit_hours))
        - (current_cgpa * current_credit_hours)
    ) / remaining_credit_hours
    return round(required, 3)


def get_semester_courses(semester: int) -> str:
    """
    Return the list of courses and credit hours for a given semester
    (1-8) of the BS Computer Science scheme. Use this when the user
    mentions a semester number and you need to know which courses or
    how many credit hours belong to it.
    """
    if semester not in COURSES:
        return "Error: semester must be between 1 and 8"
    lines = [f"{code}: {name} ({ch} credit hours)" for code, name, ch in COURSES[semester]]
    return "\n".join(lines)


def get_remaining_credit_hours(current_semester: int) -> float | str:
    """
    Total the graded credit hours remaining AFTER a given semester
    (i.e. semesters current_semester+1 through 8). Use this whenever you
    need to know how many credit hours a student has left in the degree,
    for example before calling required_gpa_for_target.
    """
    if current_semester not in COURSES:
        return "Error: semester must be between 1 and 8"
    remaining = 0.0
    for sem in range(current_semester + 1, 9):
        remaining += sum(ch for _, _, ch in COURSES[sem])
    return round(remaining, 2)


def save_report(filename: str, content: str) -> str:
    """
    Save a text summary (a semester GPA, a projected CGPA, or a plan for
    reaching a target) to disk. Only call this after producing something
    worth keeping, and only when the user has asked you to save it.
    """
    if not filename.strip():
        return "Error: filename must not be empty"
    if not filename.endswith(".txt"):
        filename += ".txt"
    path = os.path.join(os.getcwd(), filename)
    try:
        with open(path, "w") as f:
            f.write(content)
    except OSError as e:
        return f"Error: could not save file ({e})"
    return f"Report saved to {path}"
