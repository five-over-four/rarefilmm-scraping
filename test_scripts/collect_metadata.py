#!/usr/bin/env python
# coding: utf-8

import requests
from datetime import datetime
import pandas as pd
import numpy as np
from difflib import SequenceMatcher

# from lib import collect_metadata as cm
# set to cm.df = pd.read_csv(cleaned_titles_data_filepath)
df = None

# set this when importing.
# cm.API_KEY = api_string
API_KEY = '08bfcffdd73f2bfad0410dc1914be2c6'

# # Functions to fetch movie data

def search_and_parse(request):
    """
    Give search term like "the godfather", returns python list of dictionaries,
    each dictionary its own movie entry.
    """
    result = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={request}")
    text = result.text.replace("false", "False").replace("true", "True").replace("null", "None")
    return eval(text)["results"]


def get_detailed_movie_info(id):
    result = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}")
    text = result.text.replace("false", "False").replace("true", "True").replace("null", "None")
    try:
        return eval(text)
    except Exception as e:
        print('Error occurred: ', e)

def cut_documentaries(req_dict):
    """
    genre_id 99 is a documentary. These sometimes get returned before the actual movie, so
    this cuts them out when necessary. If there are only documentary entries, we do not remove them.
    """
    if not req_dict:
        return []

    documentaries = []
    results = []

    for item in req_dict: # we select first page first.
        if 99 not in item["genre_ids"]:
            results.append(item)
        elif 99 in item["genre_ids"]:
            documentaries.append(item)
    return results if results else documentaries

def get_search_results(movie_list, genres=None):
    """
    This returns search results in a list for each movie. Each entry is
    a list of dictionaries, each its own film entry. Note that we only cut
    the documentaries from search results *if* the movie itself is not originally
    a documentary. This is tricky, but we approximate this by cutting docs when
    there are non-docs in the results. Otherwise, no cutting.
    """
    genres = [None]*len(movie_list) if not genres else genres
    results = []
    
    for i, (movie, genre) in enumerate(zip(movie_list, genres)):
        if genre == "Documentary":
            results.append(search_and_parse(movie))
        else:
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

tmdb_countries = ['afghanistan', 'albania', 'algeria', 'angola', 'argentina', 'australia', 'austria', 'belgium', 
                  'bolivia', 'brazil', 'bulgaria', 'burkina faso', 'cameroon', 'canada', 'chile', 'china', 'colombia',
                  "cote d'ivoire", 'cuba', 'czech republic', 'czechoslovakia', 'denmark', 'east germany', 'egypt', 
                  'el salvador', 'estonia', 'finland', 'france', 'georgia', 'germany', 'greece', 'guinea-bissau', 'hong kong',
                  'hungary', 'india', 'indonesia', 'iran', 'ireland', 'israel', 'italy', 'japan', 'kazakhstan', 'latvia', 'lebanon',
                  'lithuania', 'malaysia', 'mexico', 'netherlands', 'new zealand', 'nicaragua', 'norway', 'pakistan', 'palestinian territory',
                  'peru', 'philippines', 'poland', 'portugal', 'romania', 'russia', 'senegal', 'south africa', 'south korea', 'soviet union',
                  'spain', 'sri lanka', 'sudan', 'sweden', 'switzerland', 'syrian arab republic', 'taiwan', 'thailand', 'turkey', 'united kingdom',
                  'united states of america', 'yugoslavia', 'zimbabwe']

def translate_ids_to_genres(ids):
    """
    Takes list of genre_id such as [28, 80] and returns ["Action", "Crime"]
    """
    return [genre["name"] for genre in tmdb_genres if genre["id"] in ids]

def title_similarity(a, b):
    """
    Gives a score 0-1 for how close two titles are to each other.
    """
    return SequenceMatcher(None, a, b).ratio()

