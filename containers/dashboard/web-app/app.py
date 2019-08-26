"""
Flask App to manage twitter sentiment summary dashboard
"""

import ast

from flask import Flask, jsonify, request
from flask import render_template

APP_NAME = Flask(__name__)
LABELS = []
VALUES = []


@APP_NAME.route("/")
def get_chart_page():
    """
    Function to handle route /
    :return: HTML template from the template folder with the given context.
    """
    global LABELS, VALUES
    LABELS = []
    VALUES = []
    return render_template('chart.html', values=VALUES, labels=LABELS)


@APP_NAME.route('/refreshData')
def refresh_graph_data():
    """
    Method to handle the route /refreshData
    :return: JSON response to the browser:
    """
    global LABELS, VALUES
    print "labels now: " + str(LABELS)
    print "data now: " + str(VALUES)
    return jsonify(sLabel=LABELS, sData=VALUES)


@APP_NAME.route('/updateData', methods=['POST'])
def update_data():
    """
    Method to handle the route /updateDate
    :return: HTTP response code
    """
    global LABELS, VALUES
    if not request.form or 'data' not in request.form:
        return "error", 400
    LABELS = ast.literal_eval(request.form['label'])
    VALUES = ast.literal_eval(request.form['data'])
    print "labels received: " + str(LABELS)
    print "data received: " + str(VALUES)
    return "success", 201


if __name__ == "__main__":
    APP_NAME.run(host='0.0.0.0', port=3527)
