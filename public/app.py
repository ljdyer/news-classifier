from flask import Flask, render_template, request, jsonify
import pickle


count_vectorizer = pickle.load(open('pickles/count_vectorizer.pickle', 'rb'))
tfidf_transformer = pickle.load(open('pickles/tfidf_transformer.pickle','rb'))
clf = pickle.load(open('pickles/clf.pickle', 'rb'))


def get_clf_proba(text: str):

    X_test_counts = count_vectorizer.transform(text)
    X_new_tfidf = tfidf_transformer.transform(X_test_counts)

    classes = clf.classes_
    proba = clf.predict_proba(X_new_tfidf)[0]
    class_proba = {class_: proba for class_, proba in zip(classes, proba)}

    return class_proba


app = Flask(__name__)

# ====================
@app.route('/')
def index():
    return render_template('index.html')


# # ====================
@app.route('/get_proba', methods=['POST'])
def get_proba():
    input_text = request.data
    class_proba = get_clf_proba([str(input_text)])
    return jsonify(class_proba)

      
# # ====================
# @app.route('/get_wer', methods=['POST'])
# def get_wer():
#     # Get reference sentence sent from frontend
#     try:
#         data = request.get_json(force=True)
#         reference = data['reference']
#     except:
#         return {'error': RETRIEVE_REF_ERROR}

#     # Get hypothesis sentence from Google Web Speech API
#     try:
#         hypothesis = get_best_hypothesis('upload/audio.wav')
#     except:
#         return {'error': SR_ERROR}
        
#     # Get WER information to display to user
#     try:
#         html = get_levenshtein_html(reference, hypothesis)
#     except:
#         return {'error': LEVENSHTEIN_ERROR}
#     return jsonify(html)
    

# ====================
if __name__ == "__main__":
    app.run(debug=True)