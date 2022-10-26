import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)  # these two lines make it so that the columns are shown in full 
from w2vsemanalysis import normalize, create_w2v_vector, nlp
from collect_metadata import get_movies
import numpy as np
from numpy import dot
from numpy.linalg import norm

df = pd.read_csv('tmdb_data.csv')

movie_name = 'The Godfather'
movies = get_movies([movie_name])
movie = movies[0]
df_row = movie.get_df_row()
df = pd.concat([df, df_row.to_frame().T], ignore_index=True)

df.dropna(axis=0, inplace=True, subset=df.columns.difference(['country'])) # drop rows with at least one missing values with the exception of specified columns
df.reset_index(drop=True, inplace=True)
df["vote_average"] = normalize(df["vote_average"])
df["vote_count"] = normalize(df["vote_count"])
df["release_year"] = normalize(df["release_year"])





cmp_movie = df.iloc[-1:]
df = create_w2v_vector(cmp_movie, df)

feature_df = df.drop(columns=["country", 'tmdb_id', 'description', 'title'])
cmp_movie = feature_df.iloc[-1:]
print(feature_df)
# df.sort_values(by=['similarity_score'], inplace=True, ascending=False)


def cosine_sim(v1,v2):
        '''
        This function will calculate the cosine similarity between two vectors
        '''
        return sum(dot(v1,v2)/(norm(v1)*norm(v2)))
    

def recommend(df, comparison, n_rec):
        # calculate similarity of input book_id vector w.r.t all other vectors
        inputVec = comparison.values
        print('inputvec: ', inputVec)
        print('inputvec shape: ', inputVec.shape)
        df['sim']= df.apply(lambda x: cosine_sim(inputVec, x.values), axis=1)

        # returns top n user specified books
        return df.nlargest(columns='sim',n=n_rec)
    
result = recommend(feature_df, cmp_movie, 10)
print(result)
print('index:')
print(result.index)
for i in result.index:
    print(df.loc[i])
    # result.loc[i]['title'] = df.loc[i]['title']
    # result.loc[i]['description'] = df.loc[i]['description']
    
# print(result)