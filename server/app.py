# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

# Import the database instance and Earthquake model
from models import db, Earthquake

# Create the Flask application instance
app = Flask(__name__)

# Configure the SQLite database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Disable modification tracking to reduce overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure JSON responses are formatted across multiple lines
app.json.compact = False

# Set up Flask-Migrate for database version control
migrate = Migrate(app, db)

# Connect SQLAlchemy to the Flask app
db.init_app(app)

# Ensure tables exist before handling requests
# (assumes migrations have already been run)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Root route used to verify the API is running
    return make_response({'message': 'Flask SQLAlchemy Lab 1'}, 200)

@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    # Query the database for an earthquake matching the given ID
    quake = Earthquake.query.filter_by(id=id).first()

    # If no matching record is found, return a 404 response
    if quake is None:
        return make_response(
            {"message": f"Earthquake {id} not found."},
            404
        )

    # Return the earthquake data as JSON if found
    return make_response(
        {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        },
        200
    )

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    # Retrieve all earthquakes with magnitude greater than or equal
    # to the provided threshold
    quakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()

    # Return the count and a list of matching earthquakes
    return make_response(
        {
            "count": len(quakes),
            "quakes": [
                {
                    "id": quake.id,
                    "location": quake.location,
                    "magnitude": quake.magnitude,
                    "year": quake.year
                }
                for quake in quakes
            ]
        },
        200
    )

if __name__ == '__main__':
    # Run the development server on port 5555
    app.run(port=5555, debug=True)
