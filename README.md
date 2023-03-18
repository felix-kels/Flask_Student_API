# Student-API

## Aim
Using [Python](https://www.python.org/), [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/), [SQLite3](https://www.sqlite.org), and [Swagger UI](https://swagger.io/tools/swagger-ui/) to build a student management API.

## Summary
This project is a Flask-based web application that provides a simple API for managing user authentication and registration. The API allows users to create new accounts, log in, log out, and update their profile information. The application is built with Python and makes use of Flask and Flask-RESTful libraries to provide RESTful API endpoints. It also makes use of JWT tokens to manage user authentication and authorization. The application is designed to be easily extendable and customizable, allowing developers to build on top of the existing functionality to create more complex applications.


## Built With
- [Python](https://www.python.org/)
- [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/)
- [Flask-JWT](https://flask-jwt-extended.readthedocs.io/en/stable/)



# Getting Started
## Installation
Install with pip:
```
pip install -r requirements.txt
```

## Setup and Configuration

### `.env` Configuration
Create a .env file with these configurations:
```

FLASK_DEBUG=<True/False>
FLASK_APP=app.py
SECRET_KEY=<your secret key>
DATABASE_URL = <database URL>
JWT_SECRET_KEY = <JWT secrete key>
ALGORITHM = <hashing algorithm>
ACCESS_TOKEN_EXPIRES_MINUTES = <expiration time of the access and refresh tokens>

```  
Note: The `DATABASE_URL` setting is not required but it must have a value even if an arbitrary value for your app to run during development and testing. But during production, this must be set to a valid database URL.  


# How to Run
## Clone the repository
git clone https://github.com/felix-kels/Flask_Student_API.git

## Navigate to the root directory of the application
cd Flask_Student_API

## Create a virtual environment and activate it
python3 -m venv venv. Then run the following: 
source venv/bin/activate (for Linux or macOS)
 OR venv\Scripts\activate.bat (for Windows)
 
## Install the required packages
pip install -r requirements.txt

## Set the Flask app environment variable
#### Windows
set FLASK_APP=run.py 
#### Mac or Linux
export FLASK_APP=run.py


## Create the database tables
flask db upgrade


## Run the application
flask run


## Testing
There are a total of 7. In the terminal, run `pytest` or `pytest -v`.

## Contact
- Mail: kelechifelix9065@gmail.com
- GitHub: [felix-kels](https://github.com/felix-kels)

## Acknowledgements
- [AltSchool Africa](https://www.altschoolafrica.com/)
- [Caleb Emelike](https://github.com/CalebEmelike)
