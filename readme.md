# Mapping system to record spatial data using Python, Django, Leaflet, Docker and PostgresSQL 

Here I developed a webmap system to record locations/data to be used as a tool in the Sun Coral monitoring program at REBIO Arvoredo. The technology used is a Django Restful Framework (with Geodjango extension), Imagery from Leafleat Javascript Library and PostgresSQL db runing with Docker. 

The start point was this post [post](https://www.paulox.net/2021/07/19/maps-with-django-part-2-geodjango-postgis-and-leaflet/#abstract) from [Paolo Melchiorre](https://github.com/pauloxnet). Some customization where done in onder do adequate my system needs, in this case windows 11. This is a working in progress...

## Starting the project
### Install Python
Here we used Python 3.10.2.

```python

$ python --version
Python 3.10.2

```
### Creating Python virtual env

```python

$ python -m venv ~/.mymap
$$ source ~/.mymap/bin/activate

```

### Installing latest stable version of Django (tested with Django 3.1-3.2)

```python

$ python -m pip install django~=3.2

```

### Creating `mymap` project

To create the mymap project I switch to my projects directory:

```python

$ cd ~/projects

```

and then use the `startproject` Django command:

```python

$ python -m django startproject mymap

```

After run this command will be created a new directory named `mymap` with the standard files to start the app development.

### Creating markers app

Navigate to `mymap` directory

```python

$ cd mymap

```

Start the django app with the command:

```python 

$ python3 -m django startapp markers

```

### Activating markers app

The activation of markers application is done by inserting its name in the list of the INSTALLED_APPS in the mymap settings file.

`mymap/mymap/settings.py`

```python

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "markers",
]

```
## Creating an empty web map

### Adding a template view

Insert in the `views.py` file, a new `TemplateView` for the page of our map.

`mymap/markers/views.py`

```python

"""Markers view."""

from django.views.generic.base import TemplateView


class MarkersMapView(TemplateView):
    """Markers map view."""

    template_name = "map.html"

```

### Creating the map template

```python

$ mkdir templates

```

In the *markers* template directory we can now create a map.html template file for our map. For now we added only title but without a body content.

`mymap/markers/templates/map.html`

```html

<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Markers Map</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  </head>
  <body>

  </body>
</html>

``` 

### Adding markers urls

In the markers URL file we must now add the path to view our map, using its template view.

`mymap/markers/urls.py`

```python

"""Markers urls."""

from django.urls import path

from markers.views import MarkersMapView

app_name = "markers"

urlpatterns = [
    path("map/", MarkersMapView.as_view()),
]


```

### updating  myma urls

In this step we must include the URL file on the *marker* app. See [Django documents](https://docs.djangoproject.com/en/4.0/ref/urls/) about urls path. Creating url inside `mymap/mymap` just made a first view in Django, but it will show a blank page.

`mymap/mymap/urls.py`

```python

"""mymap URL Configuration."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("markers/", include("markers.urls")),
]

```
### Testing blank map on server

In order to test the blank map page you should start a python server:

```python

$ python manage.py runserver

```
Now that the server’s running, visit http://127.0.0.1:8000/markers/map/ with your Web browser. You’ll see a working blank map page.

## Leaflet
### Why [Leafleat](https://leafletjs.com/)
+ The most used javascript library for web maps apps
+ Free software
+ Friendly for desktop and mobile
+ Very ligth (~39 kb of gzippes JS)
+ Well documented
### Updatign map template HTML/CSS/JS
### HTML

We need some updates in HTML to prepare it to display the map in th app.
Basically, were inserted:
+ link to CSS
+ link Leafleat CSS
+ Sourcing to Leafleat JS
+ A DIV in the body, with the ID *map*  

```html

{% load static %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Markers Map</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" type="text/css" href="{% static 'map.css' %}" />
    <link rel="stylesheet" type="text/css" href="https:///unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https:///unpkg.com/leaflet/dist/leaflet.js"></script>
  </head>
  <body>
    <div id="map"></div>
    <script src="{% static 'map.js' %}"></script>
  </body>
</html>

```
### Creating static diretory

We must create a new directory to store the CSS ans JS files linked to HTML

```python

$ mkdir static

```

### Map CSS

Add the folowing CSS file to static folder:

`mymap/markers/static/map.css`

```css

html,
body {
    height: 100%;
    margin: 0;
}
#map {
    height: 100%;
    width: 100%;
}


```
### Map JavaScript

`mymap/markers/static/map.js`

```javascript

const copy = "© <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const osm = L.tileLayer(url, { attribution: copy });
const map = L.map("map", { layers: [osm] });
map.fitWorld();

```

### Test it on server

At this point the django project can be tested with the ‘runserver’

```python

$ python manage.py runserver

```


### Install GDAL

Check the [Django documentation](https://docs.djangoproject.com/en/4.0/ref/contrib/gis/install/) to set GDAL in your machine. There are some different process according your OS (mac, windows and linux).
### Activate geodjango

The GeoDjango activation is done by adding the django.contrib.gis module to the INSTALLED_APPS, in our project `settings.py` file.

```python

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "markers",
]

```
### Installing PostgresSQL windows 10

Download the latest PostgreSQL 12.x installer from the EnterpriseDB website. After downloading, run the installer, follow the on-screen directions, and keep the default options unless you know the consequences of changing them.

### PostGIS

From within the Stack Builder (to run outside of the installer, Start ‣ PostgreSQL 12 ‣ Application Stack Builder), select PostgreSQL 12 (x64) on port 5432 from the drop down menu and click next. Expand the Categories ‣ Spatial Extensions menu tree and select PostGIS X.Y for PostgreSQL 12.

## OSGeo4W

The OSGeo4W installer helps to install the PROJ, GDAL, and GEOS libraries required by GeoDjango. First, download the OSGeo4W installer (64bit), and run it. Select Express Web-GIS Install and click next. In the ‘Select Packages’ list, ensure that GDAL is selected; MapServer is also enabled by default, but is not required by GeoDjango and may be unchecked safely. After clicking next and accepting the license agreements, the packages will be automatically downloaded and installed, after which you may exit the installer.

### Install Docker

Go to docker homepage and choose the version according your OS.  Then you double click the Docker.app and it should start. You can check if it's working when there is a Docker icon on the top right next to your other small icons. If this is the case you can quickly follow the 'Hello World' example to get up and running.

### Create a Postgres database

Just to ilustrate, it showed bellow the easiest way of running a clean Postgres database is by running this command in a terminal window (after Docker has been installed):

```python

$ run --name postgres-db -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres

```
#### What does it do?

+ -d means that you enable Docker to run the container in the background
+ -p plus the port numbers means you map the containers port 5432 to the external port 5432 - this allows you to connect to it from the outside
+ POSTGRES_PASSWORD sets the password to docker. This is the password that gives you access to your database
+ the —name property gives your container a name and means you can easily find it back
+ Last section of the command grabs the latest 'postgres' Docker image from the Docker Hub

After knowing how to creae a PostgresSQL database in command line, it is a better approach create the container in docker using a `docker compose yml`. Here we  create the database using `docker compose yml`, it is a better way to record your how the things were done. Create a folder `docker` an them create the file `docker-compose.yml`, this file will give the instructions to the container creation. 

`mymap/docker/docker-compose.yml`

```python
version: "3"
services:
    database: 
        image: "postgres:latest"
        ports:
      - 5432:5432
      environment:
      POSTGRES_USER: postgres # The PostgreSQL user (useful to connect to the database)
      POSTGRES_PASSWORD: docker # The PostgreSQL password (useful to connect to the database)
      POSTGRES_DB: default_database # The PostgreSQL default database (automatically created at first launch)
    volumes:
        # In this example, we share the folder *db-data* in our root repository, with the default PostgreSQL data path.
        # It means that every time the repository is modifying the data inside
        # of `/var/lib/postgresql/data/`, automatically the change will appear in *db-data*.
        # You don't need to create the *db-data* folder. Docker Compose will do it for you.
        - ./db-data/:/var/lib/postgresql/data/

```

To start the container creation run the following command. The container will be created, aldo a folder will be create inside the docker folder. Don't forget to turn on docker desktop. After while you will see in your docker desktop the container just created

```python 
$ cd docker
$ docker-compose up

```

When you finish working on your project, I recommend you to stop the running Postgres Docker container using the command below:

```python

$ docker-compose down

```
### Connect the Postgres DB to the app

Now the next step is to connect to this brand new Postgres database to communicate with database **mymap** app. We modify the project database settings, adding the PostGIS engine and the connection parameters of our PostgreSQL database, which you may have locally or remotely. You need to use the following connection details to actually connect to the DB on settings file:

`mymap/mymap/settings.py`

```python
DATABASES = {
 
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": "localhost",
        "NAME": "postgres",
        "PASSWORD": "docker",
        "PORT": 5432,
        "USER": "postgres",
    }
}

```

Note if you are using a localhost, you must provide the same password when you installed Postgres in your machine. 

### Updating the database 

We can now generate a new database migration and then apply it to our database. In the context of a data base, the command `makemigrations` which is responsible for creating new migrations based on the changes you have made to your models. The command `migrate` which is responsible for applying and unapplying migrations. You should think of migrations as a version control system for your database schema.

```python

$ python manage.py makemigrations
$ python manage.py migrate

```
### Testing the admin

We have to create an admin user to login and test it. You will be promted to create na user and a password.

```python

$ python manage.py createsuperuser

```
After this you can test the admin running this command:

```python

$ python manage.py runserver

```

Now you have the app running in server, access  http://127.0.0.1:8000/admin/markers/marker/add/ with your Web browser. You’ll see a “Markers” admin page, insert the `user` and `password` just created as superuser to add new markers with a map widget.

### Showing markers in the map
#### Requirements file
We’re going to use additional packages for our advanced map: Django filter, Django REST Framework (DRF) and its geographic add-on. Django Rest Framework lets you create RESTful APIs: A way to transfer information between an interface and a database in a simple way. The way to do it so is listing the packages in the `requirements.txt` file.

`mymap/requirements.txt`

```python

django-filter~=21.1
djangorestframework-gis~=0.17
djangorestframework~=3.12.0
django~=3.2.0
psycopg2-binary~=2.9.0

```
### Installing the requirements

We install all the Python requirements, using the python package installer module.

```python

$ python -m pip install -r requirements.txt

```
## Activating Django REST Framework¶

The packages that we’ll use directly in the code of our project are Django REST Framework and its geographic add-on which we then insert in the list of INSTALLED_APPS of our project settings.

`mymap/mymap/settings.py`

```python

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "rest_framework",
    "rest_framework_gis",
    "markers",
]

```
### Adding the Marker serializer

Let’s create a serializer for our Marker class. Inheriting from a ‘rest_framework_gis’ serializer, we only have to define the Marker model, the geographical field ‘location’ and also the optional fields, to be shown as additional properties. 

obs: customize here to insert others fields concerning the monitoring at rebio

`mymap/markers/serializers.py`

```python

"""Markers serializers."""

from rest_framework_gis import serializers

from markers.models import Marker


class MarkerSerializer(serializers.GeoFeatureModelSerializer):
    """Marker GeoJSON serializer."""

    class Meta:
        """Marker serializer meta class."""

        fields = ("id", "name")
        geo_field = "location"
        model = Marker

```

The `GeoFeatureModelSerializer serializer` will generate a GeoJSON like this:

```json

{
    "type": "FeatureCollection",
    "features": [
    {
        "id": 1,
        "type": "Feature",
        "geometry": {
        "type": "Point",
        "coordinates": [14.085910318319995, 42.086280141658]
        },
        "properties": {
        "name": "Monte Amaro 2793m 🇮🇹"
        }
    }
    ]
}

``` 
### Adding a Marker viewset

Our intention is to expose our markers via a RESTful API and to do so we define a read-only viewset.
1. We set the location as a field to filter our markers, and then a filter based on the bound box.
2. We also return all our Marker instances, without limitations or filters.

`mymap/markers/viewsets.py`

```python

"""Markers API views."""
from rest_framework import viewsets
from rest_framework_gis import filters

from markers.models import Marker
from markers.serializers import MarkerSerializer


class MarkerViewSet(viewsets.ReadOnlyModelViewSet):
    """Marker view set."""

    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

```

### Adding API ‘markers’ urls

In the `markers` application, we define the URL of our new endpoint using the Django REST Framework default router, to create our path.

`mymap/markers/api.py`

```python

"""Markers API URL Configuration."""

from rest_framework import routers

from markers.viewsets import MarkerViewSet

router = routers.DefaultRouter()
router.register(r"markers", MarkerViewSet)

urlpatterns = router.urls

```

### Updating ‘mymap’ urls

Finally, we add to the definition of the URL of our project, a new path for the API that includes the path just specified for our ‘marker’ app.

`mymap/mymap/urls.py`

```python

"""mymap URL Configuration."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("markers.api")),
    path("markers/", include("markers.urls")),
]

```
### Trying to locate the user

After finishing our RESTful API we move-on to updating our javascript file.

Here we configure the `leaflet` methods which will run in our app. One of those are try to locate the user: in the positive case we’ll use it’s location to center the map, in the negative case we’ll locate him on an arbitrary point in the map, with a low zoom level.

`mymap/markers/static/map.js`

```javascript

const copy = "© <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const osm = L.tileLayer(url, { attribution: copy });
const map = L.map("map", { layers: [osm], minZoom: 5 });
map.
    locate()
    .on("locationfound", (e) => map.setView(e.latlng, 8))
    .on("locationerror", () => map.setView([0, 0], 5));

/*continue*/

``` 

### Rendering markers incrementally

We ask our endpoint to return only the markers of the specific displayed area, passed as a boundbox string.
To build the marker layer, we ask our endpoint for data asynchronously and extract the properties we want to show in the pop-ups.
We invoke this flow, every time the user stops moving on the map.

´mymap/markers/static/map.js´

```javascript

/*js continuation*/


async function load_markers() {
    const markers_url = `/api/markers/?in_bbox=${map.getBounds().toBBoxString()}`
    const response = await fetch(markers_url)
    const geojson = await response.json()
    return geojson
}

async function render_markers() {
    const markers = await load_markers();
    L.geoJSON(markers)
    .bindPopup((layer) => layer.feature.properties.name)
    .addTo(map);
}

map.on("moveend", render_markers);

```

### Testing the populated map

The loading takes place in a very fluid way, because the number of calls occurs only when the movement on the map stops and therefore the data traffic is reduced to the essentials as well as the rendering of the markers carried out by Leaflet.

You can test the populated web map running this command:

```python

$ python manage.py runserver

```

## Usefull Resourcers
+ [GeoDjango](https://docs.djangoproject.com/en/4.0/ref/contrib/gis/)
+ [LeaFleat](https://leafletjs.com/)
+ [PostgresSQL](https://www.postgresql.org/)
+ [Docker compose](https://dev.to/andre347/how-to-easily-create-a-postgres-database-in-docker-4moj) 
+ [Docker compose](https://herewecode.io/blog/create-a-postgresql-database-using-docker-compose/) 
+ [Creating PostgresSQL container via yml file docker compose](https://herewecode.io/blog/create-a-postgresql-database-using-docker-compose/)
+ [Setting path to GDAL](https://newbedev.com/geodjango-on-windows-try-setting-gdal-library-path-in-your-settings)






