#!/usr/bin/python3
""" Route Python function app together with variable text"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_world():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """
    This function handles the route '/c/<text>'
    and returns a formatted string.
    Returns 404 error page if no value is given
    """
    if text:
        return 'C {}'.format(text.replace('_', ' '))


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text):
    """
    This function handles the route '/python/<text>' and returns a formatted string.
    Displays a default value 'cool' if value is given
    """
    if text:
        return 'Python {}'.format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
