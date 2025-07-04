# backend/scraper/management/commands/scrape_courses.py

# Add scraper to sys.path
import os
import sys
import inspect
commands = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
course_planner = os.path.dirname(os.path.dirname(os.path.dirname(commands)))
sys.path.insert(0, course_planner) 
import requests
import re # Import for regular expressions
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction # Import transaction for atomicity
import scraper.management.commands.prereq_utility as util # Import util for prereq parsing
import json # Import json for storing prereqs/coreqs in db
from scraper.models import Course # Import Course model


class Command(BaseCommand):
    help = 'Scrapes course data from a specified UBC Course Calendar URL and saves it to the database.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='The URL of the course catalog to scrape')

    def handle(self, *args, **options):
        url = options['url'] if 'url' in options else 'https://vancouver.calendar.ubc.ca/course-descriptions/subject/cpscv'

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
        
        course_listings = soup.find_all('li') # Returns a list
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
                course_elem = listing.find('article', class_="node--type-course")
                if course_elem:

                    title_elem = course_elem.find('h3', class_='text-lg') 
                    desc_elem = course_elem.find("p", class_="mt-0")
                    

                    if title_elem:
                        # 1. Extract the Course Name:
                        # The course name is inside the <strong> tag.
                        name_tag = title_elem.find('strong')
                        course_name = name_tag.get_text(strip=True) if name_tag else ""

                        # 2. Get the text before the <strong> tag:
                        # This part contains "CPSC_V 100 (3)"
                        pre_name_text = title_elem.get_text(separator=' ', strip=True).replace(course_name, '').strip()

                        # 3. Parse the pre_name_text to get subject, code, and credits:
                        # Pattern: (Subject) (Code) [(Credits)]
                        # CPSC_V 100 (3)
                        match = re.match(r'([A-Z_]+)\s+(\d+)\s+\((\d+)(?:-\d+)?\)', pre_name_text)

                        subject = ""
                        code = None
                        credits = None
                        desc = ""
                        prereqs = None
                        coreqs = None

                        if desc_elem:
                            # Get text from the paragraph (this includes course desc, prereqs, coreqs)
                            desc_text = desc_elem.get_text()

                            # Separate description from prereqs and coreqs
                            info = util.course_info(desc_text)
                            
                            desc = info[0]
                            prereq = info[1]
                            coreq = info[2]
                            
                            # Make prereqs into dictionary
                            if prereq is not None:
                                prereqs = util.split_by_option(prereq)

                                for op, req in prereqs.items():
                                    all_of = re.split(" and ", req)

                                    prereqs[op] = util.req_dict(all_of)
                            else:
                                prereqs = {"(a)" : {"all of" : "None"}}

                            # Make coreqs into dictionary
                            if coreq is not None:
                                coreqs = util.split_by_option(coreq)

                                for op, req in coreqs.items():
                                    all_of = re.split("and", req)

                                    coreqs[op] = util.req_dict(all_of)
                            else:
                                coreqs = {"(a)" : {"all of" : "None"}}

                            coreqs = json.dumps(coreqs)
                            prereqs = json.dumps(prereqs)
                        else:
                            print("Could not find the p tag with class 'mt-0'")

                        if match:
                            subject = match.group(1) # CPSC_V
                            code = int(match.group(2)) # 100
                            credits = int(match.group(3)) # 3

                        # to strip "_V" from the subject:
                        subject = subject.split('_')[0] if '_' in subject else subject
                    
                        # Type validation
                        if not (len(subject) == 4 and subject.isalpha()): # Assuming 4-letter alphabetic subject
                            self.stdout.write(self.style.WARNING(f"Skipping invalid subject format: {subject}"))
                            self.stdout.write(self.style.WARNING(f"Course element HTML:\n{listing.prettify()}\n"))
                            courses_skipped += 1
                            continue
                        # a lot of courses getting skipped for this reason, need to find bug...

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
                            credits = int(credits) # may have errors since some courses have credits format 3-12 for example
                            if credits < 0: 
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
                        print(f"Description: {desc}")
                        print(f"Prereqs: {prereqs}")
                        print(f"Coreqs: {coreqs}")
                        
                        # Saving to the Database
                        try:
                            course_obj = Course.objects.get(subject=subject, code=code)
                            if course_obj.name != course_name or course_obj.credit != credits:
                                course_obj.name = course_name
                                course_obj.credit = credits
                                course_obj.desc = desc
                                course_obj.prereqs = prereqs
                                course_obj.coreqs = coreqs
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

        # Bulk Create New Courses 
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