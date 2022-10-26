from math import floor
import numpy as np
import spacy
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
# sys.path.append('../templates')
from collect_metadata import get_movies, tmdb_genres
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)  # these two lines make it so that the columns are shown in full
nlp = spacy.load('en_core_web_md')

df = pd.read_csv('../data/rf_data.csv')
print(df.columns)
# print(df['country'])
movie_name = 'Les jeux de la Comtesse Dolingen de Gratz'
movies = get_movies([movie_name])
movie = movies[0]
print('movie:')
print(movie)
df_row = movie.get_df_row()
df = pd.concat([df, df_row.to_frame().T], ignore_index=True)

last_row = len(df.index)-1


df.dropna(axis=0, inplace=True, subset=df.columns.difference(['Unnamed: 0', 'tmdb-poster', 'url', 'poster-path', 'genre', 'country'])) # drop rows with at least one missing values
for i in range(len(df['country'])):
  print(str(df.iloc[i]['title']) +', ' + str(df.iloc[i]['country'])+', '+str(df.iloc[i]['vote_count'])+', '+str(df.iloc[i]['tmdb-poster']))



def create_w2v_vector(movie, df):

  descriptions = df['description']
  docs = [nlp(' '.join([str(t) for t in nlp(description) if t.pos_ in ['NOUN', 'PROPN']])) for description in descriptions]
  movie_nlp = nlp(' '.join([str(t) for t in nlp(movie[0].overview) if t.pos_ in ['NOUN', 'PROPN']]))

  similarity = []
  new_df = pd.DataFrame()
  new_df['title'] = df['title']
  new_df['description'] = df['description']
  for i in range(len(docs)):
    similarity.append(movie_nlp.similarity(docs[i]))

  new_df['similarity_score'] = similarity

  

  new_df.sort_values(by=['similarity_score'], inplace=True, ascending=False)
  return new_df


# def create_heatmap(similarity, cmap = "YlGnBu"):
  #   df = pd.DataFrame(similarity)
  #   df.columns = labels
  #   df.index = labels
  #   fig, ax = plt.subplots(figsize=(5,5))
  #   return sns.heatmap(df, cmap=cmap)

  # for i in range(len(docs)):
  #     row = []
  #     for j in range(len(docs)):
  #         similarity_2 = docs[i].similarity(docs[j])
  #         # print(similarity_2)
  #         row.append(similarity_2)
  #     similarity.append(row)
  # print("ok 2")
  # create_heatmap(similarity)

  # plt.show()


def normalize(data):
    '''
    This function will normalize the input data to be between 0 and 1
    
    params:
        data (List) : The list of values you want to normalize
    
    returns:
        The input data normalized between 0 and 1
    '''
    min_val = min(data)
    if min_val < 0:
        data = [x + abs(min_val) for x in data]
    else:
      data = [x - min_val for x in data]
    max_val = max(data)
    return [x/max_val for x in data]


feature_df = pd.DataFrame()
# feature_df.drop(["genre", "url", "poster-path", "tmdb-poster"],inplace=True, axis=1)
df.reset_index(drop=True, inplace=True)

feature_df["vote_average"] = normalize(df["vote_average"])
feature_df["vote_count"] = normalize(df["vote_count"])
feature_df["year"] = normalize(df["year"])
# print(feature_df)
# print(feature_df.iloc[-1:])

# data = onehot_encode(feature_df, 'country')
# print(data.head(15))
# feature_df.sort_values(by=['year'], inplace=True, ascending=False)