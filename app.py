from flask import Flask, jsonify
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# connect to database
engine = create_engine('sqlite:///./Resources/hawaii.sqlite')

# Reflect database
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def homepage():
  """List all routes that are available"""
  return ( f"<h1>Available Routes:</h1>"
           f"<ul>"
           f"<li>/api/v1.0/precipitation</li>"
           f"<li>/api/v1.0/stations</li>"
           f"<li>/api/v1.0/tobs</li>"
           f"<li>/api/v1.0/<start> and /api/v1.0/<start>/<end></li>"
           f"</ul>"
  )


@app.route("/api/v1.0/precipitation")
def get_tobs():
  prcps = session.query(Measurement.date, Measurement.prcp).all()
  prcps_dict = [{date: prcp} for date, prcp in prcps]
  return jsonify(results_dict)


@app.route("/api/v1.0/stations")
def get_stations():
  stations = session.query(Station.station).all()
  return jsonify([station for station, in stations])


@app.route("/api/v1.0/tobs")
def get_tobs_of_most_active_station():
  most_active_station, _ = session.query(Measurement.station, func.count(Measurement.tobs))\
      .group_by(Measurement.station)\
      .order_by(desc(func.count(Measurement.tobs)))\
      .all()[0]

  temps = session.query(Measurement.date, Measurement.tobs)\
      .filter(Measurement.station == most_active_station)\
      .filter(Measurement.date > '2016-08-23')\
      .all()
  
  return jsonify([{date: tobs} for date, tobs in temps])


@app.route("/api/v1.0/<start>")
def get_greg_data1(start):
    TMIN, TAVG, TMAX = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                        .filter(Measurement.date >= start)\
                        .all()[0]

    return  jsonify({"TMIN": TMIN,
                   "TAVG": TAVG,
                   "TMAX": TMAX
                   })


@app.route("/api/v1.0/<start>/<end>")
def get_greg_data2(start, end):
    TMIN, TAVG, TMAX = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                        .filter(Measurement.date >= start)\
                        .filter(Measurement.date <= end)\
                        .all()[0]

    return  jsonify({"TMIN": TMIN,
                     "TAVG": TAVG,
                     "TMAX": TMAX
                   })


if __name__ == '__main__':
    app.run(debug=True)


