import numpy as np
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()

    session.close()
    return jsonify(prcp_scores)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    station_list = session.query(Station.station).all()

    session.close()
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    busiest = 'USC00519281'
    year_data = session.query(Measurement.date, Measurement.tobs). \
                filter(Measurement.date >= start_date).filter(Measurement.station == busiest).all()

    session.close()
    return jsonify(year_data)


@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    

    end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    start_date = start  
    busiest = 'USC00519281'
    summary_stats = session.query(Measurement.date, func.min(Measurement.tobs),\
                            func.max(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                                filter(Measurement.station == busiest).\
                                filter(Measurement.date >= start_date).\
                                group_by(Measurement.date).all()

    final_results = []
    for record_date, minimum, maximum, average in summary_stats:
        each_date = {}
        each_date["Date"] = record_date
        each_date["Minimum"] = minimum
        each_date["Maximum"] = maximum
        each_date["Average"] = average
        final_results.append(each_date)

    session.close()
    return jsonify([final_results])


@app.route("/api/v1.0/<start>/<end>")
def date_range(start,end):
    session = Session(engine)
    

    end_date = end
    start_date = start  
    busiest = 'USC00519281'
    summary_stats = session.query(Measurement.date, func.min(Measurement.tobs),\
                            func.max(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                                filter(Measurement.station == busiest).\
                                filter(Measurement.date >= start_date).\
                                filter(Measurement.date <= end_date).\
                                group_by(Measurement.date).all()

    final_results = []
    for record_date, minimum, maximum, average in summary_stats:
        each_date = {}
        each_date["Date"] = record_date
        each_date["Minimum"] = minimum
        each_date["Maximum"] = maximum
        each_date["Average"] = average
        final_results.append(each_date)

    session.close()
    return jsonify([final_results])

if __name__ == '__main__':
    app.run(debug=True)
