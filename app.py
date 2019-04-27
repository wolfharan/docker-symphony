from flask import Flask, render_template, request, json, jsonify
from multiprocessing import Value
import mysql.connector
import requests
import docker 

class ORCengine:
	def __init__(replicas,request_limit,autoscale_timer):
		self.replicas=replicas
		self.request_limit=request_limit
		self.autoscale_timer=autoscale_timer
				
app=Flask(__name__)

count=Value('i',0)
no_of_containers=1

@app.route("/api/v1/_health", methods=['GET'])
@app.route("/api/v1/_crash",methods=['GET'])
@app.route("/api/v1/_count", methods=['GET'])
@app.route("/api/v1/_count", methods=['DELETE'])



@app.route('/api/v1/categories', methods = ['GET'])
def get_categories():
	global count
	with count.get_lock():
		count=count+1
		port=count%no_of_containers
		mid_response=requests.get(url="http://localhost:"+str(8000+port)+str(request.full_path))
		response=app.response_class(response=mid_response.json(),status=mid_response.status_code,mimetype='application/json')
		return response

@app.route('/api/v1/categories', methods = ['POST'])
def post_categories():
	global count
	with count.get_lock():
		count=count+1
		port=count%no_of_containers
		mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),data=request.get_json())
		response=app.response_class(response=mid_response.json(),status=mid_response.status_code,mimetype='application/json')
		return response


@app.route('/api/v1/categories/<categoryName>', methods = ['DELETE'])
@app.route('/api/v1/categories/<categoryName>/acts', methods = ['GET'])
@app.route('/api/v1/categories/<categoryName>/acts/size', methods = ['GET'])
@app.route('/api/v1/categories/<categoryName>/acts?start=<startRange>&end=<endRange>', methods = ['GET'])
@app.route('/api/v1/acts/upvote', methods = ['POST'])
@app.route('/api/v1/acts/<actid>', methods = ['DELETE'])
@app.route('/api/v1/acts', methods = ['POST'])
@app.route('/api/v1/acts/count',methods=['GET'])











app.run(host='0.0.0.0',port='80',debug=True)
