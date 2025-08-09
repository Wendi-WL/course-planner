from scraper.models import Course # maybe want to move the model to myapp/models.py

def find_eligible_courses(taken_courses_list):
    """
    Determines which courses can be taken based on a list of taken courses.
    
    Args:
        taken_courses_list (list): A list of strings, e.g., ["CPSC 110", "CPSC 121"].
    
    Returns:
        list: A list of Course objects that are eligible to be taken.
    """

    # !!!!! return all course info, not just course id
    # !!!!! also take a subject for filtering (only fetch courses from db that have that subject)
    
    all_courses = Course.objects.all() # accesses database to get all courses
    taken_courses_set = set(taken_courses_list)
    eligible_courses = []

    for course in all_courses:
        prereqs = course.prereqs 

        if all(prereq in taken_courses_set for prereq in prereqs):
            eligible_courses.append(f"{course.subject} {course.code}")
            print(f"updated list of eligible courses: {eligible_courses}")

    return eligible_courses