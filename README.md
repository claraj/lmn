# LMNOP

## Live Music Notes, Opinions, Photographs

### Set Up 
Before getting started you will need to get the API key from [TicketMaster](https://developer.ticketmaster.com/products-and-docs/apis/getting-started/). Once you have obtain your API Key, you can set up your environment variable by following the steps below:
- For Mac User:
    - Open Terminal
    - Run `touch ~/.bash_profile; open ~/.bash_profile`
    - In TextEdit, add ` export TICKETMASTER_KEY=<your-api-key-here> `
    - Save the `.bash_profile` file and Quit (Command + Q) Text Edit.

    - Run `source ~/.bash_profile` on terminal to execute
    - Check wheter `TICKETMASTER_KEY` has been added to your `bash_profile` by running `echo $TICKETMASTER_KEY`
- For Windows User:
    - [Here](https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/) is a tutorial on how to set up your environment variable. Set up `TICKETMASTER_KEY` with the API key that you have created.

### To install

1. Create and activate a virtual environment. Use Python3 as the interpreter. Suggest locating the venv/ directory outside of the code directory.


2. Once activated the virtual environment, you will need to run the following command to install the required packages. Once you have installed the required packages, you will need to make migration before running the Django server.

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

3. Once you started the server, you can visit the site via http://127.0.0.1:8000 


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


## What's New

- Get up-to-date show details from TicketMaster
- Share notes on Facebook and Twitter
- Ability to upload photos in your note
- Update your user profile with your favorite artist, venue, and shows
- View other's public user profile 
- Login and Logout message 
- View top shows based on notes rating
- Features to add ratings on your note
- Badges for user that posted the most reviews
- Search your own notes 
- Update/delete your own notes
- View the top rated shows/notes

## Application Snapshots 
- User Profile
![User Profile](/images/UserProfile.png)
- Update User Profile
![Update User Profile](/images/UpdateProfile.png)
- Public Profile
![Public Profile](/images/Profile.png)
- Artist List
![Artist List](/images/artistlist.png)
- Note List
![Note List](/images/notelist.png)
- Venue List
![Venue List](/images/venuelist.png)
- Update Notes
![Update Notes](/images/UpdateNotes.png)
- Note Details
![Note Details](/images/NoteDetails.png)
- Top Shows List
![Top Shows List](/images/topshows.png)
- Login Message
![Login Message](/images/loginmessage.png)
- Logout Message
![Logout Message](/images/logoutmessage.png)

