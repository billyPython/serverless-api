# Serverless API 

API provides simple authentication and authorization. 
That uses `postgres` as backend DB and 
`Sendgrid` as 3rd party software for sending emails.

## Language
python 3.7


## Libraries used:
1. `Flask python framework`
2. `psycopg2` ( Postgres python adapter )
3. [itsdangerous (Data singing module)](https://pythonhosted.org/itsdangerous/)


## Setup

1. Clone repo

## Run

In order to keep project portable and easy to use I'm suggesting using [docker](https://docs.docker.com/install/)
and also I've been using `Postgres` docker container exclusively. 

There is Dockerfile prepared, which will create an image of this project and 
also [docker-compose (tool for defining and running container apps)](https://docs.docker.com/compose/).
This docker-compose configuration contains both application and database settings up.

**1.1. Docker server**:

After installing docker and docker-compose you should go to the cloned repo and start server and db with:
```
export SENDGRID_API_KEY={send grid api key here}
docker-compose up -d --build
```

This will build, (re)create, start and pull container that are defined in `docker-compose.yaml`

 

**1.2. Python env Server**:

If you wish to run it from your python [environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

I. create virtual environment and activate in cloned repo, using above instructions.

II. Install requirements:
```
pip install -r requirements.txt
```

III. As mentioned before, `Postgres` docker container has been used. Run database:
```
docker run --name postgres-serverless-api -e POSTGRES_PASSWORD=sapi -e POSTGRES_USER=sapi -e POSTGRES_DB=serverless_api -d postgres
```

IV. Run application:
```
export SENDGRID_API_KEY={send grid api key here}
export FLASK_APP=serverless_api
export FLASK_DEBUG=1
flask run
```


# Instruction how to make this app serverless

## AWS

Configuring credentials for AWS you can follow these steps to quickly get started:
```$ mkdir ~/.aws
$ cat >> ~/.aws/config
[default]
aws_access_key_id=YOUR_ACCESS_KEY_HERE
aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
region=YOUR_REGION (such as us-west-2, us-west-1, etc)
```

## Zappa

After we have configured AWS we want to run 
this application with AWS Lambda + API Gateway

`Zappa` makes it easy to build and deploy python apps. Kind of "serverless" web hosting for python apps.
You can check more on how to configure and use Zappa here: https://github.com/Miserlou/Zappa


## Chalice

I would maybe recommend using `Chalice`, because it is "microframework" writen by AWS it self for fast creation and deployment of applications that use AWS Lambda.
Also, it is flask like.

You can read on how to configure and use `Chalice` on link below:

https://github.com/aws/chalice

## Interesting read:
https://read.iopipe.com/the-right-way-to-do-serverless-in-python-part-2-63430131239
