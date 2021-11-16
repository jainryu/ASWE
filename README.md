# Talking Potatoes

A unified lead service built using Flask. The service is hosted at https://tp-leads-app.herokuapp.com .

The API documentation and endpoints are available at this [link](https://app.swaggerhub.com/apis/tojo/lead-aggregator_and_analytics_service/1.0.0)

## Third Party APIs

1. [Thumbtack](https://pro-api.thumbtack.com/docs/#introduction)
2. [Facebook](https://developers.facebook.com/docs/messenger-platform/)


## Build and running the service
Steps to Start the flask server

#### i. Create config.py file in server directory to store configuration

The file config.py contains the database url and other flask related config parameters which are used by the service.
Sample file looks like below:
```
DATABASE_URL = 'insert database url'
TESTING = True
DEBUG = True
FLASK_ENV = 'development'
```
#### ii. Virtual Environment activation and installing dependencies
```
$ cd server
$ python3 -m virtualenv tp_env        # create the virtual environment
$ source tp_env/bin/activate          # activate the virtual environment
$ pip install -r requirements.txt   # install all dependencies
```
#### iii. Run the server
Flask server is started by running
```
$ python -m flask run
```
## Testing the service

### i. Unit and System Tests

We have used pytest to run our unit and system tests.

To run unit and system/integration tests:
```
$ (tp_env) ./run_unit_integration_tests.sh 
```
The unit and system/integration test reports are created in the `./reports/tests/` directory . Each file has the timestamp to maintain report history.

### ii. Style checker

To run pylint style checker:
```
$ (tp_env) ./run_style_checker.sh 
```

Style checker reports are created in `./reports/style_bug_checker/` directory . Each file has the timestamp to maintain report history.

## Deploy service to Heroku

```
$ heroku login
$ heroku create <app_name>
$ git init
$ heroku git:remote -a <app_name>
$ git add .
$ git commit -m "Talking potatoes service initial commit"
$ git push heroku main
```
The service will be available at https://<app_name>.herokuapp.com
