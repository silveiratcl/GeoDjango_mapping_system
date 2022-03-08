# Creating a web map system to record spatial data using Python, Django and Leaflet 

Here I developed a webmap system to record locations/data storing all data in a PostgresSQL db base using Docker. The start point was this post [post](https://www.paulox.net/2021/07/19/maps-with-django-part-2-geodjango-postgis-and-leaflet/#abstract) from [Paolo Melchiorre](https://github.com/pauloxnet). Some customization where done in onder do adequate my system needs. This is a working in progress...

## Installing geodjango windows 10 (Django Docs)

Download the latest PostgreSQL 12.x installer from the EnterpriseDB website. After downloading, run the installer, follow the on-screen directions, and keep the default options unless you know the consequences of changing them.

## PostGIS
From within the Stack Builder (to run outside of the installer, Start ‣ PostgreSQL 12 ‣ Application Stack Builder), select PostgreSQL 12 (x64) on port 5432 from the drop down menu and click next. Expand the Categories ‣ Spatial Extensions menu tree and select PostGIS X.Y for PostgreSQL 12.

## OSGeo4W
The OSGeo4W installer helps to install the PROJ, GDAL, and GEOS libraries required by GeoDjango. First, download the OSGeo4W installer (64bit), and run it. Select Express Web-GIS Install and click next. In the ‘Select Packages’ list, ensure that GDAL is selected; MapServer is also enabled by default, but is not required by GeoDjango and may be unchecked safely. After clicking next and accepting the license agreements, the packages will be automatically downloaded and installed, after which you may exit the installer.

## Install Docker

Go to docker homepage and choose the version according your OS. 
Then you double click the Docker.app and it should start. You can check if it's working when there is a Docker icon on the top right next to your other small icons. If this is the case you can quickly follow the 'Hello World' example to get up and running.

## Create a Postgres database

Hands down the easiest way of running a clean Postgres database is by running this command in a terminal window (after Docker has been installed):

```docker

docker run --name postgres-db -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres

```
### But what does it do?

+ -d means that you enable Docker to run the container in the background
+ -p plus the port numbers means you map the containers port 5432 to the external port 5432 - this allows you to connect to it from the outside
+ POSTGRES_PASSWORD sets the password to docker. This is the password that gives you access to your database
+ the —name property gives your container a name and means you can easily find it back
+ Last section of the command grabs the latest 'postgres' Docker image from the Docker Hub

Alternatively, you can create the database using `docker compose yml`

In this [post](https://herewecode.io/blog/create-a-postgresql-database-using-docker-compose/) I followed the steps to create the yml file. After the file creation you can run in order o create the container.

```docker

$ docker-compose up

```

Now the next step is to connect to this brand new Postgres database to communicate with database **mymap** app. We modify the project database settings, adding the PostGIS engine and the connection parameters of our PostgreSQL database, which you may have locally or remotely.
You need to use the following connection details to actually connect to the DB.

`mymap/mymap/settings.py`

```python
DATABASES = {
 
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": "localhost",
        "NAME": "postgres",
        "PASSWORD": "spatial78ptsrtm",
        "PORT": 5432,
        "USER": "postgres",
    }
}

```

stoped in Updating the database

https://dev.to/andre347/how-to-easily-create-a-postgres-database-in-docker-4moj - ok
https://herewecode.io/blog/create-a-postgresql-database-using-docker-compose/ - ok, better


Create a virtual environment for python and django
https://www.pointsnorthgis.ca/blog/geodjango-gdal-setup-windows-10/
follow this - uma bosta,




