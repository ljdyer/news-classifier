from helper.file_helper import (
    get_file_paths, get_text_from_file, get_num_chars
)
import json
import math
import os
from os.path import join
import pickle
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

ARTICLES_PATH = "articles/"
TRAIN_TEST_PERCENT = 0.8
PRIVATE_PICKLE_PATH = "pickles/"
PUBLIC_PICKLE_PATH = "../public/pickles"
JSON_PATH = "../public/static/json/model_info.json"


# ====================
def pickle_to_path(count_vectorizer, tfidf_transformer, clf, path):
    """Pickle classifier and related objects to a path"""

    count_vectorizer_path = join(path, 'count_vectorizer.pickle')
    pickle.dump(count_vectorizer, open(count_vectorizer_path, 'wb'))
    tfidf_transformer_path = join(path, 'tfidf_transformer.pickle')
    pickle.dump(tfidf_transformer, open(tfidf_transformer_path, 'wb'))
    clf_path = join(path, 'clf.pickle')
    pickle.dump(clf, open(clf_path, 'wb'))


# ====================
def save_model_info(num_train_files, num_test_files, accuracy_percent):
    """Save information about model to JSON file"""

    model_info = {
        'num_train_files': num_train_files,
        'num_test_files': num_test_files,
        'accuracy_percent': accuracy_percent
    }
    with open(JSON_PATH, 'w') as file:
        json.dump(model_info, file)


# ====================
def remove_small_files(folder_path, min_chars=1000):
    """Remove all files from a folder that contain less than a minimum
    number of characters

    Return the number of files removed as an integer"""

    file_paths = get_file_paths(folder_path)
    removed_count = 0
    for file in file_paths:
        if get_num_chars(file) < 1000:
            os.remove(file)
            removed_count += 1
    return removed_count


# ====================
def sort_into_dict(tuple_list: list) -> dict:
    """Sort a list of tuples into a dictionary of lists

    Keys are first elements of tuple, and values are lists of second elements
    of tuples with that first value"""

    dict_ = {}
    for key, value in tuple_list:
        if key in dict_:
            dict_[key].append(value)
        else:
            dict_[key] = []
    return dict_


# ====================
def category_from_path(file_path: str) -> str:
    """Get the category of an article from the file path"""

    return (file_path.rpartition('/')[2]).rpartition('-')[0]


# ====================
def flatten(list_of_lists: list) -> list:
    """Flatten a list of lists into a list of elements"""

    return [item for sublist in list_of_lists for item in sublist]


# ====================
def print_most_informative_features(vectorizer, clf, n=10):
    """Print the most informative features for each class in a classifier
    model"""

    feature_names = vectorizer.get_feature_names_out()
    for index, class_ in enumerate(clf.classes_):
        # Sort in ascending order of log probability and take last n elements
        top_n = sorted(zip(clf.feature_log_prob_[index], feature_names))[-n:]
        # Reverse to get highest to lowest
        top_n = reversed(top_n)
        top_n = [feature[1] for feature in top_n]
        print(f"{class_}: {', '.join(top_n)}")


# ====================
def main():

    # Remove files less than 1000 characters
    num_removed = remove_small_files(ARTICLES_PATH, 1000)
    print(f"Removed {num_removed} files containing less than 1000 characters")

    # Sort files into categories and get number of articles in each
    file_paths = get_file_paths(ARTICLES_PATH)
    categories_and_files = [(category_from_path(fp), fp) for fp in file_paths]
    files_by_category = sort_into_dict(categories_and_files)
    num_files_by_category = {
        category: len(files) for category, files in files_by_category.items()
    }
    print(f'Numbers of files in each category: {num_files_by_category}')

    # Take lowest number of articles in a category as the number of articles from each
    # category to use for training and testing.
    num_files_per_category = int(min(num_files_by_category.values()))
    print(f'Using {num_files_per_category} articles per category for training and testing.')

    # Prepare train and test files
    files_by_category = [
        random.sample(files, num_files_per_category)
        for files in files_by_category.values()
    ]
    train_test_split = math.ceil(num_files_per_category * TRAIN_TEST_PERCENT)
    train_files = flatten([files[:train_test_split] for files in files_by_category])
    num_train_files = len(train_files)
    print(f"Using a total of {num_train_files} articles for training.")
    test_files = flatten([files[train_test_split:] for files in files_by_category])
    num_test_files = len(test_files)
    print(f"Using a total of {num_test_files} articles for testing.")
    X_train = [get_text_from_file(fp) for fp in train_files]
    y_train = [category_from_path(fp) for fp in train_files]
    X_test = [get_text_from_file(fp) for fp in test_files]
    y_test = [category_from_path(fp) for fp in test_files]

    # Train Naive Bayes classifier
    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer()
    X_train_counts = count_vectorizer.fit_transform(X_train)
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = MultinomialNB().fit(X_train_tfidf, y_train)
    print()
    print("Model trained.")

    # Print 10 most informative features for each class
    print()
    print("Most informative features:")
    print_most_informative_features(count_vectorizer, clf, 10)

    # Test model
    X_test_counts = count_vectorizer.transform(X_test)
    X_new_tfidf = tfidf_transformer.transform(X_test_counts)
    predictions = clf.predict(X_new_tfidf)
    total_articles = len(y_test)
    correct = 0
    for predicted, actual in zip(predictions, y_test):
        if predicted == actual:
            correct += 1
    accuracy_percent = f"{(correct / total_articles) * 100:.2f}%"
    print()
    print(f"Model has {accuracy_percent} accuracy on the test set.")

    # Pickle model and save model info to JSON file
    pickle_to_path(
        count_vectorizer, tfidf_transformer, clf, PRIVATE_PICKLE_PATH
    )
    pickle_to_path(
        count_vectorizer, tfidf_transformer, clf, PUBLIC_PICKLE_PATH
    )
    save_model_info(
        num_train_files, num_test_files, accuracy_percent
    )


# ====================
if __name__ == "__main__":

    main()
