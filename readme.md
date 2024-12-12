Quiz app docs:

The Quiz app is comprised of react which is frontend and django where it is the backend.

To run the backend 

1) create a environment variable for the backend (optional but recommended)

- python -m venv venv
- /venv/scripts/activate
- cd quizapp

2) install necessary packages from requirements.txt

- pip install -r requirements.txt

3) configure the database in settings.py

4) make migrations to database

- python manage.py makemigrations
- python manage.py migrate

5) create a user in admin panel to create questions

- python manage.py createsuperuser   

6) run the backend server

- python manage.py runserver

7) go to http://localhost:8000/admin/ to add questions


To run the frontend

1) go to react directory

- cd frontend-quiz

2) install packages

- npm install

3) run the frontend

- npm run dev

3) go to localhost http://localhost:5173/ to access the quiz app.
