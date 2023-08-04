#import modules / dependencies 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

@app.route("/")
def home():
#List all available api routes

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/home<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create session (link) from Python to the DB
    session = Session(engine)
    
    #Return precipitation data
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Convert list of tuples into a dictionary with date as the key and prcp as the value
    precipitation_dict = {}
    for date, prcp in prcp_results:
        precipitation_dict[date] = prcp

    return jsonify(precipitation_dict)

    session.close()
    
@app.route("/api/v1.0/stations")
def stations():
    
    # Create session (link) from Python to the DB
    session = Session(engine)
    
    #Return station data
    station_results = session.query(Station.name).all()
    session.close()

    # Convert list of tuples into a normal list of station names
    all_stations = [station[0] for station in station_results]

    return jsonify(all_stations)

    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create session (link) from Python to the DB
    session = Session(engine)
    
     # Define one_year_ago
    one_year_ago = dt.date(2016, 8, 23)

    # Define most_active_station_id (if you have it from the previous route)
    most_active_station_id = "USC00519281"
    
    #Return temp observations data
    yearly_temp_observations = session.query(Measurement.tobs).\
        filter(Measurement.date >= one_year_ago, Measurement.station == most_active_station_id).all()

    session.close()
    
    # Extract the temperature values from the list of tuples
    temperatures = [temp[0] for temp in yearly_temp_observations]
    
    return jsonify(temperatures)



if __name__ == '__main__':
    app.run(debug=True)