# Docker Symphony :whale: :musical_note:

Docker symphony is a simple orchestrator for docker containers running REST API's. It performs load balancing amongst containers, autoscaling(Both scaling up and scaling down) and also implements fault tolerance.

## Specifications

1. The requests from the user are load balanced amongst the active containers in a round robin way.
2. Checks the number of requests recieved in last t seconds (default = 120s, i.e 2 minutes), if the number of requests exceed base\_scale\_count (default is 20) a new container is started on port 8001. If number of requests exceed base\_scale\_count\*2 , then 2 new containers of the same image are started on port 8001 and 8002 and so on.If the number of requests in the next 2 minutes is less then 20, the orchestrator must delete all the excess containers and reduce the number of running containers to 1.
3. The orchestrator must make requests to a health check API implemented within the containers, if the health is not OK ( i.e is if the API doesn't return 200) the container is killed and a new container is started on the same port. This must be done every fault_t seconds (default = 1s).

## Where can I use this?

You can use this to orchestrate  **docker containers running REST API's** on a single server instance. (eg :- AWS EC2 instance)
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
- Change the name of the image in app.py. Find (CTRL +F) the line ``` containers.run ``` and change ``` image= acts ``` to ``` image= your_image_name ``` . You have to make this change in two places ( One in autoscale() and the other in fault_tolerence() )
- Before you run the orchestrator, you need to do the following things to your REST API code that you deploy in docker containers: implement a health check API at the route - /api/v1/_health ( or find /api/v1/_health i.e [line 171](https://github.com/wolfharan/docker-symphony/blob/2518bb795f291f837d0f58e15531d66884d78f0e/app.py#L171) in app.py and replace it with the route of your choice ).The health check API could check if the filesystem is functioning properly if you are using the filesystem to store data or it could be checking if the database connection is still active. 

- Make sure atleast one application container is running before you run the orchestrator. 



## Running the orchestrator

You can run it like you run any other python code, The output will be show on the command line and you can stop the process using CTRL + C.
```
sudo python3 app.py
```
or you could use nohup or No Hangups to run the code, this will run the orchestrator in the background. This way, the code keeps running even after you exit the terminal and all the output will appended to nohup.out in the same directory as the code.
```
sudo nohup python3 app.py
```

## Languages and libraries used

* [Python3](https://docs.python.org/3/) :snake:
* [Flask](http://flask.pocoo.org/) 
![Flask](https://raw.githubusercontent.com/pallets/flask/master/artwork/logo-lineart.svg?sanitize=true){width=100px}

* [Requests](https://pypi.org/project/requests/) :turtle:
* [Python Docker SDK](https://docker-py.readthedocs.io/en/stable/) :whale:

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

Copyright (c) 2019 Hari Charan U


