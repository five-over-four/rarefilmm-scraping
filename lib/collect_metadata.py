#!/usr/bin/env python
# coding: utf-8

import requests
from datetime import datetime
import pandas as pd
from difflib import SequenceMatcher

# from lib import collect_metadata as cm
# set to cm.df = pd.read_csv(cleaned_titles_data_filepath)
df = None

# set this when importing.
# cm.API_KEY = api_string
API_KEY = None

# # Functions to fetch movie data

def search_and_parse(request):
    """
    Give search term like "the godfather", returns python list of dictionaries,
    each dictionary its own movie entry.
    """
    result = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={request}")
    text = result.text.replace("false", "False").replace("true", "True").replace("null", "None")
    return eval(text)

def cut_documentaries(req_dict):
    """
    genre_id 99 is a documentary. These sometimes get returned before the actual movie, so
    we cut them out entirely. Seems to work very well.
    """
    results = []
    for item in req_dict["results"]: # we select first page first.
        if 99 not in item["genre_ids"]:
            results.append(item)
    return results

def get_search_results(movie_list):
    """
    This returns search results in a list for each movie. Each entry is
    a list of dictionaries, each its own film entry.
    """
    results = []
    
    for movie in movie_list:
        results.append(cut_documentaries(search_and_parse(movie)))
    return results


# # Metadata extraction

def get_genre_list():
    """
    returns [{"id": 28, "name": "Action"}, ..., {"id": 37, "name": "Western"}]
    """
    req_string = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"
    result = requests.get(req_string)
    text = result.text.replace("false", "False").replace("true", "True").replace("null", "None")
    return eval(text)["genres"]

# you can still get these with the above function if you want, but web requests are slow.
# tmdb_genres = get_genre_list()
tmdb_genres = [{'id': 28, 'name': 'Action'}, {'id': 12, 'name': 'Adventure'}, {'id': 16, 'name': 'Animation'}, \
                {'id': 35, 'name': 'Comedy'}, {'id': 80, 'name': 'Crime'}, {'id': 99, 'name': 'Documentary'}, \
                {'id': 18, 'name': 'Drama'}, {'id': 10751, 'name': 'Family'}, {'id': 14, 'name': 'Fantasy'}, \
                {'id': 36, 'name': 'History'}, {'id': 27, 'name': 'Horror'}, {'id': 10402, 'name': 'Music'}, \
                {'id': 9648, 'name': 'Mystery'}, {'id': 10749, 'name': 'Romance'}, {'id': 878, 'name': 'Science Fiction'}, \
                {'id': 10770, 'name': 'TV Movie'}, {'id': 53, 'name': 'Thriller'}, {'id': 10752, 'name': 'War'}, {'id': 37, 'name': 'Western'}]

def translate_ids_to_genres(ids):
    """
    Takes list of genre_id such as [28, 80] and returns ["Action", "Crime"]
    """
    return [genre["name"] for genre in tmdb_genres if genre["id"] in ids]

def title_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

