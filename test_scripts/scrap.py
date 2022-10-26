from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder


def onehot_encode(df, column):
  # integer encode
  values=df[column]
  label_encoder = LabelEncoder()
  integer_encoded = label_encoder.fit_transform(values)
  # binary encode
  onehot_encoder = OneHotEncoder(sparse=False)
  integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
  onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
  countries = []
  for encoding in onehot_encoded:
    inverted = (label_encoder.inverse_transform([argmax(encoding)]))[0]
    if inverted not in countries:
      countries.append(inverted)
  new_df = pd.DataFrame(0, index=np.arange(len(values)), columns=countries)
  for i in range(len(onehot_encoded)):
    encoding = onehot_encoded[i]
    inverted = (label_encoder.inverse_transform([argmax(encoding)]))[0]
    new_df.iloc[i, new_df.columns.get_loc(inverted)] = 1
  return pd.concat([df, new_df], axis=1)
