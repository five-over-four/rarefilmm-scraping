from decouple import config
import os
import tmdbsimple as tmdb
import matplotlib.pyplot as plt

import pandas as pd
df = pd.read_csv('finalised_data2.csv')

tmdb.API_KEY = config('API_KEY')
found_movies = []
i=0
for movie_name in df['title']:
    search = tmdb.Search()
    search.movie(query=movie_name)
    if hasattr(search, "results"):
        print('Found ' + movie_name)
        found_movies.append(movie_name)
    i = i + 1
    print("Round " + str(i))


print('Found movies percentage: ' + str(len(found_movies)/df.shape[0]))







# print(df.head())
# print(df.columns)
# # print(df[df.duplicated(keep=False)])
# df['year'] = df['year'].astype(int)
# print(df['year'])
# df.sort_values(by=['year'], ascending=True)
# print(df['year'])
# # df['year'].plot()
# print(df.dtypes)
# # df.plot(kind='bar', x='year')
# # plt.show()
# # df['year'] = pd.to_datetime(df['year'], format = '%Y-%m-%d')
# import seaborn as sns
# # sns.set(style="darkgrid")
# ax = sns.countplot(x="year", data=df)
# plt.xticks(plt.xticks()[0], rotation=90)
# plt.show()