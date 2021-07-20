from flask import Flask, render_template, redirect, url_for, request, escape
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, validators
import requests


TMDB_API_KEY = "bd499229ab556e0224f11b8545ab93ef"
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
POSTER_PATH = 'https://image.tmdb.org/t/p/w500'
SEARCH_MOVIE_URL = "https://api.themoviedb.org/3/search/movie?"
MOVIE_INFO_URL = "https://api.themoviedb.org/3/movie"


class EditForm(FlaskForm):
    rating = FloatField('Your Rating Out of 10 e.g. 7.5', [validators.DataRequired()])
    review = StringField('Your Review', [validators.DataRequired()])
    submit = SubmitField("submit")


class AddForm(FlaskForm):
    movie_title = StringField('Movie Title', [validators.DataRequired()])
    submit = SubmitField("submit")


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(80))
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(80), nullable=False)
    img_url = db.Column(db.String(80), nullable=False)


@app.route("/")
def home():
    # query and order by the rating from low to high.
    all_movies = Movie.query.order_by(Movie.rating).all()
    # set the ranking for the movie
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i

    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    edit_form = EditForm()
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    if edit_form.validate_on_submit():
        movie.review = escape(edit_form.review.data)
        movie.rating = escape(edit_form.rating.data)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=edit_form)


@app.route("/add", methods=['POST', 'GET'])
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        movie_title = add_form.movie_title.data
        response = requests.get(url=SEARCH_MOVIE_URL, params={'api_key': TMDB_API_KEY, 'query': movie_title})
        return render_template('select.html', movies=response.json())

    return render_template("add.html", form=add_form)


@app.route("/delete")
def delete():
    movie_id = request.args.get('id')
    movie_delete = Movie.query.get(movie_id)
    db.session.delete(movie_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/select", methods=['POST', 'GET'])
def select():
    return render_template("select.html")


@app.route("/find", methods=['POST', 'GET'])
def find():
    movie_id = request.args.get('id')
    response = requests.get(url=f"{MOVIE_INFO_URL}/{movie_id}", params={"api_key": TMDB_API_KEY, 'language': 'en-US'})
    movie_data = response.json()
    new_movie = Movie(
        title=movie_data['original_title'],
        year=movie_data['release_date'][0:4],
        description=movie_data['overview'],
        img_url=POSTER_PATH+movie_data['poster_path']
    )
    db.session.add(new_movie)
    db.session.commit()
    print(new_movie.id)
    return redirect(url_for('edit', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
