def initialize_docs():
  print('preprocess df')
  print(df)
  df.dropna(axis=0, inplace=True, subset=df.columns.difference(['country']))
  df.reset_index(drop=True, inplace=True)
  global docs
  docs_prc = [nlp(' '.join([str(t) for t in nlp(str(description)) if t.pos_ in ['NOUN', 'PROPN']])) for description in df['description']]
  docs_arr_bytes = np.array(docs_prc).tobytes()
  f = open("rf_docs.bin", "wb")
  f.write(docs_arr_bytes)
  f.close()
  
  print('preprocess finished')
  
initialize_docs()