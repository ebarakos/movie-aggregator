# MovieRama #

The project was created with emphasis on the functionality of the required features along with the robustness of the system.

The underlying concept is the following:

* For each source(rotten tomatoes or the movie db) API call, we get the list of the movie IDs(as they are declared in each source). Then we check our database to see if the pair [ID,source] is already cached. If yes, we get the stored movie object. If not, we create it with the data provided from the source API and afterwards we store it in our database.

* When we perform a text search, if some of the two sources are not responding accordingly(which can be simulated by altering the base urls in the backend/config.py file), we search if the given text exists in the titles of our cached movie objects, and if yes, we return these.

* The next step is to aggregate the fetched(from API's or database either) movie objects according to specifications. Two movies are considered identical, if their title and year are exactly matched. The starring actors are the combination of unique actor names from both sources.

* Finally we return a JSON response with the aggregated result.

The frontend that consumes the API is a very simple and separate application. 


# Instructions for setting up MovieRama #
The application was created and tested on Ubuntu, but the app can be set up on every operating system by running the following commands on the command line.

### Requirements: 
[Python 2.7.9 or above (from Python 2 versions)](https://www.python.org/downloads) 

Includes pip package manager(Note: you can also use previous python versions, but you must ensure that you also have pip package manager installed. 2.7.9 and above comes with pip included)

* Clone the existing project

* Navigate inside the cloned folder and run
`pip install -r requirements.txt`
(Note: For linux users: if you get access problems, try to run it as superuser. For windows users: You may need to add the path containing pip in your installation to your environment PATH variable. Any user: You can also use virtualenv, but is not necessary)

* After installing the dependencies, run the following sequence of commands:

`python manage.py migrate`

`python manage.py runserver`

You must now have the API server up and running

You can view the API by typing http://localhost:8000/search/<text to search> or http://localhost:8000/now_playing accordingly.
(Note that a convenient view created by django-rest-framework will be displayed. If you want to get the raw json, concatenate /?format=json to the end of the previous urls, for e.g http://localhost:8000/search/star%20wars/?format=json)

* In order to start the web app, start a new terminal, navigate inside the folder named "frontend"  and run 
`python -m SimpleHTTPServer 8080`
(You can also use as an alternative any simple http server of your choice, and/or change the port accordingly)

* To see the frontend web application in your browser, go to http:/localhost/8080

In case you want to clear the cache/database, navigate to the base folder and run the command 
`python manage.py flush`
