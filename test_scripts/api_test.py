
from collect_metadata import get_movies, tmdb_genres
import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)  # these two lines make it so that the columns are shown in full 


df = pd.read_csv('tmdb_data_3.csv')

df_row = df.loc[df['title'] == 'Jours tranquilles à Clichy']

print(df_row)


