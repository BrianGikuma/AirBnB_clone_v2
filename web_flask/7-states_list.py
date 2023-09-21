#!/usr/bin/python3
"""
Starts a Flask web application
"""

from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def close_db(exception):
    from models import storage
    """Remove the session after each request"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list_route():
    """List all states sorted by name"""
    from models import storage
    from models.state import State
    states = storage.all(State).values()
    # states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
