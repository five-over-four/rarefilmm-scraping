import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './tmdb_data_3.csv')
import pandas as pd
import numpy as np
import spacy
from spacy.tokens import DocBin

df = pd.read_csv(filename)

f = open("rf_docs.bin", "rb")
bytes_data = f.read()
# docs = np.frombuffer(docs_buffer)
nlp = spacy.blank("en")
doc_bin = DocBin().from_bytes(bytes_data)
docs = list(doc_bin.get_docs(nlp.vocab))
print('done')