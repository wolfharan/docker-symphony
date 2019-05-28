# Docker Symphony

Docker symphony is a simple docker container orchestrator for containers running REST API's. It performs load balancing, autoscaling(Both scaling up and scaling down) and also implements fault tolerance

## Specifications

1. The requests from the user are load balanced amongst the active containers in a round robin way.
2. Checks the number of requests recieved in last t seconds (default is 120s, i.e 2 minutes), if the number of requests exceed base\_scale\_count (default is 20) a new container is started. If number of requests exceed base\_scale\_count\*2 , then 2 new containers are started and so on.
3. The orchestrator must make requests to the health check API implemented in the application code running in the containers, if the health is not OK ( i.e is if the API doesn't return 200) the container is killed and a new container is start. This must be done every 1 second.

## Where can you use this?

You can use this to orchestrate the **containers running REST API's** on a single server instance. (eg :- AWS EC2 instance)
Supported HTTP requests are as follows:
- GET
- POST
- PUT
- DELETE

```
Give examples
```

## Prerequisites and things to do :-
- Python3
'''sudo apt install python3 '''
- pip3
''' sudo apt install python3-pip '''
- Install requirements for the code using 
''' pip3 install -r requirements '''
or 
''' python3 -m pip install -r requirements '''
- Before you run the orchestrator, you need to do the following things to your REST API code running on docker containers -
  - implement the health check API with your other API's at the route - /api/v1/_health ( or find /api/v1/_health in app.py and replace with the route of your choice ).The health check API could check if the filesystem is functioning properly if you are using the filesystem to store data or it could be checking if the database connection is still active. 



Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc


