# LMNOP

## Live Music Notes, Opinions, Photographs


### To install

1. Create and activate a virtual environment. Use Python3 as the interpreter. Suggest locating the venv/ directory outside of the code directory.
   
2. Install the requirements given in requirements.txt

```
pip install -r requirements.txt
```

3. Migrate the database

```
python manage.py migrate
```


### Create superuser

Create a superuser, 

```
python manage.py createsuperuser
```

Enter a username and password. Remember the password. If you forget, you can create another superuser with the same command. 

### Run the server 

Run the server, 

```
python manage.py runserver
```

Your site should be visible at http://127.0.0.1:8000

You will be able to the superuser username and password to log into admin console at http://127.0.0.1:8000/admin/

Create some example **Artists**, **Venues**, and **Shows** for the app to use. A user will then be able to create **Notes** using the app. 

When you view the site, you should see artists, venues and shows, and be able to add notes. 

The app allows new users to create accounts, and users can log in, and log out.

### Run tests

```
python manage.py test
```

Or just some of the tests, for example,

```
python manage.py test lmn.tests.test_views
python manage.py test lmn.tests.test_views.TestUserAuthentication
python manage.py test lmn.tests.test_views.TestUserAuthentication.test_user_registration_logs_user_in
```

### Test coverage

The app uses Coverage to generate a test coverage report. 

From directory with manage.py in it,

```
coverage run --source='.' manage.py test lmn.tests
coverage report
```

### Linting

The app uses Flake8 to lint code files. This checks for some (but not all) code quality issues.

```
flake8 .
```

Configure linting rules if desired in the .flake8 file. You may want to list your virtual environment directory if it has a name other than venv, otherwise Flake8 will lint the library files and that isn't necessary. 

A tool called JinjaLint is installed when GitHub actions runs your tests. You may also install this locally, but it's somewhat common to see issues when trying to run it. 

### Databases

The app is configured to use a SQLite database, which is usually sufficent for local development. You will likely want to configure the app to use SQLite locally, and PaaS database when deployed.  
