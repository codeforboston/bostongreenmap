# Boston Green Map

A map promoting green spaces in the Metro Boston Area.

## Features

* Discover green spaces in a neighborhood
* Find green spaces for an activity
* See how to get to green spaces by foot, bike or transit

## Data Schema Basics

The map is based entirely on open space data in the public domain.

The core concept of the application is very simple and should be applicable for green spaces in any community or location. There are 3 basic elements that build the heart of the application: Park, Facility and Activity.

> A park visitor can perform *Activities*, such as playing Frisbee or Football, on a *Facility*, such as a Field, in a *Park*. 

This means, the 3 basic elements relate to each according to the following schema:

    Park [OneToMany] Facility [ManyToMany] Activity

A *Facility* can only be located in one single *Park*, whereas a visitor potentially can perform multiple *Activities* on a single *Facility*.

There are more elements, such as Neighborhoods, Parkowners, Types, etc., to the data schema, but those 3 ones are essential to understand the philosophy of the application.

## Installation

The Boston Green Map is a [Django](https://www.djangoproject.com/) project with spatial functionality, also called GeoDjango. Data storage and enabler for most spatial functionality is the [PostgreSQL](http://www.postgresql.org/) extension [PostGIS](http://postgis.net/). Minimum requirements for running this project are therefore Python and PostgreSQL/PostGIS. 

### PostgreSQL/PostGIS setup

The following steps ouline basic steps to install and configure the databasse requirements on Mac OS or Ubuntu Linux. For installation under Windows, please see the [installer packages for PostgreSQL/](http://www.enterprisedb.com/products-services-training/pgdownload), it includes PostGIS. Configuration should be similar, however, it will most likely by via GUI tools. 

#### PostGIS setup on Mac OS X (with [homebrew](http://mxcl.github.com/homebrew/))

1. Install PostGIS
        
    Install PostGIS and all its dependencies:

        brew install postgis
    
    Initialize PostgreSQL data directory:

        initdb /usr/local/var/postgres

    Start PostgreSQL database server:

        pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
 
2. Create PostGIS database template
 
        createdb postgis_template
        createlang plpgsql postgis_template
        psql -d postgis_template -f /usr/local/Cellar/postgis/2.0.3/share/postgis/postgis.sql
        psql -d postgis_template -f /usr/local/Cellar/postgis/2.0.3/share/postgis/spatial_ref_sys.sql
        psql -d postgis_template -f /usr/local/Cellar/postgis/2.0.3/share/postgis/rtpostgis.sql
        psql -d postgis_template -f /usr/local/Cellar/postgis/2.0.3/share/postgis/topology.sql
        psql -d postgis_template -c "GRANT ALL ON geometry_columns TO PUBLIC;"
        psql -d postgis_template -c "GRANT ALL ON geography_columns TO PUBLIC;"
        psql -d postgis_template -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

#### PostGIS setup on Ubuntu

1. Install PostGIS

    Add UbuntuGIS packages
    
        sudo add-apt-repository ppa:ppa:ubuntugis/ppa
        sudo apt-get update

    Install PostGIS and all dependencies
    
        sudo apt-get install postgresql-9.1-postgis

    To build PostgreSQL adapter for Python you'll probably make sure to have `python-dev` and `postgresql-9.1-dev` installed too.

2. Create PostGIS database template

        createdb -E UTF8 postgis_template
        createlang -d postgis_template plpgsql
        psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='postgis_template'"
        psql -d postgis_template -f /usr/share/postgresql/9.1/contrib/postgis-2.0/postgis.sql
        psql -d postgis_template -f /usr/share/postgresql/9.1/contrib/postgis-2.0/spatial_ref_sys.sql
        psql -d postgis_template -f /usr/share/postgresql/9.1/contrib/postgis-2.0/rtpostgis.sql
        psql -d postgis_template -f /usr/share/postgresql/9.1/contrib/postgis-2.0/topology.sql
        psql -d postgis_template -c "GRANT ALL ON geometry_columns TO PUBLIC;"
        psql -d postgis_template -c "GRANT ALL ON geography_columns TO PUBLIC;"
        psql -d postgis_template -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

#### Create a django database user

    createuser django
        Shall the new role be a superuser? (y/n) n
        Shall the new role be allowed to create databases? (y/n) y
        Shall the new role be allowed to create more new roles? (y/n) n
    psql
        # ALTER ROLE django WITH PASSWORD 'django';
        ALTER ROLE
        # \q 

#### Create a database owned by the django user

        createdb -O django -T postgis_template bostongreenmap

### Python

Django 1.5 is a [Python](http://www.python.org/) module and requires Python 2.6.5 or higher.  

Python 2.7 comes pre-installed with most modern operating systems (Mac OS, Linux, etc.) and there are installers available for Windows. Please see  installation instructions for your platform for more details.

To see if or which Python version is installed on your system, open a terminal or shell and type:

    python --version

### Virtual Environments

It is good practice to sandbox and isolate Python projects from each other. The `virtuelenv` tool helps to do that and prevents potential future version conflicts among Python modules. The tool `virtualenvwrapper` is a convenience helper that makes `virtualenv` a little easier to use. The following steps will install both:

1. Install `pip`, a Python package management system.

    Please follow the installation instructions for your platform: [pip installation](http://www.pip-installer.org/en/latest/installing.html)

2. Install `virtualenvwrapper` and `virtualenv`

        pip install virtualenvwrapper

    Initialize virtualenvwrapper in your shell startup file (`~/.bashrc`, `~/.profile`, etc.):
        
        export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
        export WORKON_HOME=~/.venvs
        source /usr/local/bin/virtualenvwrapper.sh
        export PIP_DOWNLOAD_CACHE=$HOME/.pip-downloads

3. Create new virtual environment:

        mkvirtualenv bostongreenmap

### Get a local copy of the project

    git clone https://github.com/codeforboston/bostongreenmap.git
    cd bostongreenmap

*[Download](https://github.com/codeforboston/bostongreenmap/archive/master.zip) the project manually if you're not familier with `git`*

### Setup the Django project

Activate previously created virtual environment:

    workon bostongreenmap

Install all project dependencies:

    pip install -r requirements.txt

Create a private config file in `bostongreenmap/bostongreenmap/local_settings.py` with at least the following content:

    from settings import *
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis', 
            'NAME': 'bostongreenmap', 
            'USER': 'django', 
            'PASSWORD': 'django', 
            'HOST': 'localhost', 
            'PORT': '5432', 
        }
    }

Tell Django to create all necessary database tables, and create a project superuser if it doesn't exist yet:

    python manage.py syncdb

Some requirements are managed by a third party data migration module. Apply all migrations:

    python manage.py migrate

### Import sample data

This command will import the Boston Common Park and a related facility and activity.

    python manage.py loaddata fixtures/sample.json

### Run a local development server

    python manage.py runserver

Access the site at [http://localhost:8000](http://localhost:8000).
    
## Project History

The first iteration of this project was created during Boston's Hack Day Challenge in 2011. A team of 7 volunteers (Christian Spanring, David Norcott, David Rafkind, Holly St. Clair, Patrick Robertson, Peter Gett, Tom Morris) prototyped the application in 48 hours, which was among the [winners of the challenge](http://www.boston.com/business/technology/innoeco/2011/02/winners_of_the_first-ever_bost.html). The original code repository is still available and can be found here: [https://github.com/bostongreen/bostongreen](https://github.com/bostongreen/bostongreen).

After the challenge, the Metropolitan Area Planning Council (MAPC), the employer of 2 of the volunteers, worked with Boston Parks Advocates and a group of Boston Parks Trustees to turn the application into a service for people who live and work in the Metro Boston Area. 

The code repository was moved to Code for Boston's GitHub account in Spring 2013. Code for Boston seems to be an excellent home for the project: it started as volunteer effort and should be owned by volunteers, it is a public service application built on top of open data and it is an open source project than can be replicated with local green space data in any other community.

---

© Boston Green Map contributors
