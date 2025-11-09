# --- Import necessary libraries ---
from flask import Flask, render_template, request, jsonify 
 # Flask for web app, render_template for HTML, request for handling user input, jsonify for returning JSON data
from itertools import chain, combinations                  
 # itertools provides functions to easily generate power sets

# --- Create the Flask app instance ---
app = Flask(__name__)  # This initializes your Flask application. '__name__' tells Flask where to look for files like templates and static assets.

# --- Route for the home page ---
@app.route('/')  # This defines the URL path for your homepage (e.g., http://localhost:5000/)
def home():
    # When a user visits the homepage, Flask renders the index.html file from the templates folder.
    return render_template('index.html')


# --- Route for Power Set Generation ---
@app.route('/powerset', methods=['POST'])  # This route handles POST requests sent to /powerset
def power_set():
    # Get JSON data sent from the frontend
    data = request.get_json()  # This reads the JSON body of the request from the browser
    elements_str = data.get('elements', '')  # Extract the 'elements' value (a string like "a,b,c") from the JSON data

    # Convert the string into a clean list of elements, removing any extra spaces or empty items
    elements = [x.strip() for x in elements_str.split(',') if x.strip()]

    # --- Define an inner function to generate the power set ---
    def powerset(iterable):
        # Convert the input iterable (like a list) into a list for easy handling
        s = list(iterable)
        # The 'combinations' function generates subsets of size r (for r from 0 to len(s))
        # 'chain.from_iterable' merges all those subsets into one long sequence
        return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

    # Call the powerset function and convert each subset (tuple) into a list
    result = [list(x) for x in powerset(elements)]

    # Return the result to the frontend as a JSON response
    return jsonify({'powerset': result})


# --- Route for Equality Check ---
@app.route('/check', methods=['POST'])  # This route handles POST requests sent to /check
def check_equality():
    # Get JSON data from the frontend (containing two sets entered by the user)
    data = request.get_json()

    # Extract and clean Set A
    # Split the input string by commas, remove spaces, and make it a Python set (to remove duplicates)
    setA = {x.strip() for x in data.get('setA', '').split(',') if x.strip()}

    # Extract and clean Set B in the same way
    setB = {x.strip() for x in data.get('setB', '').split(',') if x.strip()}

    # Compare the two sets directly using '=='
    # If both sets contain exactly the same elements (order doesn't matter), this will be True
    equal = setA == setB

    # Send back the comparison result to the frontend in JSON format
    return jsonify({'equal': equal})


# --- Run the Flask app ---
if __name__ == '__main__':
    # This block ensures the app only runs when this script is executed directly (not when imported)
    app.run(debug=True)  # Starts the Flask development server with debug mode ON (for auto-reload and error visibility)
