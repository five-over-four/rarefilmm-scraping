from decouple import config
import os
import tmdbsimple as tmdb
tmdb.API_KEY = config('API_KEY')
external_source = 'imdb_id'
search = tmdb.Search()
search.movie(query='Aerograd')
# movie = tmdb.Movies(603)
print(search.results)