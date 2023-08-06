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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create session (link) from Python to the DB
    session = Session(engine)
    
    #Return precipitation data
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()
    
    # Convert list of tuples into a dictionary with date as the key and prcp as the value
    precipitation_dict = {}
    for date, prcp in prcp_results:
        precipitation_dict[date] = prcp

    session.close()
    
    return jsonify(precipitation_dict)
    
@app.route("/api/v1.0/stations")
def stations():
    
    # Create session (link) from Python to the DB
    session = Session(engine)
    
    #Return station data
    station_results = session.query(Station.name).all()

    # Convert list of tuples into a normal list of station names
    all_stations = [station[0] for station in station_results]

    session.close()
    
    return jsonify(all_stations)

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
    
    # Extract the temperature values from the list of tuples
    temperatures = [temp[0] for temp in yearly_temp_observations]
    
    session.close()
    
    return jsonify(temperatures)

@app.route("/api/v1.0/<start>")
def start_date(start):
    
    # Create a new session for this request
    session = Session(engine)
    
    # Query TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    # Close the session after the request is processed
    session.close()
    
    # Unpack the results into variables
    tmin, tavg, tmax = results[0]
    
    # Return the JSON response
    return jsonify({
        "TMIN": tmin,
        "TAVG": tavg,
        "TMAX": tmax
    })

@app.route("/api/v1.0/<start>/<end>")
def temperature_by_date_range(start, end):
    # Create a new session for this request
    session = Session(engine)
    
    # Query TMIN, TAVG, and TMAX for dates in the range from start date to end date (inclusive)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()
    
    # Close the session after the request is processed
    session.close()
    
    # Unpack the results into variables
    tmin, tavg, tmax = results[0]
    
    # Return the JSON response
    return jsonify({
        "TMIN": tmin,
        "TAVG": tavg,
        "TMAX": tmax
    })
    
if __name__ == '__main__':
    app.run(debug=True)