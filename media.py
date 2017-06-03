# Author : Sheena Elveus

import webbrowser

class Movie():
    def __init__(self, movie_id, movie_title, movie_storyline, poster_image, trailer_youtube, release_date, runtime, genres, cast):
        self.movie_id = movie_id
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube
        self.release_date = release_date
        self.runtime = runtime
        self.genres = genres
        self.cast = cast


    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)

