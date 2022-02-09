import pandas as pd
import numpy as np
from helper.file_helper import get_file_names, get_text_from_file, get_num_chars
import os
from os.path import join
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from random import shuffle
from math import ceil
import pickle

ARTICLES_PATH = "articles/"

file_names = get_file_names(ARTICLES_PATH)
file_paths = [join(ARTICLES_PATH, fn) for fn in file_names]

# Remove files containing less than 1000 characters
for file in file_paths:
    if get_num_chars(file) < 1000:
        os.remove(file)
        print(f"Removed {file}")

counts = {}

file_names = get_file_names(ARTICLES_PATH)

for fn in file_names:
    category = fn.rpartition('-')[0]
    if category in counts:
        counts[category] += 1
    else:
        counts[category] = 1

max_per_category = min(counts.values())

new_file_names = []
count_so_far = {category: 0 for category in counts.keys()}
for fn in file_names:
    category = fn.rpartition('-')[0]
    if count_so_far[category] < max_per_category:
        new_file_names.append(fn)
        count_so_far[category] += 1

print(len(new_file_names))
file_names = new_file_names

shuffle(file_names)
all_text = [get_text_from_file(join(ARTICLES_PATH, fn)) for fn in file_names]
all_labels = [fn.rpartition('-')[0] for fn in file_names]

train_cutoff = ceil(len(file_names) * 0.8)
print(train_cutoff)

X_train = all_text[:train_cutoff]
X_test = all_text[train_cutoff:]
y_train = all_labels[:train_cutoff]
y_test = all_labels[train_cutoff:]

# https://medium.com/@eiki1212/natural-language-processing-naive-bayes-classification-in-python-e934365cf40c

count_vector = CountVectorizer(stop_words='english')
tfidf_transformer = TfidfTransformer()

X_train_counts = count_vector.fit_transform(X_train)
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = MultinomialNB().fit(X_train_tfidf, y_train)
classes = clf.classes_

# https://stackoverflow.com/questions/11116697/how-to-get-most-informative-features-for-scikit-learn-classifiers

def print_most_informative_features(vectorizer, classifier, classlabel, n=10):
    labelid = list(classifier.classes_).index(classlabel)
    feature_names = vectorizer.get_feature_names_out()
    topn = sorted(zip(classifier.feature_log_prob_[labelid], feature_names))[-n:]
    topn = [feature[1] for feature in topn]
    print(f"{classlabel}: {', '.join(topn)}")

for class_ in classes:
    print_most_informative_features(count_vector, clf, class_)

X_test_counts = count_vector.transform(X_test)
X_new_tfidf = tfidf_transformer.transform(X_test_counts)

# Execute prediction(classification).
predicted = clf.predict(X_new_tfidf)
proba = clf.predict_proba(X_new_tfidf)

total = len(y_test)
incorrect = 0

for predicted, actual, prob in zip(predicted, y_test, proba):
    if predicted != actual:
        incorrect += 1

print(f"{((total-incorrect) / total)*100:.2f}%")

pickle.dump(count_vector, open('pickles/count_vector.pickle', 'wb'))
pickle.dump(tfidf_transformer, open('pickles/tfidf_transformer.pickle','wb'))
pickle.dump(clf, open('pickles/news_classifier.pickle', 'wb'))
