# Diving School Database Frontend App with Python, Tkinter, PostgreSQL
 This app is made for the Database Management course assignment. Language is Turkish.
## Folder organization:

* On main page there are two python files: the first is the main file **script.py** for running the app. The second is **backend.py** providing connection of the frontend to PostgreSQL database.
* In the folder **app** there are other python files related to database tables. They are **student.py, program.py, group.py, trainer.py**

## App screenshot samples
#### Main page
![01](https://user-images.githubusercontent.com/46975718/107482424-b3be7c00-6b90-11eb-98eb-09c43a0cc912.JPG)

#### Instructors table - view, add, update, delete
![eg0](https://user-images.githubusercontent.com/46975718/107482525-db154900-6b90-11eb-81b5-ad7af93dbe99.JPG)
![eg1](https://user-images.githubusercontent.com/46975718/107482547-e2d4ed80-6b90-11eb-9002-69e6bb0bed74.JPG)
![eg2](https://user-images.githubusercontent.com/46975718/107482550-e36d8400-6b90-11eb-87a9-e76f2fe07efa.JPG)
![eg3](https://user-images.githubusercontent.com/46975718/107482552-e4061a80-6b90-11eb-8505-b4f257510518.JPG)

#### Groups' students table - view, add, delete, triggers
![grp_ogr0](https://user-images.githubusercontent.com/46975718/107482707-1e6fb780-6b91-11eb-9530-3ec7ba53be3a.JPG)
![grp_ogr1](https://user-images.githubusercontent.com/46975718/107482711-1f084e00-6b91-11eb-9311-852de4680a09.JPG)
![grp_ogr2](https://user-images.githubusercontent.com/46975718/107482712-1f084e00-6b91-11eb-9325-0031df8ada18.JPG)
![grp_ogr5](https://user-images.githubusercontent.com/46975718/107482715-1fa0e480-6b91-11eb-80c4-a23726b2ad9e.JPG)

## Instructions on how to run the app on local:
To run on your local machine:
1. Check if Python is installed by typing in command prompt `python`. The version of python on which this app is developed is Python 3.8.1.
2. Create a virtualenv "venv" with `python -m venv virtual`. If you do not have
    virtualenv python package installed type `pip install virtualenv`. If pip is not installed, do so by `python get-pip.py`.
    Your virtual environment folder is now **virtualenv**.
3. Activate virtual environment with `source virtual/Scripts/activate`.
4. Install the requirements with `pip install -r requirements.txt`.
5. Run the application with `python script.py`.
6. If you install new packages during app development, add those to requirement.txt file 
   by `pip freeze > requirements.txt`.

## PotgreSQL to Heroku
* On Windows: ***Remember to update your PATH environment variable to add the bin directory of your Postgres installation. The directory will be similar to this: `C:\Program Files\PostgreSQL\<VERSION>\bin`. If you forget to update your PATH, commands like heroku pg:psql won’t work.***
* Push:
    ```
    heroku pg:push diving_school 'DATABASE_URL' --app divingschooldb
    ```
* Troubleshooting:
    ```
    pg_dump -f diving_school.dump -Fc --no-acl -no-owner -h localhost -U postgres --schema=public diving_school

    heroku config:get DATABASE_URL --app divingschooldb

    pg_restore --verbose --no-acl --no-owner -U lmgcolusndmjrc -h ec2-3-233-206-99.compute-1.amazonaws.com -p 5432 -d dfie71fcq48391 < diving_school.dump
    ```
* Connecting in Python
    ```
    pip install psycopg2-binary
    ```
