import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)  # these two lines make it so that the columns are shown in full 
from . import w2vsemanalysis as w2v# normalize, create_w2v_vector
from . import collect_metadata as cm# get_movies
from .df import df
import numpy as np
from numpy import dot
from numpy.linalg import norm
def get_movie_recommendations(movie_name, n_recs):
    global df
    movies = cm.get_movies([movie_name])
    movie = movies[0]
    if not movie.title:
        new_df = None
        return
    df_row = movie.get_df_row()
    new_df = pd.concat([df, df_row.to_frame().T], ignore_index=True)
    new_df.dropna(axis=0, inplace=True, subset=new_df.columns.difference(['country'])) # drop rows with at least one missing values with the exception of specified columns
    new_df.reset_index(drop=True, inplace=True)
    new_df["vote_average"] = w2v.normalize(new_df["vote_average"])
    new_df["vote_count"] = w2v.normalize(new_df["vote_count"])
    new_df["release_year"] = w2v.normalize(new_df["release_year"])
    # new_df = w2v.normalize_onehots(new_df)
    cmp_movie = new_df.iloc[-1:]
    new_df = w2v.create_w2v_vector(cmp_movie, new_df)
    feature_df = new_df.drop(columns=["country", 'tmdb_id', 'description', 'title', 'poster'])
    cmp_movie = feature_df.iloc[-1:]
    feature_df.drop(feature_df.tail(1).index,inplace=True)
    result = recommend(feature_df, cmp_movie, n_recs)
    recommended_movies = []
    for i in result.index:
        recommended_movies.append(new_df.loc[i])
        # print(new_df.iloc[i])
    return recommended_movies




# df.sort_values(by=['similarity_score'], inplace=True, ascending=False)


def cosine_sim(v1,v2):
        '''
        This function will calculate the cosine similarity between two vectors
        '''
        return sum(dot(v1,v2)/(norm(v1)*norm(v2)))
    

def recommend(new_df, comparison, n_rec):
        # calculate similarity of input book_id vector w.r.t all other vectors
        inputVec = comparison.values
        new_df['sim']= new_df.apply(lambda x: cosine_sim(inputVec, x.values), axis=1)
        # returns top n user specified books
        return new_df.nlargest(columns='sim',n=n_rec)
    
    # result.loc[i]['title'] = df.loc[i]['title']
    # result.loc[i]['description'] = df.loc[i]['description']
    
# print(result)
