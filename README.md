# LMNOP

## Live Music Notes, Opinions, Photographs

### Unexpected Features
- *Style is strange on add note page*
- *Certain browsers -- depending on user -- are not displaying styles*

### Future Development
- *Match page style to Kelsey's UX design*
https://www.figma.com/file/XoJmT6KOsXz4tpTDKhtYed/LMN?node-id=0%3A1

### Credits
- *Pagination made possible by a ridiculously deep rabbit hole of docs and tutorials pagination
 made possible by a ridiculously deep rabbit hole of docs and tutorials 
 (https://www.youtube.com/channel/UCCezIgC97PvUuR4_gbFUs5g)*
- *Extending user modelmade possible by:
https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone*
- *Some css styles exported from figma designs
(https://www.figma.com/file/XoJmT6KOsXz4tpTDKhtYed/LMN?node-id=0%3A1)*
- *link hover styles
(https://css-tricks.com/4-ways-to-animate-the-color-of-a-text-link-on-hover/)*
- *Gradient style creator (https://cssgradient.io/)*
- *Logo designs and other design images from Canva (https://www.canva.com/)*

### To install

1. Create and activate a virtual environment. Use Python3 as the interpreter. Suggest locating the venv/ directory outside of the code directory.

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
if on mac:
  export LMNOP_USER_PW=[password]
elif on windows:
  set LMNOP_USER_PW=[password]
```

Local site at
http://127.0.0.1:8000
Live site at
https://lmnop-312618.uc.r.appspot.com/

### Create superuser

`python manage.py createsuperuser`

enter username and password

will be able to use these to log into admin console at

127.0.0.1:8000/admin


### Run tests


```
python manage.py test lmn.tests
```

Or just some of the tests,

```
python manage.py test lmn.tests.test_views
python manage.py test lmn.tests.test_views.TestUserAuthentication
python manage.py test lmn.tests.test_views.TestUserAuthentication.test_user_registration_logs_user_in
```


### Functional Tests with Selenium

Make sure you have the latest version of Chrome or Firefox, and the most recent chromedriver or geckodriver, and latest Selenium.

chromedriver/geckodriver needs to be in path or you need to tell Selenium where it is. Pick an approach: http://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path

If your DB is hosted at Elephant, your tests might time out, and you might need to use longer waits http://selenium-python.readthedocs.io/waits.html

Run tests with

```
python manage.py test lmn.tests.functional_tests
```

Or select tests, for example,
```
python manage.py test lmn.tests.functional_tests.HomePageTest
python manage.py test lmn.tests.functional_tests.BrowseArtists.test_searching_artists
```


### Test coverage

From directory with manage.py in it,

```
coverage run --source='.' manage.py test lmn.tests
coverage report
```

### PostgreSQL

Recommend using PaaS Postgres such as Elephant, instead of installing local Postgres.

### Authors
##### Chris Gisala - Grand Note Master
##### Clara James - Base Code Extraordinaire
##### Kelsey Stiff - Supreme UX Chief
##### Mo Sargazi - Rating and Badge Captain
##### Shawn Jones - API Phreak
##### Topanga Gramlich - User Profile Guru
