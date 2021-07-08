# juvoxa_hospital_system
Simulate a platform to be used by hospitals for managing doctors and patients.


* Steps to Run Project:-
  - Create a virtual environment with python3.6 (python3.6 -m venv env)
  - Activate the environment (source env/bin/activate)
  - Root to project (cd hospital_system)
  - Install all requirements (pip install -r req.txt)
  - Create Database according to the project and set the credentials in settings.py of the project
  - Do initial migrations
       - python manae.py makemigrations
       - python manae.py migrate
  - Access admin pannel by creating a superuser
       - python manage.py createsuperuser 
       - provide role = 1
  - runserver (python manage.py runserver)
 
* Steps if UI breaks
  - Make sure nginx serves from project static file
  - python manage.py collectstatic

* Add Patient Visits
  - There is no way described that how a patient have multiple doctor visits or hospital visits
  - Written a script for creating multiple visit
  - Redirect to hospital_system/app/patient/helpers
  - Follow the written steps 
  - Run script by following command
       - python manage.py shell
       - from apps.patient.helpers import create_patient_visits
       - create_patient_visits()
