
from collect_metadata import get_movies, tmdb_genres
import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)  # these two lines make it so that the columns are shown in full 

df = pd.read_csv('../data/rf_data.csv')

series_list = []
for i in range(len(df.index)):
    series_list.append(df.iloc[i])
print(series_list)

tmdb_df =  pd.DataFrame()
tmdb_movies = get_movies(series_list, True)
for movie in tmdb_movies:
    df_row = movie.get_df_row()
    tmdb_df = tmdb_df.append(df_row, ignore_index=True)
    
print(tmdb_df)

tmdb_df.to_csv('tmdb_data_3.csv', index=False)  



