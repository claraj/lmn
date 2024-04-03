# LMNOP

## Live Music Notes, Opinions, Photographs


### To install

1. Create and activate a virtual environment. Use Python3 as the interpreter. Suggest locating the venv/ directory outside of the code directory.

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Site at

http://127.0.0.1:8000


### Create superuser

```
python manage.py createsuperuser
```

enter username and password

Then you will be able to use these to log into admin console at

127.0.0.1:8000/admin/

Create some example Artists, Venues, and Shows for the app to use. A user will create Notes using the app. 

### Run tests


```
python manage.py test
```

Or just some of the tests,

```
python manage.py test lmn.tests.test_views
python manage.py test lmn.tests.test_views.TestUserAuthentication
python manage.py test lmn.tests.test_views.TestUserAuthentication.test_user_registration_logs_user_in
```


### Test coverage

From directory with manage.py in it,

```
coverage run --source='.' manage.py test lmn.tests
coverage report
```

### Linting

Ensure requirements are installed, then run,

```
flake8 .
```

Configure linting rules if desired in the .flake8 file. 

### Databases

You will likely want to configure the app to use SQLite locally, and PaaS database when deployed.  
