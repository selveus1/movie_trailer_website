# Author : Sheena Elveus
'''
    This file loads the movies into a list and
    sends that list to fresh_tomatoes.py to be
    display in the generated HTML file.
'''

import media
import fresh_tomatoes
import api_key
import urllib
import json


# format a query to get movie details
def create_details_url(movie_id):
    url_p1 = "https://api.themoviedb.org/3/movie/"
    url_p2 = "?api_key="
    url_p3 = "&language=en-US"

    query = url_p1 + str(movie_id) + url_p2 + api_key.get_api_key() + url_p3

    return query


# format a query to get all videos associated with a movie
def create_video_url(movie_id):
    url_p1 = "https://api.themoviedb.org/3/movie/"
    url_p2 = "/videos?api_key="
    url_p3 = "&language=en-US"

    query = url_p1 + str(movie_id) + url_p2 + api_key.get_api_key() + url_p3

    return query


# format a query to get case members of a movie
def create_credits_url(movie_id):
    url_p1 = "https://api.themoviedb.org/3/movie/"
    url_p2 = "/credits?api_key="

    query = url_p1 + str(movie_id) + url_p2 + api_key.get_api_key()

    return query


# format a query to get the poster image of a movie
def create_poster_url(poster_img):
    return "https://image.tmdb.org/t/p/original/" + poster_img


# format a query to get the Youtube trailer for a move
def create_youtube_url(youtube_key):
    url_p1 = "https://www.youtube.com/watch?v="
    return url_p1 + youtube_key


# send a query and get results from themoviedb.org
def send_query(query):
    connection = urllib.urlopen(query)
    output = connection.read()
    json_output = json.loads(output)
    connection.close()
    return json_output


# convert a dict of genres to list
def parse_genres(genres):
    genre_list = []
    for i in range(0, len(genres)):
        genre_str = genres[i]['name'].encode("ascii")
        genre_list.append(genre_str)

    return ', '.join(genre_list)


# convert a dict of cast members to a list
def parse_cast(cast):
    cast_list = []
    for i in range(0, 5):
        name = cast[i]['name'].encode('utf-8')
        cast_list.append(name)

    return ', '.join(cast_list)


# create and load the moves to be shown in on the site
def load_movies():
    movies = []

    ''' This list contains the movies IDs provided by themoviedb.org. These IDs
        can be used to retrive all information about the movies.
        The list of IDs correspond to this list:
        movies = ["Inception", "The Adjustment Bureau", "The Avengers", "RocknRolla",
              "The Dark Knight","Terminator 2", "Pride and Prejudice 2005", "Jurassic Park",
              "Enron: The Smartest Guys in the Room","Bridget Jones's Diary", "Ghost",
              "Kill Bill, Volume 1"]
    '''
    movie_ids = [27205, 38050, 24428, 13809, 155, 280, 4348, 329, 13020, 634, 251, 24]

    for i in range(0, len(movie_ids)):
        # format queries to send themoviedb.org
        m = movie_ids[i]
        details_query = create_details_url(m)
        trailer_query = create_video_url(m)
        credits_query = create_credits_url(m)

        # send details query to themoviedb.org and get back results
        parsed_details = send_query(details_query)
        parsed_trailer = send_query(trailer_query)
        parsed_cast = send_query(credits_query)

        # format poster url
        poster_url = create_poster_url(parsed_details['poster_path'])

        # grab trailer details with movie_id
        youtube_url = create_youtube_url(parsed_trailer['results'][0]['key'])

        # parse genre details
        genres = parse_genres(parsed_details['genres'])

        # get top 5 billed actors/actresses
        cast = parse_cast(parsed_cast['cast'])

        # create movie object
        fav_movie = media.Movie(m, parsed_details['title'], parsed_details['overview'].encode('utf8'),
                                poster_url, youtube_url, parsed_details['release_date'],
                                parsed_details['runtime'], genres, cast)

        # add the movie to the list
        movies.append(fav_movie)

    return movies


fav_movies = load_movies()

fresh_tomatoes.open_movies_page(fav_movies)

