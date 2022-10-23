
import spacy
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('../lib')
from collect_metadata import get_movies, tmdb_genres

nlp = spacy.load('en_core_web_md')

df = pd.read_csv('../data/rf_data.csv')
print(df.shape) # (2771, 9)

df.dropna(axis=0, inplace=True) # drop rows with at least one missing value
print(df.shape) # (2757, 9), removed 14 rows


descriptions = df['description']
titles = df['title']


def create_w2v_vector(main_desc, df):

  descriptions = df['description']
  docs = [nlp(' '.join([str(t) for t in nlp(description) if t.pos_ in ['NOUN', 'PROPN']])) for description in descriptions]
  movie_name = main_desc
  movie = get_movies([movie_name])
  movie_nlp = nlp(' '.join([str(t) for t in nlp(movie[0].overview) if t.pos_ in ['NOUN', 'PROPN']]))

  similarity = []
  new_df = pd.DataFrame()
  new_df['title'] = df['title']
  new_df['description'] = df['description']
  for i in range(len(docs)):
    similarity.append(movie_nlp.similarity(docs[i]))

  new_df['similarity_score'] = similarity

  pd.set_option('display.max_colwidth', None)
  pd.set_option('display.max_columns', None)  # these two lines make it so that the columns are shown in full

  new_df.sort_values(by=['similarity_score'], inplace=True, ascending=False)
  print(new_df.head(20))
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


from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder



def onehot_encode(data):
  # integer encode
  values=data
  label_encoder = LabelEncoder()
  integer_encoded = label_encoder.fit_transform(values)
  print('test2')
  # binary encode
  onehot_encoder = OneHotEncoder(sparse=False)
  integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
  onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
  print(onehot_encoded)
  print('test3')
  # invert first example
  inverted = label_encoder.inverse_transform([argmax(onehot_encoded[0, :])])
  print(inverted)
  return {'onehot': onehot_encoded, 'label': inverted}
  
  
genres = df['genre']
print('test1')
print(genres.iloc[0])
print('test2.5')
print(tmdb_genres)
genre_names = [genre['name'] for genre in tmdb_genres]
print(genre_names)
onehot_ex = onehot_encode(genre_names)
print(onehot_ex)
print(onehot_ex['onehot'])
# df['genre'] = df.apply(lambda row: , axis=1)