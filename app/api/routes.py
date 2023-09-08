from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Movie, movie_schema, movies_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/movie', methods = ['POST'])
@token_required
def create_movie (current_user_token):
    title = request.json['title']
    director = request.json['director']
    rating = request.json['rating']
    run_time = request.json['run_time']
    user_token = current_user_token.token

    print(f'Big Test: {current_user_token.token}')

    movie = Movie(title, director, rating, run_time, user_token=user_token)

    db.session.add(movie)
    db.session.commit()

    response =  movie_schema.dump(movie)
    return jsonify(response)

@api.route('/movies', methods = ['GET'])
@token_required
def get_movie(cuurent_user_token):
    a_user = cuurent_user_token.token
    movies = Movie.query.filter_by(user_token = a_user).all()
    response = movies_schema.dump(movies)
    return jsonify(response)

@api.route('/movie/<id>', methods = ['POST', 'PUT'])
@token_required
def update_movie(current_user_token, id):
    movie = Movie.query.get(id)
    movie.title = request.json['title']
    movie.director = request.json['director']
    movie.rating = request.json['rating']
    movie.run_time = request.json['run_time']
    movie.user_token = current_user_token.token

    db.session.commit()
    response = movie_schema.dump(movie)
    return jsonify(response)

@api.route('/movie/<id>', methods = ['DELETE'])
@token_required
def delete_movie(current_user_token, id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    response = movie_schema.dump(movie)
    return jsonify(response)