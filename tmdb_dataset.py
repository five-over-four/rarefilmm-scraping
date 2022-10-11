import pandas as pd

df = pd.read_csv("/home/ruby/coding/rarefilmm-scraping/data/tmdb_dataset/movies_metadata.csv", on_bad_lines='skip')

# Download this and extrat into data/tmdb_dataset: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

print(df['revenue'])