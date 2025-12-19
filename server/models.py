# server/models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Use a naming convention–friendly MetaData object
# (required for Flask-Migrate compatibility in some databases)
metadata = MetaData()

# Initialize SQLAlchemy with the custom metadata
db = SQLAlchemy(metadata=metadata)


class Earthquake(db.Model):
    # Explicitly define the table name used in the database
    __tablename__ = "earthquakes"

    # Primary key column automatically assigned by the database
    id = db.Column(db.Integer, primary_key=True)
    magnitude = db.Column(db.Float)
    location = db.Column(db.String)
    year = db.Column(db.Integer)

    def __repr__(self):
        # Helpful string representation used in debugging and the Flask shell
        return f"<Earthquake {self.id}, {self.magnitude}, {self.location}, {self.year}>"
