import pickle
from helper.file_helper import get_text_from_file

count_vector = pickle.load(open('pickles/count_vector.pickle', 'rb'))
tfidf_transformer = pickle.load(open('pickles/tfidf_transformer.pickle','rb'))
clf = pickle.load(open('pickles/news_classifier.pickle', 'rb'))

X_test = [get_text_from_file("articles/business-60001147.txt")]

X_test_counts = count_vector.transform(X_test)
X_new_tfidf = tfidf_transformer.transform(X_test_counts)

# Execute prediction(classification).
predicted = clf.predict(X_new_tfidf)
proba = clf.predict_proba(X_new_tfidf)

print(proba)