class Movie:
    """
    A Movie() instance holds all the metadata of a movie, conveniently packaged.
    just call Movie(search_result), where search_result is an element of
    get_search_results(movies).
    """
    def __init__(self, search_results, from_rarefilmm=False, df=None):
        self.from_rarefilmm = from_rarefilmm
        self.df = df # in case we search from the rarefilmm df, then this is the row.
        self.select_movie(search_results, from_rarefilmm) # set self.metadata

        if self.metadata:
            self.extract_data()
        
        # this happens when the search results on TMDB are empty.
        else:
            self.tmdb_id = None
            self.title = None
            self.genres = None
            self.release_date = None
            self.release_year = None
            self.poster = None
            self.description = None
            self.vote_average = None
            self.vote_count = None
            self.countries = None
            self.genre_onehot = None
            self.countries_onehot = None
            if from_rarefilmm: # but we should still set the data by the dataframe.
                self.title = df["title"]
                if df["genre"] == "Sci-Fi": # this exception causes problems.
                    self.genres = {878: "Science Fiction"}
                else:
                    self.genres = {genre["id"]: genre["name"] for genre in tmdb_genres if genre["name"] == df["genre"]}
                self.release_date = df["year"]
                self.poster = df["poster-path"]
                self.description = df["description"]
        
    def extract_data(self):
        """
        We gather and save all the information about the movie into the Movie object.
        All of this is also stored in self.metadata, but pre-formatted.
        Contains a lot of validation due to missing data in metadata.
        """
        if self.metadata.keys() and self.metadata["genre_ids"]:
            self.genres = {genre_id: genre["name"] for genre_id in self.metadata["genre_ids"] for genre in tmdb_genres if genre["id"] == genre_id}
        elif self.metadata.keys() and self.from_rarefilmm:
            self.genres = {0: self.df["genre"]}
        else:
            self.genres = None
        self.title = self.metadata["original_title"]
        self.description = self.metadata["overview"]
        if self.metadata["release_date"]:
            self.release_year = int(self.metadata["release_date"][:4])
            if len(self.metadata["release_date"]) < 10:
                self.release_date = int(self.metadata["release_date"][:4])
            else:
                self.release_date = datetime.strptime(self.metadata["release_date"], "%Y-%m-%d")
        if self.metadata["poster_path"]:
            self.poster = "https://image.tmdb.org/t/p/original" + self.metadata["poster_path"]
        else:
            if self.from_rarefilmm: # if we can't find poster on TMDB for RF film, use RF poster.
                if pd.isna(self.df["tmdb-poster"]):
                    self.poster = self.df["poster-path"]
                else:
                    self.poster = self.df["tmdb-poster"]
            else:
                self.poster = None
        if self.metadata["production_countries"] and len(self.metadata["production_countries"]) > 0:
            countries = []
            for country in self.metadata["production_countries"]:
                countries.append(country['name'].lower())
            self.countries = countries
        else:
            if df and df["country"]:
                if df["country"] == 'USA':
                    self.countries = ['united states of america']
                elif df["country"] == 'UK':
                    self.countries = ['united kingdom']
                elif df["country"] == 'USSR':
                    self.countries = ['soviet union']
                else:
                    self.countries = [df["country"].lower()]
            else:
                self.countries = None
                   
        self.vote_average = self.metadata["vote_average"]
        self.vote_count = self.metadata["vote_count"]
        self.tmdb_id = self.metadata["id"]
        self.assign_genre_onehot_encoding()
        self.assign_country_onehot_encoding()
        

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
            # the scoring system. max 2 points for title, 1 for genre, 1 for year.
            for result in search_results:
                genre_ids = result["genre_ids"]
                result = get_detailed_movie_info(result['id'])
                if not result:
                    continue
                result['genre_ids'] = genre_ids
                correct_score = 0
                if "original_title" in result.keys():
                    correct_score += title_similarity(result["original_title"], self.df["title"]) * 2
                if "release_date" in result.keys():
                    if result["release_date"] and int(result["release_date"][:4]) == year:
                        correct_score += 1
                    elif result["release_date"]:
                        correct_score += 1 / (abs(int(result["release_date"][:4]) - year) + 1)
                if "production_countries" in result.keys():
                    if len(result["production_countries"])>0:
                        correct_score += title_similarity(result["production_countries"][0]["name"].lower(), self.df["country"])
                if "genre_ids" in result.keys() and genre in translate_ids_to_genres(result["genre_ids"]): correct_score += 1
                # if "production_countries" in result.keys():
                    
                best_result = (result, correct_score) if correct_score > best_result[1] else best_result
            self.metadata = best_result[0]

        else:
            if not search_results:
                self.metadata = None
            else:
                result = get_detailed_movie_info(search_results[0]['id'])
                result['genre_ids'] = search_results[0]['genre_ids']
                self.metadata = result
                
    def get_onehot_genres(self):
        """
        Returns a one-hot encoding of the genres of the film in a list, in alphabetical order as
        in tmdb_genres.
        """
        one_hot = [0 for _ in range(len(tmdb_genres))]
        if not self.genres:
            return one_hot
        for i, genre in enumerate(tmdb_genres):
            if genre["name"] in self.genres.values():
                one_hot[i] = 1
        return one_hot
    
    def get_onehot_countries(self):
        """
        Returns a one-hot encoding of the country of the film in a list, in alphabetical order as
        in tmdb_countries.
        """
        one_hot = [0 for _ in range(len(tmdb_countries))]
        if not self.countries:
            return one_hot
        else:
            for i, country in enumerate(tmdb_countries):
                if country in self.countries:
                    one_hot[i] = 1
            return one_hot
    
    def assign_genre_onehot_encoding(self):
        genre_onehot = {}
        onehot = self.get_onehot_genres()
        for i, genre in enumerate(tmdb_genres):
            genre_onehot[genre["name"]] = onehot[i]
        self.genre_onehot = genre_onehot
        
    def assign_country_onehot_encoding(self):
        country_onehot = {}
        onehot = self.get_onehot_countries()
        for i, country in enumerate(tmdb_countries):
            country_onehot[country] = onehot[i]
        self.countries_onehot = country_onehot
            
    def get_df_row(self):
        try:
            data = {"title": self.title, "description": self.description, "country": self.countries, "tmdb_id": self.tmdb_id, "poster": self.poster, "release_year": self.release_year, "vote_average": self.vote_average, "vote_count": self.vote_count}
            data = {**data, **self.genre_onehot}
            data = {**data, **self.countries_onehot}
            return pd.Series(data=data, index=data.keys())
        except Exception as e:
            print("error happened: ", e)
            return pd.Series(data={"title": self.title}, index=["title"])
        
    def __str__(self):
        return f"title: {self.title}\n" + \
                f"tmdb_id: {self.tmdb_id}\n" + \
                f"genres: {self.genres}\n" + \
                f"release_date: {self.release_date}\n" + \
                f"release_year: {self.release_year}\n" + \
                f"vote_average: {self.vote_average}\n" + \
                f"vote_count: {self.vote_count}\n\n" + \
                f"description: {self.description}\n\n" + \
                f"poster: {self.poster}\n\n" + \
                f"genre_onehot: {self.genre_onehot}\n\n" + \
                f"genre_onehot: {self.countries_onehot}\n\n" + \
                f"country: {self.countries}"
    
def get_movies(movie_list, from_rarefilmm=False):
    """
    If NOT from_rarefilmm, movie_list is a list of search terms.
    if IS from_rarefilmm, movie_list is a list of dataframe rows, each its own
    movie entry. for instance, df.loc[df["title"] == "Utz"] or df.iloc[20].

    Note that you cannot use df.iloc[10:20], they have to be individual rows in a list, so
    [df.iloc[x] for x in range(10,21)] must be used.
    """
    if from_rarefilmm:
        movie_list = [movie.squeeze() for movie in movie_list] # this fixes issues with .loc and .iloc returning different structures.
        results = get_search_results([movie["title"] for movie in movie_list], genres = [movie["genre"] for movie in movie_list])
        return [Movie(result, from_rarefilmm, df.squeeze()) for result, df in zip(results, movie_list)]
    results = get_search_results(movie_list)
    return [Movie(result) for result in results]
