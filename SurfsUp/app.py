# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# Flask Setup
app = Flask(__name__)


# Flask Routes Home
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome to the Climate Analysis API!<br/>"

        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )


# Flask Routes the last 12 months Precipitation 
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()
   
    precipitation_score = []
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict["precipitation"] = prcp
        precipitation_dict["date"] = date
        precipitation_score.append(precipitation_dict)
    return jsonify(precipitation_score) 

# Flask Routes Stations
@app.route("/api/v1.0/stations")

def stations():
    stations_ds = session.query(Station.station).all()
    session.close()
    
    # Extract station names from the query result tuples
    stations = [station[0] for station in stations_ds]
    
    return jsonify(stations=stations)


# Flask Routes Tobs

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= last_year).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


#Flask Routes Temp Start/End
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def temp_stats(start=None, end=None):
    temp_stats = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end: 

        results = session.query(*temp_stats).\
        filter(Measurement.date <= start).all()
        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps)


    results = session.query(*temp_stats).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


if __name__ == "__main__":
    app.run(debug=True)











