from flask import Flask, request, jsonify
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)

nltk.download('popular', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

with open('Chatbot.txt', 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["Hi There, Good Evening", "Hey, How are You", "*nods*", "Hi there", "Hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        robo_response = "I'm Sorry, I'm Still In Development Mode"
    else:
        robo_response = sent_tokens[idx]
    sent_tokens.remove(user_response)
    return robo_response

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message.lower() == 'bye':
        return jsonify(reply="Bye! take care..")
    if user_message.lower() in ['thanks', 'thank you']:
        return jsonify(reply="You are welcome..")
    if greeting(user_message) is not None:
        return jsonify(reply=greeting(user_message))
    return jsonify(reply=response(user_message))

if __name__ == "__main__":
    app.run(debug=True)
