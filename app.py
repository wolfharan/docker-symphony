from flask import Flask, render_template, request, json, jsonify
from time import sleep
from multiprocessing import Value
import threading
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
def get_health():
	with count.get_lock():
		#count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get('http://localhost:'+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype='application/json')
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response
@app.route("/api/v1/_crash",methods=['POST'])
def post_crash():
	with count.get_lock():
		#count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),json=request.get_json())
		response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response

@app.route("/api/v1/_count", methods=['GET'])
def get_count():
	with count.get_lock():
		#count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get('http://localhost:'+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype='application/json')
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response
@app.route("/api/v1/_count", methods=['DELETE'])
def delete_count():
	with count.get_lock():
		#count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.delete("http://localhost:"+str(8000+port)+str(request.full_path))
		return json.dumps({}),mid_response.status_code



@app.route('/api/v1/categories', methods = ['GET'])
def get_categories():
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get('http://localhost:'+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype='application/json')
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response

@app.route('/api/v1/categories', methods = ['POST'])
def post_categories():
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),json=request.get_json())
		response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response


@app.route('/api/v1/categories/<categoryName>', methods = ['DELETE'])
def delete_categories(categoryName):
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.delete("http://localhost:"+str(8000+port)+str(request.full_path))
		return json.dumps({}),mid_response.status_code

@app.route('/api/v1/categories/<categoryName>/acts', methods = ['GET'])
def get_catefories_acts(categoryName):
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get("http://localhost:"+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype="application/json")
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype="application/json")
		return response
@app.route('/api/v1/categories/<categoryName>/acts/size', methods = ['GET'])
def get_catefories_acts_count(categoryName):
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get("http://localhost:"+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype="application/json")
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype="application/json")
		return response


@app.route('/api/v1/categories/<categoryName>/acts?start=<startRange>&end=<endRange>', methods = ['GET'])
def get_catefories_acts_count_100(categoryName,startRange,endRange):
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get("http://localhost:"+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype="application/json")
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype="application/json")
		return response

@app.route('/api/v1/acts/upvote', methods = ['POST'])
def upvote_act():
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),json=request.get_json())
		response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response


@app.route('/api/v1/acts/<actid>', methods = ['DELETE'])
def delete_acts(actid):
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.delete("http://localhost:"+str(8000+port)+str(request.full_path))
		return json.dumps({}),mid_response.status_code

@app.route('/api/v1/acts', methods = ['POST'])
def post_acts():
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),json=request.get_json())
		response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response

@app.route('/api/v1/acts/count',methods=['GET'])
def get_acts_count():
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get('http://localhost:'+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype='application/json')
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response






def fault_tolerence():
	print("thread start")
	client=docker.from_env()
	container_list=client.containers.list()	
	cont_count=0
	global no_of_containers
	for a in container_list:
		if(cont_count<no_of_containers):
			p=a.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']
			r=requests.get('http://localhost:'+str(p)+"/api/v1/_health")
			if r.status_code!=200:
				a.kill()
				client.containers.run(image='acts',detach=True,links={'db':'db'},ports={'80/tcp':p})
			cont_count=cont_count+1

def fault_thread():
	print("startwd")
	while True:
		sleep(1)
		fault_tolerence()






if __name__=='__main__':
	
	t1=threading.Thread(target=fault_thread)
	t1.start()
	app.run(host='0.0.0.0',port='80',debug=True)
