#!/usr/bin/python3
""" Route Python function app together with variable text"""
from flask import Flask, render_template

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
    This function handles the route '/python/<text>'
    and returns a formatted string.
    Displays a default value 'cool' if value is given
    """
    if text:
        return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """
    This function handles the route '/number/<n>'
    and displays n only if n is a number.
    Returns 404 error page if no value is not a number.
    """
    if n:
        return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template_route(n=None):
    """
    This function handles the route '/number/<n>'
    and displays a template only if n is a number.
    Returns 404 error page if value is not a number.
    """
    if n:
        return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
