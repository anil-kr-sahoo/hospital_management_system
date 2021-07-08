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
       
* Extra Features
  - Home page created for Different User (Hospital, Doctor, Patient).
  - Anyone can see the Hospital list registered with the system.
  - Admin panel integrated, where a super user can create, delete and edit the existing data for all hospital, doctor and patient.
  - In Admin pannel superuser have the search functionality by email, name or phone number of the corresponding users table.
  - Appointment date is one of primary things for a doctor - patient interlink, which is missing in requirement.
  - After a patient login through Appointment date they request a doctor appointment. (Future Aspects)
  - Other Essential fields visualised in Table which not mentioned in requirement. (Appointment Date, Blood Group, Contact Details) 
  - Check added that a patient can't have multiple entry on same day, if doctor and appointment date is there in table.
