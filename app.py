"""
This module defines a Flask web application that provides an API to search curriculum data.
It renders a home page and a readme page, and it exposes an API endpoint to perform searches.
The search functionality is delegated to the Search class defined in the search.py module.
"""

from flask import Flask, jsonify, render_template, request

from search import Search  # Import the Search class

app = Flask(__name__)
search_engine = Search()  # Initialize the search engine


@app.route("/")
def home():
    """Renders the home page."""
    return render_template("index.html")


@app.route("/readme")
def readme():
    """Renders the readme page."""
    return render_template("README.html")


@app.route("/api/search", methods=["GET"])
def api_search():
    """Handles search requests and returns results as JSON."""
    query = request.args.get("query", "")
    results, status_code = search_engine.search(query)

    return jsonify(results) if status_code == 200 else jsonify(results), status_code


if __name__ == "__main__":
    app.run(debug=True)
