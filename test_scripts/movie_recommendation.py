import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)  # these two lines make it so that the columns are shown in full 
from . import w2vsemanalysis as w2v# normalize, create_w2v_vector
from . import collect_metadata as cm# get_movies
import numpy as np
from numpy import dot
from numpy.linalg import norm
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './tmdb_data_2.csv')

df = pd.read_csv(filename)
def get_movie_recommendations(movie_name, n_recs):
    global df
    movies = cm.get_movies([movie_name])
    movie = movies[0]
    df_row = movie.get_df_row()
    df = pd.concat([df, df_row.to_frame().T], ignore_index=True)
    df.dropna(axis=0, inplace=True, subset=df.columns.difference(['country'])) # drop rows with at least one missing values with the exception of specified columns
    df.reset_index(drop=True, inplace=True)
    df["vote_average"] = w2v.normalize(df["vote_average"])
    df["vote_count"] = w2v.normalize(df["vote_count"])
    df["release_year"] = w2v.normalize(df["release_year"])
    cmp_movie = df.iloc[-1:]
    df = w2v.create_w2v_vector(cmp_movie, df)
    feature_df = df.drop(columns=["country", 'tmdb_id', 'description', 'title', 'poster'])
    cmp_movie = feature_df.iloc[-1:]
    result = recommend(feature_df, cmp_movie, n_recs)
    recommended_movies = []
    for i in result.index:
        recommended_movies.append(df.loc[i])
        print(df.loc[i])
    return recommended_movies




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
    
    # result.loc[i]['title'] = df.loc[i]['title']
    # result.loc[i]['description'] = df.loc[i]['description']
    
# print(result)