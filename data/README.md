# Contains all the scraped data.

USE `rf_data.csv`. It is the most current of the data files and contains columns 

`title year genre country url poster-path description vote_average vote_count`

### Column explanations
    url: the rarefilmm page for the movie
    poster-path: the image on each rarefilmm page for the movie
    description: the movie overview on rarefilmm
    vote_average: tmdb's rating
    vote_count: tmdb's vote count

This file is a combination of `cleaned_titles_data.csv` and `cleaned_urls.csv`, and then everything after that (poster-url, description, vote_average, vote_count) has been scraped in Jupyter Notebook separately.
