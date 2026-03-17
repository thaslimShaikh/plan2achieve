import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# load dataset
data = pd.read_csv("model/dataset.csv")

X = data["goal"]
y = data["category"]

# vectorize
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)

# train model
model = MultinomialNB()
model.fit(X_vec, y)

# save
pickle.dump((model, vectorizer), open("model/model.pkl", "wb"))

print("Model trained using dataset.csv ✅")