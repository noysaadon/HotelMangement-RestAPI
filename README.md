*** Hotel Management API ***

# Technologies used for this project

We used django 4.1.3, python 3.9.7 in our app.


# Installation

for running our app, You have to install python or anaconda on your pc or server.


1. Install dependencies with pip. (If you are using virtual environment remember to activate it)

    `pip install -r requirements.txt`


2. Perform migrations: 

    `python manage.py makemigrations`

    Or Do the migrations separately in case the command does not fail.

    `python manage.py makemigrations account`

    `python manage.py makemigrations guest`

    `python manage.py makemigrations room`

    And finally create the database.

    `python manage.py migrate`


3. Run the project:

    `python manage.py runserver`

# postgresql
install and create new database as named hotel using pgadmin4

4. Load test data (Optional):

    * In Local:
        `python manage.py loaddata data/room-type.json`

        `python manage.py loaddata data/room.json`

        `python manage.py loaddata data/discount.json`


