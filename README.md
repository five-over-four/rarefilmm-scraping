# Rarefilmm scraping

[Here](http://rarefilmm.com/) is the website we're using. A directory of old and rare films. Note that this site *does* host some torrents to the films, but as long as we're only taking advantage of the movie information, there shouldn't be any ethical problems in our way.

## The code
We use beautifulsoup4 and pandas mostly. Code's included in the repo. Some movies had 'Arthouse' as the first tag. In those cases, I opted to choose the second tag, which usually ended up being more descriptive, such as 'Drama'.

Occasionally, however, the only tag was 'Arthouse', so it'll occur in the dataset somewhat.

The data is in the form of a csv file with columns "title", "year", "genre", "country". You can import it into pandas with

```
import pandas as pd
pd.read_csv(filename)
pd.head()
```

The head() command just shows the first 5 or so rows.

## Some ideas
One idea for data analysis we discussed was getting the distribution of genres over years and comparing to more popular movies from those eras.

There are also some 'nan' values every now and then, but that just means we'll have more to write about for the report- the process of scraping, the process of cleaning the data, wrangling and whatnot buzzwords we have.

We can also consider other (?) correlations between the datapoints. Years and countries of origin? Even directors? (that code doesn't really work yet)
