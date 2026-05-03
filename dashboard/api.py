from flask import Blueprint, jsonify, request
import pandas as pd
from db import pandaSQL
import json
from dfHelper import tableToSeries,tableToHeatMap,aggPerDevice,correctionMatrix

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/health")
def health():

   sensors=f"select * from sensor_readings"
   res = pandaSQL(sensors)

   return res.to_dict(orient='records')

@api.route("/devices/",methods=["POST"])
def devices():
   sensors=f"SELECT * FROM DEVICES"
   res = pandaSQL(sensors)

   return res.to_dict(orient='records')

@api.route("/devices/latest")
def lastestStats():
   sensors=f"SELECT DISTINCT ON (device_name) * FROM sensor_readings ORDER BY device_name, ts DESC;"
   df = pandaSQL(sensors)
   df['ts'] = pd.to_datetime(df['ts'])
   df = df.sort_values(by='ts',ascending=False)
   lastest_record = df.to_dict(orient='records')
   overview = aggPerDevice(df)
   response ={
      'overview':overview,
   'records':lastest_record
   }

   return response


@api.route("/device/overview",methods=['POST'])
def deviceOverview():
   body_json = request.get_json()
   name = body_json.get('device_name')

   sensors=f"select * from sensor_readings where device_name='{name}' ORDER BY ts DESC"
   df = pandaSQL(sensors)
   overview = aggPerDevice(df)
   return  overview
@api.route("/device/",methods=['POST'])
def device():
   body_json = request.get_json()
   name = body_json.get('device_name')

   sensors=f"select * from sensor_readings where device_name='{name}' ORDER BY ts DESC"
   df = pandaSQL(sensors)
   series =tableToSeries(df)
   temp = {"raw": df.to_dict(orient='records'),"series":series}
   return temp 

@api.route("/device/analyzer",methods=['POST'])
def deviceRecordHeatMap():
   body_json = request.get_json()
   name = body_json.get('device_name')

   sensors=f"select * from sensor_readings where device_name='{name}' ORDER BY ts DESC"
   df = pandaSQL(sensors)
   heatmap =tableToHeatMap(df,"soil_moisture")
   corr_heatmap_data = correctionMatrix(df)
   response={"heatmap":heatmap,"correlation": corr_heatmap_data}
   return response
