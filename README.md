# Rarefilmm scraping

[Here](http://rarefilmm.com/) is the website we're using. A directory of old and rare films. Note that this site *does* host some torrents to the films, but as long as we're only taking advantage of the movie information, there shouldn't be any ethical problems in our way.

## The code
We use beautifulsoup4 and pandas mostly. Code's included in the repo. Some movies had 'Arthouse' as the first tag. In those cases, I opted to choose the second tag, which usually ended up being more descriptive, such as 'Drama'.

Occasionally, however, the only tag was 'Arthouse', so it'll occur in the dataset somewhat.

The data is in the form of a csv file with columns "title", "year", "genre", "country". You can import it into pandas with

`
import pandas as pd
pd.read_csv(filename)
pd.head()
`

The head() command just shows the first 5 or so rows.
