import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './tmdb_data_3.csv')
import pandas as pd

df = pd.read_csv(filename)