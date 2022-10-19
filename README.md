# Rarefilmm Recommender

[Here](http://rarefilmm.com/) is the website we're using. A directory of old and 'rare/lost' films. Note that this site *does* host some torrents to the films, but as long as we're only taking advantage of the movie information, there shouldn't be any ethical problems in our way.

The goal is to build a film recommender that takes a movie from the user that we'll search for using the TMDB API, and then recommend films from  the Rarefilmm-database, thus exposing the viewer to potentially interesting movies they might've not seen otherwise.

## Project Hierarchy
The project is currently in the form of a Flask application that we're going to try to host on Heroku. The current layout is:
### /data
Contains all of the Rarefilmm data required for our cosine-similarity algorithm, mostly in `rf_data.csv`: title, genre, year, description, poster-urls, urls for page, a one-hot encoding for genres... All kinds of stuff.

### Scrape scripts
These were used at the *very* beginning of the project to gather the initial data that we begun our work with. Not very useful anymore, but formed the foundation of the database.

### /templates/collect_metadata.py
This is used to interface with the TMDB API and the rarefilmm database simulataneously to gather search results. Imported into the `main.py` flask application via `from templates import collect_metadata as cm`

### main.py
Main application. Once the cosine-similarity algorithm is finished, it can be integrated into here and work can begin on CSS-design. It needs to be so that each recommended film is displayed nicely.


## Scraping
We use beautifulsoup4 and pandas mostly. Code's included in the repo. Some movies had 'Arthouse' as the first tag. In those cases, we opted to choose the second tag, which usually ended up being more descriptive, such as 'Drama'. Occasionally, however, the only tag was 'Arthouse', so it appears in the dataset occasionally.

The data is in the form of a csv file with columns "title", "year", "genre", "country", "usl", "poster-path". You can import it into pandas with

```python
import pandas as pd
df = pd.read_csv(path/to/rf_data.csv)
```

## TMDB API
See /lib/ for current work on the backend using the API and instructions on collecting movie data.

## Statistical biases
- The site isn't guaranteed to have randomly sampled 'rare' movies. They can have a bias toward certain time periods or countries or styles, such as german expressionism. We'll therefore have to preface that our findings are in the context of this database.

## Occurrence of each genre by decade on RF (black) vs. TMDB (red)
![](https://i.imgur.com/5dUpIYH.png)
Here, we have at each decade (#genre films / #films) to see the distribution of each genre. For instance, Westerns peak just around 1950s, as they should. Just a fun little visualisation.
