from math import floor
import numpy as np
import spacy
from spacy.tokens import DocBin
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
nlp = spacy.load('en_core_web_md')
from .df import df, docs
# from . import collect_metadata as cm #import get_movies, tmdb_genres
# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_columns', None)  # these two lines make it so that the columns are shown in full


# df = pd.read_csv('../data/rf_data.csv')
# print(df.columns)
# # print(df['country'])
# movie_name = 'Les jeux de la Comtesse Dolingen de Gratz'
# movies = get_movies([movie_name])
# movie = movies[0]
# print('movie:')
# print(movie)
# df_row = movie.get_df_row()
# df = pd.concat([df, df_row.to_frame().T], ignore_index=True)

# last_row = len(df.index)-1


# df.dropna(axis=0, inplace=True, subset=df.columns.difference(['Unnamed: 0', 'tmdb-poster', 'url', 'poster-path', 'genre', 'country'])) # drop rows with at least one missing values
# for i in range(len(df['country'])):
#   print(str(df.iloc[i]['title']) +', ' + str(df.iloc[i]['country'])+', '+str(df.iloc[i]['vote_count'])+', '+str(df.iloc[i]['tmdb-poster']))
# docs = []

def initialize_docs():
  print('preprocess df')
  print(df)
  df.dropna(axis=0, inplace=True, subset=df.columns.difference(['country']))
  df.reset_index(drop=True, inplace=True)
  # global docs
  
  doc_bin = DocBin()
  for doc in nlp.pipe(df['description']):
    doc_bin.add(doc)
  bytes_data = doc_bin.to_bytes()
  # # docs_prc = [nlp(' '.join([str(t) for t in nlp(str(description)) if t.pos_ in ['NOUN', 'PROPN']])) for description in df['description']]
  # print("docs_prc:")
  # for doc in docs_prc:
  #   print(docs)
  # docs_arr_bytes = np.array(docs_prc).tobytes()
  f = open("rf_docs.bin", "wb")
  f.write(bytes_data)
  f.close()
  
  print('preprocess finished')



def create_w2v_vector(cmp_row, df_2): 
  # global docs
  print('len docs: ', len(docs))
  print(docs)
  cmp_row_nlp = nlp(' '.join([str(t) for t in nlp(str(cmp_row['description'])) if t.pos_ in ['NOUN', 'PROPN']]))
  similarity = []
  for i in range(len(docs)):
    similarity.append(cmp_row_nlp.similarity(docs[i]))
  similarity.append(1) # the movie on which recommendations are based has a perfect match with itself
  df_2['similarity_score'] = similarity
  return df_2


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

# def normalize_onehots(df):
  

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


# feature_df = pd.DataFrame()
# # feature_df.drop(["genre", "url", "poster-path", "tmdb-poster"],inplace=True, axis=1)
# df.reset_index(drop=True, inplace=True)

# feature_df["vote_average"] = normalize(df["vote_average"])
# feature_df["vote_count"] = normalize(df["vote_count"])
# feature_df["year"] = normalize(df["year"])
# # print(feature_df)
# print(feature_df.iloc[-1:])

# data = onehot_encode(feature_df, 'country')
# print(data.head(15))
# feature_df.sort_values(by=['year'], inplace=True, ascending=False)