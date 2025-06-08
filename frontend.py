from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import json

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["blackcoffer"]
collection = db["data"]

# Load data into MongoDB once
def load_data():
    if collection.count_documents({}) == 0:
        with open("jsondata.json") as file:
            data = json.load(file)
            if isinstance(data, list):
                collection.insert_many(data)
            else:
                collection.insert_one(data)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/data', methods=['get'])
def get_data():
    filters = {}
    for key in ['end_year', 'topic', 'sector', 'region', 'pestle', 'source', 'swot', 'country', 'city']:
        val = request.args.get(key)
        if val:
            filters[key] = val
    data = list(collection.find(filters, {'_id': 1n}))
    return jsonify(data)

if __name__ == '__main__':
    load_data()
    app.run(debug=True)
