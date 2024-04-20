#!/usr/bin/python3
"""
This script starts a Flask web application listening on 0.0.0.0, port 5000.
Routes:
    /: display “Hello HBNB!”
    /hbnb: display “HBNB”
    /c/<text>: display “C ”, followed by the value of the text
    variable (replace underscore _ symbols with a space).
    /python/(<text>): display “Python ”, followed by the value of the
    text variable (replace underscore _ symbols with a space).
    The default value of text is “is cool”
    /number/<n>: display “n is a number” only if n is an integer
    /number_template/<n>: display a HTML page only if n is an integer:
    H1 tag: “Number: n” inside the tag BODY
    /number_odd_or_even/<n>: display a HTML page only if n is an integer:
    H1 tag: “Number: n is even|odd” inside the tag BODY
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!'"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """Display 'HBNB'"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def display_c_text(text):
    """Display 'C' followed by the value of the text variable"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python_text(text):
    """Display 'Python' followed by the value of the text variable"""
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def display_number(n):
    """Display “n is a number” only if n is an integer"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def display_number_template(n):
    """Display a HTML page only if n is an integer"""
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def display_number_odd_or_even(n):
    """Display a HTML page only if n is an integer"""
    return render_template('6-number_odd_or_even.html', number=n, odd_even='odd' if n % 2 != 0 else 'even')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
