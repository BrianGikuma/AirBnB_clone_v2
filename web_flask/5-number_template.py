#!/usr/bin/python3
"""Hbnb route module"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """index route"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """hbnb route"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """c is fun route"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    """python route"""
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """number route"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:num>', strict_slashes=False)
def numbe_template(num):
    """number_template route"""
    return render_template('5-number.html', number=num)


@app.route('/number_odd_or_even/<int:n>')
def number_odd_ir_even(n):
    """number odd or even route"""
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
