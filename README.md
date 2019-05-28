# Docker Symphony

Docker symphony is a simple docker container orchestrator for containers running REST API's. It performs load balancing, autoscaling(Both scaling up and scaling down) and also implements fault tolerance

## Specifications

1. The requests from the user are load balanced amongst the active containers in a round robin way.
2. Checks the number of requests recieved in last t seconds (default is 120s, i.e 2 minutes), if the number of requests exceed base\_scale\_count (default is 20) a new container is started. If number of requests exceed base\_scale\_count\*2 , then 2 new containers are started and so on.
3. The orchestrator must make requests to the health check API implemented in the application code running in the containers, if the health is not OK ( i.e is if the API doesn't return 200) the container is killed and a new container is start. This must be done every 1 second.

## Where can I use this?

You can use this to orchestrate  **containers running REST API's** on a single server instance. (eg :- AWS EC2 instance)
Supported HTTP requests are as follows:
- GET
- POST
- PUT
- DELETE

## Prerequisites 
- Python3
```
sudo apt install python3 
```
- pip3
``` 
sudo apt install python3-pip
 ```
- Install requirements for the code using 
```
 pip3 install -r requirements 
```
or 
```
 python3 -m pip install -r requirements 
```
- Before you run the orchestrator, you need to do the following things to your REST API code running on docker containers: implement the health check API with your other API's at the route - /api/v1/_health ( or find /api/v1/_health i.e [line 171](https://github.com/wolfharan/docker-symphony/blob/2518bb795f291f837d0f58e15531d66884d78f0e/app.py#L171) in app.py and replace with the route of your choice ).The health check API could check if the filesystem is functioning properly if you are using the filesystem to store data or it could be checking if the database connection is still active. 
- Make sure you REST API application container is running before you run the orchestrator. 



## Running the orchestrator

You can run it like you run any other python code, The output will be show on the command line and you can stop the process using CTRL + C.
```
sudo python3 app.py
```
or you could use nohup or No Hangups to run the code, this will run the orchestrator in the background. This way, the code keeps running even after you exit the terminal and all the output will appended to nohup.out in the same directory as the code.
```
sudo nohup python3 app.py
```

## Languages and Libraries Used

* [Python3](https://docs.python.org/3/) 
* [Flask](http://flask.pocoo.org/) 
* [Requests](https://pypi.org/project/requests/) 
* [Python Docker SDK](https://docker-py.readthedocs.io/en/stable/) 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



