# course-planner


In UBC's switch to Workday, many students found that course planning became frustrating using only Workday's tools. We aim to create a tool that students can use in 
tandem with [UBC Scheduler]('https://ubcscheduler.ca/') to plan their degrees and futures with ease. 


## User Stories

- Input courses users took 
- Given courses taken, produce courses that can be taken in a particular subject or in particular subjects
- Given a new course and courses taken, determine what pre-reqs still need to be taken or if the user can register for the course
- Filter for required courses depending on different degree (BA, BSc, etc.) 
  - Produce courses that are yet to be completed (like degree navigator)
- Filter by subject area (e.g., CPSC)
- Authentication (If have time) Save information that the user has input and searched in the past (data persistence).


## Tech Stack

- Frontend:
  - JavaScript
    - React.js
  - HTML5
  - CSS
- Backend:
  - Python 3.13.3
    - Django for core backend  
    - Selenium for web scraping
