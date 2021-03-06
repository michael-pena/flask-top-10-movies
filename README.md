
# Top 10 Movies 

Python web application that uses flask, wtforms, requests, sqlite, and the The [The Movie Database API](https://developers.themoviedb.org/3/getting-started/introduction)  to create a personal top 10 movies list. This is a CRUD app that allows a user to search, add, and rank movies and store them into a sqlite database. The site displays each movie's poster, year released, and description. Each movie is also ranked dynamically based on the user's personal score of the movie.


## Demo

#### Viewing Added Movies
<img src="https://raw.githubusercontent.com/michael-pena/flask-top-10-movies/master/index.gif"  width=650>

#### Adding and Reviewing
<img src="https://raw.githubusercontent.com/michael-pena/flask-top-10-movies/master/add.gif"  width=650>


## Install
Git clone this repo and run the Flask application.
```bash
pip3 install -r requirements.txt
export FLASK_APP=main
flask run
```
