
import spacy
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('../lib')
from collect_metadata import get_movies
nlp = spacy.load('en_core_web_md')

df = pd.read_csv('../data/rf_data.csv')
print(df.shape) # (2771, 9)

df.dropna(axis=0, inplace=True) # drop rows with at least one missing value
print(df.shape) # (2757, 9), removed 14 rows


descriptions = df['description']
titles = df['title']

docs = [nlp(' '.join([str(t) for t in nlp(description) if t.pos_ in ['NOUN', 'PROPN']])) for description in descriptions]

# labels = [title for title in titles]
 
 
movie_name = 'shawshank redemption'
movie = get_movies([movie_name])
movie_nlp = nlp(' '.join([str(t) for t in nlp(movie[0].overview) if t.pos_ in ['NOUN', 'PROPN']]))
print(movie[0].overview)
print('---')
def create_heatmap(similarity, cmap = "YlGnBu"):
  df = pd.DataFrame(similarity)
  df.columns = labels
  df.index = labels
  fig, ax = plt.subplots(figsize=(5,5))
  return sns.heatmap(df, cmap=cmap)

similarity = []
new_df = pd.DataFrame()
new_df['title'] = df['title']
new_df['description'] = df['description']
for i in range(len(docs)):
  similarity.append(movie_nlp.similarity(docs[i]))
  
new_df['score'] = similarity

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)  # these two lines make it so that the columns are shown in full

new_df.sort_values(by=['score'], inplace=True, ascending=False)
print(new_df.head(20))


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