class Movie:
    """
    A Movie() instance holds all the metadata of a movie, conveniently packaged.
    just call Movie(search_result), where search_result is an element of
    get_search_results(movies).
    """
    def __init__(self, search_results, from_rarefilmm=False, df=None):
        self.df = df # in case we search from the rarefilmm df, then this is the row.
        self.select_movie(search_results, from_rarefilmm) # set self.metadata

        if self.metadata:
            self.extract_data()

        # this happens when the search results on TMDB are empty.
        else:
            self.title = None
            self.genres = None
            self.release_date = None
            self.poster = None
            self.overview = None
            self.vote_average = None
            self.vote_count = None
            if from_rarefilmm: # but we should still set the data by the dataframe.
                self.title = df["title"]
                if df["genre"] == "Sci-Fi": # this exception causes problems.
                    self.genres = {878: "Science Fiction"}
                else:
                    self.genres = {genre["id"]: genre["name"] for genre in tmdb_genres if genre["name"] == df["genre"]}
                self.release_date = df["year"]
                self.poster = df["poster-path"]
        
    def extract_data(self):
        """
        We gather and save all the information about the movie into the Movie object.
        All of this is also stored in self.metadata, but pre-formatted.
        Contains a lot of validation due to missing data in metadata.
        """
        if self.metadata.keys() and self.metadata["genre_ids"]:
            self.genres = {genre_id: genre["name"] for genre_id in self.metadata["genre_ids"] for genre in tmdb_genres if genre["id"] == genre_id}
        else:
            self.genres = None
        self.title = self.metadata["original_title"]
        self.overview = self.metadata["overview"]
        if self.metadata["release_date"]:
            if len(self.metadata["release_date"]) < 10:
                self.release_date = int(self.metadata["release_date"][:4])
            else:
                self.release_date = datetime.strptime(self.metadata["release_date"], "%Y-%m-%d")
        if self.metadata["poster_path"]:
            self.poster = "https://image.tmdb.org/t/p/original" + self.metadata["poster_path"]
        else:
            self.poster = None
        self.vote_average = self.metadata["vote_average"]
        self.vote_count = self.metadata["vote_count"]

    def select_movie(self, search_results, from_rarefilmm):
        """
        if not from rarefilmm, just pick the first one. Otherwise try to match
        production year, title, and genre as well. This should lead to better results.
        Has a bunch of validation due to occasionally missing dictionary keys in results.
        """
        if from_rarefilmm:
            year = self.df["year"]
            genre = self.df["genre"]
            if genre == "Sci-Fi": genre = "Science Fiction"
            best_result = (None, 0)
            
            for result in search_results:
                correct_score = 0
                if "original_title" in result.keys():
                    correct_score += title_similarity(result["original_title"], self.df["title"]) * 2
                if "release_date" in result.keys():
                    if result["release_date"] and int(result["release_date"][:4]) == year:
                        correct_score += 1
                    elif result["release_date"]:
                        correct_score += 1 / (abs(int(result["release_date"][:4]) - year) + 1)
                if "genre_ids" in result.keys() and genre in translate_ids_to_genres(result["genre_ids"]): correct_score += 1
                best_result = (result, correct_score) if correct_score > best_result[1] else best_result
            
            self.metadata = best_result[0]

        else:
            self.metadata = search_results[0]
        
    def __str__(self):
        return f"title: {self.title}\n" + \
                f"genres: {self.genres}\n" + \
                f"release: {self.release_date}\n" + \
                f"vote_average: {self.vote_average}\n" + \
                f"vote_count: {self.vote_count}\n\n" + \
                f"overview: {self.overview}"
    
def get_movies(movie_list, from_rarefilmm=False):
    """
    If NOT from_rarefilmm, movie_list is a list of search terms.
    if IS from_rarefilmm, movie_list is a list of dataframe rows, each its own
    movie entry. for instance, df.loc[df["title"] == "Utz"].
    """
    if from_rarefilmm:
        results = get_search_results([movie["title"] for movie in movie_list])
        return [Movie(result, from_rarefilmm, df.squeeze()) for result, df in zip(results, movie_list)]
    results = get_search_results(movie_list)
    return [Movie(result) for result in results]

# test here if you like.
if __name__ == "__main__":

    from random import randint
    
    # example queries for the API.
    search_terms = ["godfather", "avengers endgame", "taxi driver", "dances with wolves", 
                  "aerograd", "i'm thinking of ending things", "synecdoche", "budapest hotel", "anomalisa",
                  "ikiru", "seven samurai", "akira", "angel's egg", "naked lunch", "videodrome"]
    
    # test print. try different indices, corresponding to the above list.
    movies = get_movies(search_terms)
    print(movies[6])

    # example query for API with rf films. random movies in this test.
    how_many_films = 5
    searches = [df.iloc[randint(0,df.shape[0]-1)] for x in range(how_many_films)]
    movies = get_movies(searches, from_rarefilmm=True)
    print(movies[0])
