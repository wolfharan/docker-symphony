#!/usr/bin/env python3
from flask import Flask, render_template, request, json, jsonify
from time import sleep
from multiprocessing import Value
import threading
import requests
import docker 


first_flag=0 
#flag that becomes 1 after the first request.

def autoscale():
	'''This function scales up and down depending upon the number of requests recieved in time t. 
	It scales up or down every t minutes. The variable base_scale_count defines a lower limit to the number of requests
	recieved. If the number of requests exceed base_scale_count, one container is started and so on.'''
	global curr_no_of_containers 
	#curr_no_of_containers is the number currently active containers
	with count.get_lock():
		base_scale_count=20
		cont_to_run=int(count.value/base_scale_count)+1
		#cont_to_run is the required number of containers to be active
		cont_to_start=cont_to_run-curr_no_of_containers
		#cont_to_start is the number of containers that need to be started, 
		#i.e the difference between the containers that need to be active and the number of containers that are currently active.
		print("Number of containers to start or delete :",cont_to_start)
		#if cont_to_start is negative we need to scale down and delete a -(cont_to_start) active containers.
		if(cont_to_start<0):
			client2=docker.from_env()
			container_list2=client2.containers.list()
			no_cont_delete=-(cont_to_start)
			cont_del_list=[]
			#cont_del_list will be populated with port numbers of containers that need to killed.
			temp=curr_no_of_containers
			while(no_cont_delete!=0):
				cont_del_list.append(int(8000+temp-1))
				temp=temp-1
				no_cont_delete=no_cont_delete-1
			for container in container_list2:
				try:
					p=container.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']
					#The above line gets the port of the container object and stores it in p.
					#Read more about Container object attributes here - https://docker-py.readthedocs.io/en/stable/containers.html#container-objects (Docker SDK for Python)
					if int(p) in cont_del_list:
						print("Container deleted in port :",int(p))
						container.kill()
						curr_no_of_containers=curr_no_of_containers-1
						
				except:
					pass
		#if cont_to_start is positive, we have to start more containers.	
		elif cont_to_start>0:
			for i in range(cont_to_start):
				client1=docker.from_env()
				print("Container started on port: ",8000+curr_no_of_containers)
				client1.containers.run(image='acts',detach=True,links={'db':'db'},ports={'80/tcp':8000+(curr_no_of_containers)})
				curr_no_of_containers=curr_no_of_containers+1
		count.value=0
		#count is number of requests recieved and it is reset here after every t minutes. t is defined below.		

def autoscale_thread():
	print("Autoscaling Start")
	t=120
	#Scaling is done every t minutes, t is specified in seconds. Hence we are scaling up or down every 2 minutes.
	while True:
		sleep(t)
		autoscale()
		
t2=threading.Thread(target=autoscale_thread)
				
app=Flask(__name__)

count=Value('i',0)
#count keeps tracks of number of requests recieved in the last t minutes.
curr_no_of_containers=1
#Initially , one container has to be running. Hence initially curr_no_of_container is 1.



@app.route('/',defaults={'path':''})
@app.route('/<path:path>')
def orc_engine(path):
	'''This is the function responsible of forwarding requests to containers 
	in a round robin way, the response also needs to returned to the client/user.'''
	global first_flag
	if request.method=='GET':
		if first_flag==0 and count.value==0:
			try:
				t2.start()
				#The above line starts the autoscaling thread. The autoscaling thread has to start only after the first request is recieved. 
				#(Why only after first request? :in compliance with university project specification)
				first_flag=1
			except:
				pass

		with count.get_lock():
			count.value=count.value+1
			port=count.value%curr_no_of_containers
			#The above line calculates the port number such that 8000+port gives port number of the container the request should go to. 
			#This is done in a round robin way using the modulus operation.
			mid_response=requests.get("http://localhost:"+str(8000+port)+str(request.full_path))
			try:
				data=mid_response.json()
				response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype="application/json")
			except:
				response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype="application/json")
			return response
	elif request.method=='POST':
		if first_flag==0 and count.value==0:
			try:
				t2.start()
				first_flag=1
			except:
				pass
		with count.get_lock():
			count.value=count.value+1
			port=count.value%curr_no_of_containers
			mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),json=request.get_json())
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
			return response
	elif request.method=='DELETE':
		if first_flag==0 and count.value==0:
			try:
				t2.start()
				first_flag=1
			except:
				pass
		with count.get_lock():
			count.value=count.value+1
			port=count.value%curr_no_of_containers
			mid_response=requests.delete("http://localhost:"+str(8000+port)+str(request.full_path))
			return json.dumps({}),mid_response.status_code
	elif request.method=='PUT':
		if first_flag==0 and count.value==0:
			try:
				t2.start()
				first_flag=1
			except:
				pass
		with count.get_lock():
			count.value=count.value+1
			port=count.value%curr_no_of_containers
			mid_response=requests.put(url="http://localhost:"+str(8000+port)+str(request.full_path),data=json.loads(request.get_json()))
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
			return response











def fault_tolerence():
	'''This function requests every container to get their health ever fault_t seconds, if any container is faulty, 
	that container is killed and a new container is started on the same port.
	For this to work, the application running in the docker container has to have a 
	health check api implemented in the path /api/v1/_health''' 
	client=docker.from_env()
	container_list=client.containers.list()	
	cont_count=0
	global curr_no_of_containers
	with count.get_lock():
		for a in container_list:
			if(cont_count<curr_no_of_containers):
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
	fault_t=1
	#fault_t is the interval at which health checks are performed.Here it is 1 second.
	print("Fault Tolerence Running")
	while True:
		fault_tolerence()
		sleep(fault_t)
		




t1=threading.Thread(target=fault_thread)
t1.start()
app.run(host='0.0.0.0',port='80',debug=True)
