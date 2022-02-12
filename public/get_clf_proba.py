"""
get_clf_proba.py

Module for getting clf probabilities for each class (category) of the
classifier model for the text input.

Returns a dictionary where the keys are class names and the values are float
probabilities"""

import pickle

count_vectorizer = pickle.load(open('pickles/count_vectorizer.pickle', 'rb'))
tfidf_transformer = pickle.load(open('pickles/tfidf_transformer.pickle', 'rb'))
clf = pickle.load(open('pickles/clf.pickle', 'rb'))


# ====================
def get_clf_proba(text: str):

    X_test_counts = count_vectorizer.transform(text)
    X_new_tfidf = tfidf_transformer.transform(X_test_counts)

    classes = clf.classes_
    proba = clf.predict_proba(X_new_tfidf)[0]
    class_proba = {class_: proba for class_, proba in zip(classes, proba)}

    return class_proba
