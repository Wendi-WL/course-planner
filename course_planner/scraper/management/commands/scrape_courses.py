# backend/scraper/management/commands/scrape_courses.py

import requests
import re
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction # Import transaction for atomicity
from scraper.models import Course # Import your Course model

class Command(BaseCommand):
    help = 'Scrapes course data from a specified UBC Course Calendar URL and saves it to the database.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='The URL of the course catalog to scrape')

    def handle(self, *args, **options):
        url = options['url'] if 'url' in options else 'https://vancouver.calendar.ubc.ca/course-descriptions/subject/cpscv' # Replace with actual URL

        self.stdout.write(f"Attempting to scrape from: {url}")

        try:
            response = requests.get(url, timeout=10) # Set a timeout
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        except requests.exceptions.RequestException as e:
            raise CommandError(f"Error fetching URL {url}: {e}")

        soup = BeautifulSoup(response.text, 'html.parser')

        course_list = soup.find('ol', class_='list-none')
        if not course_list:
            self.stdout.write(self.style.WARNING("No course list found. Check the URL and HTML structure."))
            return
        
        course_listings = soup.find_all('li')
        if not course_listings:
            self.stdout.write(self.style.WARNING("No course entries found within the course list. Check the HTML structure."))
            return
        
        courses_to_create = []
        courses_created = 0
        courses_updated = 0
        courses_skipped = 0

        for listing in course_listings:
            try:
                # Extract data using BeautifulSoup selectors
                course_elem = listing.find('h3', class_='text-lg') 

                if course_elem:
                    # 1. Extract the Course Name:
                    # The course name is inside the <strong> tag.
                    name_tag = course_elem.find('strong')
                    course_name = name_tag.get_text(strip=True) if name_tag else ""

                    # 2. Get the text before the <strong> tag:
                    # This part contains "CPSC_V 100 (3)"
                    pre_name_text = course_elem.get_text(separator=' ', strip=True).replace(course_name, '').strip()

                    # 3. Parse the pre_name_text to get subject, code, and credits:
                    # Pattern: (Subject) (Code) [(Credits)]
                    # CPSC_V 100 (3)
                    match = re.match(r'([A-Z_]+)\s+(\d+)\s+\((\d+)\)', pre_name_text)

                    subject = ""
                    code = None
                    credits = None

                    if match:
                        subject = match.group(1) # CPSC_V
                        code = int(match.group(2)) # 100
                        credits = int(match.group(3)) # 3

                        # to strip "_V" from the subject:
                        subject = subject.split('_')[0] if '_' in subject else subject
                    
                    # Type validation
                    if not (len(subject) == 4 and subject.isalpha()): # Assuming 4-letter alphabetic subject
                        self.stdout.write(self.style.WARNING(f"Skipping invalid subject format: {subject}"))
                        courses_skipped += 1
                        continue
                
                    try:
                        if not (100 <= code <= 700):
                            self.stdout.write(self.style.WARNING(f"Skipping code out of range: {code}"))
                            courses_skipped += 1
                            continue
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f"Skipping invalid code (not a number): {code}"))
                        courses_skipped += 1
                        continue

                    try:
                        credits = int(credits) 
                        if credits < 0: # Or whatever your minimum credit is
                            self.stdout.write(self.style.WARNING(f"Skipping invalid credit: {credits}"))
                            courses_skipped += 1
                            continue
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f"Skipping invalid credit (not a number): {credits}"))
                        courses_skipped += 1
                        continue

                    print(f"Subject: {subject}")
                    print(f"Code: {code}")
                    print(f"Credits: {credits}")
                    print(f"Name: {course_name}")

                    # --- Saving to the Database (remains the same) ---
                    try:
                        course_obj = Course.objects.get(subject=subject, code=code)
                        if course_obj.name != course_name or course_obj.credit != credits:
                            course_obj.name = course_name
                            course_obj.credit = credits
                            course_obj.save()
                            self.stdout.write(self.style.MIGRATE_HEADING(f"Updated: {course_obj}"))
                            courses_updated_count += 1
                        else:
                            self.stdout.write(self.style.NOTICE(f"Existing: {course_obj} (no changes needed)"))

                    except Course.DoesNotExist:
                        courses_to_create.append(
                            Course(
                                subject=subject,
                                code=code,
                                name=course_name,
                                credit=credits
                            )
                        )                
                else:
                    print("Could not find the h3 tag with class 'text-lg'")  
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing listing: {e} - HTML: {course_listings.get_text(strip=True)[:100]}..."))
                courses_skipped_count += 1
                continue

        # --- Bulk Create New Courses (remains the same) ---
        if courses_to_create:
            try:
                with transaction.atomic():
                    created_objects = Course.objects.bulk_create(courses_to_create, ignore_conflicts=True)
                    for course in created_objects:
                        self.stdout.write(self.style.SUCCESS(f"Created new: {course}"))
                    courses_created = len(created_objects)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error during bulk creation: {e}"))
                courses_skipped += len(courses_to_create)
                courses_created = 0
        else:
            courses_created = 0              

        self.stdout.write(self.style.SUCCESS(f"Scraping completed."))
        self.stdout.write(f"Total courses created: {courses_created}")
        self.stdout.write(f"Total courses updated: {courses_updated}")
        self.stdout.write(f"Total courses skipped/failed: {courses_skipped}")