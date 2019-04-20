## Welcome to the todoAPI

### Main page
![alt text](https://github.com/j-000/apibuilder/blob/master/static/repo_images/c1.PNG "todoAPI main page")

Main features:
+ Website with documentation
+ JWT integration for protected routes
+ User registration and management
+ Reset password option

Stack:
+ Python Flask and Flask-restful for API structure
+ SQLAlchemy (this example uses an sqlite db but could integrate mysql)
+ DB Migrations done via Flask-Migrate
+ [Bootstrap layout from Bootswatch](https://bootswatch.com/flatly)
+ JWT from PYJwt


More details of modules used in the [requirements.txt file](https://github.com/j-000/apibuilder/blob/master/requirements.txt). 

### API guide
![alt text](https://github.com/j-000/apibuilder/blob/master/static/repo_images/c2.PNG "todoAPI API guide")

### Try it locally (on windows 10)
I assume you already have a virtual environment up and running. For details, check [python virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

```
(venv) git clone https://github.com/j-000/todoAPI
(venv) cd todoAPI
(venv) python dbhelper.py
(venv) python app.py
// running on localhost:5000 
```
By default one user and one todo are created when `(venv) python dbhelper.py` is ran. This user's details are:
```
{
    "username": "test",
    "email" : "test@test.com",
    "password": "test"
}
```

### Testing
Clone the repo and activate the virtual environment. You will need 2 terminals. One to start the server and the other one to run the tests.
In the terminal, start by running:
```
(venv) python dbhelper.py
(venv) python app.py
```
In another temrinal pannel then run:
```
(venv) cd tests
(venv) python test_api.py -v
// (...)
// test_registration_user_exists (__main__.TestEndPoints)
// User exists ... ok
// ----------------------------------------------------------------------
// Ran 4 tests in 6.515s
// OK
```


Feel free to contribute and make suggestions.

### A few ideas for improvement 
- [ ] Comprehensive unit tests
- [ ] Playground area to test the API
- [ ] Content managemen system / admin area to manage the API guide