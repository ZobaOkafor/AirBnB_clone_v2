#!/usr/bin/python3
"""
Script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)


def load_states():
    """Load and sort all State objects"""
    states = storage.all(State).values()
    return sorted(states, key=lambda state: state.name)


def load_cities():
    """Load and sort all City objects"""
    cities = storage.all(City).values()
    return sorted(cities, key=lambda city: city.name)


def load_amenities():
    """Load and sort all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return sorted(amenities, key=lambda amenity: amenity.name)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Display the HTML page with filters"""
    states = load_states()
    cities = load_cities()
    amenities = load_amenities()
    return render_template('10-hbnb_filters.html',
                           states=states, cities=cities, amenities=amenities)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
