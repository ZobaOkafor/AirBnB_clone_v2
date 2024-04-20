#!/usr/bin/python3
"""
Script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


def generate_states_html():
    """Generate HTML for states and their cities"""
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda state: state.name)

    states_html = []
    for state in states_sorted:
        state_info = {
            "id": state.id,
            "name": state.name,
            "cities": []
        }

        if storage._DBStorage__objects == "db":
            cities = sorted(state.cities, key=lambda city: city.name)
        else:
            cities = sorted(state.cities(), key=lambda city: city.name)

        for city in cities:
            city_info = {
                "id": city.id,
                "name": city.name
            }
            state_info["cities"].append(city_info)

        states_html.append(state_info)

    return states_html


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display a HTML page with the list of states and their cities"""
    states_html = generate_states_html()
    return render_template('cities_by_states.html', states=states_html)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
