# PWP-ImageDirectory

Imagedirectory is a dockerized application including a Flask backend and frontend. In this application people can share their daily images, like other images, and add comments.

## Group Information

- Nazanin Nakhaie Ahooie
- Mehrdad Kaheh
- Danial Khaledi
- Sepehr Samadi

## Database

The database system and its entities and their relations has been explained in the [wiki page](https://github.com/daniiialll72/PWP-ImageDirectory/wiki). For this implementation we used Mongodb and mongoengine as an ORM. Here is a brief description of these systems:

Minio is an open-source object storage server that is compatible with Amazon S3 cloud storage service. It provides an API that allows developers to store and retrieve objects in a simple and scalable manner. Minio is designed to be lightweight and easy to deploy, making it an ideal solution for developers who need object storage for their applications.

MongoDB, on the other hand, is a NoSQL document-based database that uses a flexible and scalable document model to store data. It is a popular database choice for modern web applications because it provides a flexible schema that can evolve with the changing needs of an application. MongoDB also provides advanced features like sharding and replication that allow it to scale horizontally across multiple servers.

## Object Storage

For keeping the images in a secure and performant way, we have chosen MINIO, which is a dockerized object storage. Not to mention that the metadata of the image is kept in Mongodb.

## Flask

In the flask side, we approached a neat RESTful mechanism. All the entities have their own resources and respective models. We have employed flask_restful to handle all the routings and flask blueprints.

In development mode, you can go to `src` directory and execute following commands

```
$ export FLASK_APP=imagedirectory
$ export FLASK_ENV=development
$ flask run --port=5000
```

## Running in the production mode

In order to run the application you just need to install docker on the target machine. Afterwards, by executing the following commands, all the requirements will be run on respective docker container

```
docker compose up --build -d
```

In order to stop the application run the following commands

```
docker compose down
```
