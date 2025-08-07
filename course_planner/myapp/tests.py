from django.test import TestCase
from scraper.models import Course
from .utils import find_eligible_courses

# Create your tests here.
class CourseEligibilityTests(TestCase):
    def setUp(self):
        """
        Set up the test data that will be used by all test methods.
        """
        Course.objects.create(subject="CPSC", code=100, credit=3, prereqs=[])
        Course.objects.create(subject="CPSC", code=103, credit=3, prereqs=[])
        Course.objects.create(subject="CPSC", code=107, credit=3, prereqs=[])
        Course.objects.create(subject="CPSC", code=110, credit=4, prereqs=[])
        Course.objects.create(subject="CPSC", code=121, credit=4, prereqs=[])
        Course.objects.create(subject="CPSC", code=210, credit=4, prereqs=["CPSC 110"])
        Course.objects.create(subject="CPSC", code=213, credit=4, prereqs=["CPSC 121", "CPSC 210"])
        Course.objects.create(subject="CPSC", code=221, credit=4, prereqs=["CPSC 121", "CPSC 210"])
        Course.objects.create(subject="CPSC", code=299, credit=4, prereqs=["CPSC 210", "CPSC 298"])

    def test_finds_courses_with_no_prereqs(self):
        """
        Tests that the function returns courses with empty prerequisite lists.
        """
        taken = []
        eligible = find_eligible_courses(taken)

        self.assertIn("CPSC 100", eligible)
        self.assertIn("CPSC 103", eligible)
        self.assertIn("CPSC 107", eligible)
        self.assertIn("CPSC 110", eligible)
        self.assertIn("CPSC 121", eligible)
        self.assertEqual(len(eligible), 5)

    def test_finds_courses_with_110_taken(self):
        """
        Tests that the function correctly identifies courses with fulfilled prereq of CPSC 110.
        """
        taken = ["CPSC 110"]
        eligible = find_eligible_courses(taken)

        self.assertIn("CPSC 100", eligible)
        self.assertIn("CPSC 103", eligible)
        self.assertIn("CPSC 107", eligible)
        self.assertIn("CPSC 110", eligible) # have for now, may remove if taken already
        self.assertIn("CPSC 121", eligible)
        self.assertIn("CPSC 210", eligible) # CPSC 210 should also be eligible
        self.assertEqual(len(eligible), 6)

    def test_finds_courses_with_multiple_taken(self):
        """
        Tests that the function correctly identifies courses with multiple fulfilled prereqs.
        """
        taken = ["CPSC 110", "CPSC 121", "CPSC 210"]
        eligible = find_eligible_courses(taken)

        self.assertIn("CPSC 100", eligible)
        self.assertIn("CPSC 103", eligible)
        self.assertIn("CPSC 107", eligible)
        self.assertIn("CPSC 110", eligible) 
        self.assertIn("CPSC 121", eligible)
        self.assertIn("CPSC 210", eligible) 
        self.assertIn("CPSC 213", eligible) 
        self.assertIn("CPSC 221", eligible) 
        self.assertEqual(len(eligible), 8)