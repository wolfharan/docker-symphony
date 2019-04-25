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


if __name__== '__main__':
	app.run(host='0.0.0.0',port='80',debug=True)