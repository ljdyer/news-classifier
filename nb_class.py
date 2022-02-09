import pandas as pd
import numpy as np
from file_helper import get_file_names, get_text_from_file
from os.path import join
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

CATEGORIES = [
    'health',
    'business'
]

ARTICLES_PATH = "articles/"

file_names = get_file_names(ARTICLES_PATH)

all_text = [get_text_from_file(join(ARTICLES_PATH, fn)) for fn in file_names]
all_labels = [fn.rpartition('-')[0] for fn in file_names]

X_train = all_text
y_train = all_labels

print(y_train)

# https://medium.com/@eiki1212/natural-language-processing-naive-bayes-classification-in-python-e934365cf40c


count_vector = CountVectorizer(stop_words='english')
tfidf_transformer = TfidfTransformer()

X_train_counts = count_vector.fit_transform(X_train)
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

X_train_counts


clf = MultinomialNB().fit(X_train_tfidf, y_train)
print(clf.classes_)


# https://stackoverflow.com/questions/11116697/how-to-get-most-informative-features-for-scikit-learn-classifiers

def most_informative_feature_for_class(vectorizer, classifier, classlabel, n=10):
    labelid = list(classifier.classes_).index(classlabel)
    feature_names = vectorizer.get_feature_names_out()
    topn = sorted(zip(classifier.feature_log_prob_[labelid], feature_names))[-n:]

    for coef, feat in topn:
        print (classlabel, feat, coef)

# print(len(clf.coef_))

most_informative_feature_for_class(count_vector, clf, 'health')
most_informative_feature_for_class(count_vector, clf, 'business')

X_test = [
  'The banks said they would pay the taxes.',
  'christmas covid deaths death daily number uk coronavirus'
]


X_test_counts = count_vector.transform(X_test)
X_new_tfidf = tfidf_transformer.transform(X_test_counts)

# Execute prediction(classification).
predicted = clf.predict(X_new_tfidf)
proba = clf.predict_proba(X_new_tfidf)

print(predicted)
print(proba)