#!/usr/bin/env python3
from flask import Flask, render_template, request, json, jsonify
from time import sleep
from multiprocessing import Value
import threading
import requests
import docker 

first_flag=0

def autoscale():
	global no_of_containers
	with count.get_lock():
		cont_to_run=int(count.value/20)+1
		
		cont_to_start=cont_to_run-no_of_containers
		print("container count **",cont_to_start)
		if(cont_to_start<0):
			client2=docker.from_env()
			container_list2=client2.containers.list()
			cont_flag=-(cont_to_start)
			for a1 in container_list2:
				try:
					print("container:",a1)
					p=a1.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']
					print("port :" ,p)
					print("Number of containers",no_of_containers)
					print("port number to delete", 8000+no_of_containers-1)
					print("truth of p",int(p)==int( 8000 + no_of_containers-1))
					if cont_flag!=0 and int(p)==int( 8000 + (no_of_containers-1)):
						print("container del")
						a1.kill()
						no_of_containers=no_of_containers-1
						cont_flag=cont_flag-1
				except:
					pass
			
		elif cont_to_start>0:
			for i in range(cont_to_start):
				client1=docker.from_env()
				print("container start ")
				client1.containers.run(image='acts',detach=True,links={'db':'db'},ports={'80/tcp':8000+(no_of_containers)})
				print(8000+no_of_containers)
				no_of_containers=no_of_containers+1
		count.value=0		

def autoscale_thread():
	print("autoscale_start")
	while True:
		sleep(120)
		autoscale()
		
t2=threading.Thread(target=autoscale_thread)


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
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass
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
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),json=request.get_json())
		response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response


@app.route('/api/v1/categories/<categoryName>', methods = ['DELETE'])
def delete_categories(categoryName):
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.delete("http://localhost:"+str(8000+port)+str(request.full_path))
		return json.dumps({}),mid_response.status_code

@app.route('/api/v1/categories/<categoryName>/acts', methods = ['GET'])
def get_catefories_acts(categoryName):
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass
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
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass

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
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass
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
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),json=request.get_json())
		response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response


@app.route('/api/v1/acts/<actid>', methods = ['DELETE'])
def delete_acts(actid):
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass

	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.delete("http://localhost:"+str(8000+port)+str(request.full_path))
		return json.dumps({}),mid_response.status_code

@app.route('/api/v1/acts', methods = ['POST'])
def post_acts():
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass

	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),json=request.get_json())
		response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response

@app.route('/api/v1/acts/count',methods=['GET'])
def get_acts_count():
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass

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
	
	client=docker.from_env()
	container_list=client.containers.list()	
	cont_count=0
	global no_of_containers
	with count.get_lock():
		for a in container_list:
			if(cont_count<no_of_containers):
				#print("in loop")
				try:
					p=a.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']
					r=requests.get('http://localhost:'+str(p)+"/api/v1/_health")
					if r.status_code!=200:
						print("killing ",p)
						a.kill()
						client.containers.run(image='acts',detach=True,links={'db':'db'},ports={'80/tcp':p})
					cont_count=cont_count+1
				except:
					pass

def fault_thread():
	print("startwd")
	while True:
		fault_tolerence()
		sleep(1)
		




t1=threading.Thread(target=fault_thread)

t1.start()
app.run(host='0.0.0.0',port='80',debug=True)
