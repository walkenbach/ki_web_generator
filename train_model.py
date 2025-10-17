from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Trainingsdaten
texts = ["Hallo", "Wie geht es dir?", "Ich liebe Python", "Das Wetter ist schön"]
labels = ["Begrüßung", "Frage", "Aussage", "Kommentar"]

# Modell erstellen
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
model = MultinomialNB()
model.fit(X, labels)

# Modell speichern
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Modell gespeichert!")
