# rarefilmm-scraping/lib contains all custom libraries

Import these using `from lib import filename`

## lib.collect_metadata

**Convention:** `from lib import collect_metadata as cm`.

When importing, remember to set `cm.df = pd.read_csv(file_path_to_rarefilmm_csv)`. This dataframe is used whenever searching *using the dataframe* directly. Remember to also set `cm.API_KEY` to the correct string.

This file contains methods to search movie data from TMDB using the API. There are two ways to do this, both with the function `cm.get_movies()`:

### Searching with search words:

Example: If your search terms are "godfather", "avengers endgame", "taxi driver", "dances with wolves", then you can call

```python
from lib import collect_metadata as cm

cm.API_KEY = api_string
movie_search = ["godfather", "avengers endgame", "taxi driver", "dances with wolves"]
movies = cm.get_movies(movie_search)
```
Each movie in the 'movies' list is a Movie() object, as defined in the collect_metadata file. These have the following properties:
```
movie.title             - simply the name of the film.
movie.genres            - {id1: genre_name1, id2: genre_name2, ...}
movie.overview          - text description of the film.
movie.poster            - IF this exists, url to the poster. otherwise None.
movie.vote_average      - 0 to 10 score on tmdb.
movie.vote_count        - how many votes.
movie.poster            - the url to the poster.
```
You can *print* the movie object to see all of these represented cleanly.

### Searching with the Rarefilmm dataframe:

Example: you want to find the films "La guerre est finie", "You Light Up My Life", "Die große Liebe" from the Rarefilmm dataframe through the TMDB API. In this case, you give 'get_movies()' the pandas dataframe entries instead a list of words:
```python
from lib import collect_metadata as cm
import pandas as pd

cm.API_KEY = api_string
df = pd.read_csv(path_to_rarefilmm_csv)
titles = ["La guerre est finie", "You Light Up My Life", "Die große Liebe"]
movie_search = [df.loc[df["title"] == title] for title in titles]
movies = get_movies(movie_search, from_rarefilmm=True)
```
The reason we use the dataframe instead of search terms is because these films are harder to find and often have difficult titles- using a dataframe row, we have *more information* to compare to the search results: the title, year, genre, and country.

Any dataframe row from `rf_data.csv` will work, eg. you can call 
```python
get_movies([df.iloc[100]], from_rarefilmm=True)
```
