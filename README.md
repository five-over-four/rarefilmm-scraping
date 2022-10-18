# Rarefilmm Recommender

[Here](http://rarefilmm.com/) is the website we're using. A directory of old and 'rare/lost' films. Note that this site *does* host some torrents to the films, but as long as we're only taking advantage of the movie information, there shouldn't be any ethical problems in our way.

The goal is to build a film recommender that takes a list of movies from the user that we'll search for using the TMDB API, and then recommend films from  the Rarefilmm-database, thus exposing the viewer to potentially interesting movies they might've not seen otherwise.

## Project Hierarchy
### /data
Contains the scraped data. The main file is `rf_data.csv`, which contains all the relevant information. Some others are left behind as backup.
### /lib
Contains at the moment `collect_metadata.py`, which deals with interfacing with the TMDB API and *collating* information from both Rarefilmm and TMDB. May be integrated into a Flask web application, at which point this directory becomes deprecated.
### /scrape_scripts
Contains some of the scripts used to originally gather the data. Much of the collection was done in Jupyter Notebooks, so the code itself isn't stored.
### /test_scripts
Generally miscellaneous scripts from early in the project.

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
