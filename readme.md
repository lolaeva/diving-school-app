## Diving School Database App with Python, Tkinter, PostgreSQL
* Folder organization:
    * On main page there are two python files: the first is the main file `script.py` for running the app. The second is `backend.py`providing connection of the frontend to PostgreSQL database.
    * In the folder `app` there are other python files related to database tables. They are `student.py`, `program.py`,`group.py`, `trainer.py`
* IMPORTANT: Portable database is yet to be included so many functions are not runnable yet.

## Instructions on how to run the app on local:
To run on your local machine:
1. Install Python 3.8.1
2. Create a virtualenv "venv" with 'python -m venv virtual'. If you do not have
    virtualenv python package installed type 'pip install virtualenv'
3. Activate virtual environment with 'source virtual/Scripts/activate'
4. Install the requirements with 'pip install -r requirements.txt'
5. Run the application with 'python script.py'