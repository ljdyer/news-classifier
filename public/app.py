from flask import Flask, render_template, request, jsonify
from get_clf_proba import get_clf_proba

app = Flask(__name__)


# ====================
@app.route('/')
def index():
    """Render index.html on app launch"""

    return render_template('index.html')


# # ====================
@app.route('/get_proba', methods=['POST'])
def get_proba():
    """Return dictionary of category probabilities as a JSON object in response
    to requests containing text input by user"""

    input_text = request.data
    class_proba = get_clf_proba([str(input_text)])
    return jsonify(class_proba)


# ====================
if __name__ == "__main__":

    app.run(debug=True)
