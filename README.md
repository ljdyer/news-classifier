# News classifier

This project came about following a University homework exercise to create a basic Naive Bayes text classifier. After completing the exercise, I started thinking about how the results could be presented in an easy-to-understand way to a layperson, and came up with the idea for the frontend of the site. The project helped me to get a feel for the steps involved in delivering ML models to users.

## How to use it

Go to https://ljdyer-news-classifier.herokuapp.com/.

Paste an article from BBC News or another news source, or simply type a few words into the text area and watch the category labels at the top of the page change in size to reflect the probability of the text belonging to each category.

The below screenshot was taken after pasting a randomly selected article from business section of the Guardian website. The model correctly predicts that the text is from an article about business, assigning 32.05% probability to the 'business' category.

<a href="https://ljdyer-news-classifier.herokuapp.com/"><img src="readme-img/news-classifier-screenshot.png"></img></a>

## How it works

The Python files in the private and public directories show the various stages involved in creating the model and the front-end app.

### Getting data

[private/bbc_trial_and_error.py](private/bbc_trial_and_error.py)

[private/bbc_from_category_pages.py](private/bbc_from_category_pages.py)

I decided to use the BBC News website as my data source and to scrape for articles from the five categories 'business', 'entertainment-arts', 'health', 'science-environment', 'technology'. I tried two different approaches to scraping the site, and getting article URLs from category landing pages emerged as the more efficient method. However I am still only able to get a few extra articles per day for the less common categories using this method, so I would like to spend more time improving it in the future. One avenue to explore is using the selenium library to 'click' through the 'Latest Updates' section on each category landing page.

### Training the model

[private/train_nb.py](private/train_nb.py)

The next step is to train the model with the data available. The main program in train_nb.py carries out pre-processing, data selection, model training and testing, and saves information about the model for access by the web app along with the pickled classifier and associated objects, so that all I have to do when I add more articles is run the program and commit.

### Running the model on new input

[public/get_clf_proba.py](public/get_clf_proba.py)

get_clf_proba.py provides the API for getting probabilities for each class (category) from the classifier model given new text input.

### Providing a UI

[public/app.py](public/app.py)

The UI is based around a Flask app that returns class probabilities in response to requests from the webpage to run the model on text input by the user in the text area.

## Credits

Basics of Naive Bayes for text classification: [here](https://medium.com/@eiki1212/natural-language-processing-naive-bayes-classification-in-python-e934365cf40c).

Ideas for how to print most informative features: [here](https://stackoverflow.com/questions/11116697/how-to-get-most-informative-features-for-scikit-learn-classifiers).