# Boston Green Map

A map promoting green spaces in Metro Boston.

## Features

* Discover green spaces in a neighborhood
* Find green spaces for an activity
* See how to get to green spaces by foot, bike or transit

## Data Schema Basics

There are 3 core elements that build the backbone of the application: Park, Facility and Activity.

A park visitor can perform *Activities*, such as playing Frisbee or Football, on a *Facility*, such as a Field, in a *Park*. This means, that the 3 core elements are using the following relations to each other:

    Park [OneToMany] Facility [ManyToMany] Activity

A *Facility* can only be located in one single *Park*, whereas a visitor potentially can perform multiple *Activities* on a single *Facility*.

There are more elements, such as Neighborhoods, Parkowners, Types, etc., to the data schema, but those 3 ones are essential to understand the philosophy of the application.

## Installation

The Boston Green Map is a [Django](https://www.djangoproject.com/) project that relies on a data storage with spatial capabilities, such as [PostGIS](http://postgis.net/).

### Django setup

1. Create a virtual environment 

        # Setup virtualenv tools
        $ sudo pip install virtualenvwrapper

        # Add virtualenvwrapper to your environment
        $ export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
        $ export WORKON_HOME=~/.venvs
        $ source /usr/local/bin/virtualenvwrapper.sh
        $ export PIP_DOWNLOAD_CACHE=$HOME/.pip-downloads

        # Setup a virtualenv for the project
        $ mkvirtualenv bostongreenmap

2. Activate virtual environment

        $ workon bostongreenmap

3. Install project dependencies

        $ pip install -r requirements

### PostGIS setup on Ubuntu

1. Install PostGIS

        # Add UbuntuGIS packages
        $ sudo add-apt-repository ppa:ppa:ubuntugis/ppa
        $ sudo apt-get update

        # Install PostGIS
        $ sudo apt-get install postgresql-9.1-postgis

2. Create PostGIS database template

        $ createdb -E UTF8 postgis_template
        $ createlang -d postgis_template plpgsql
        $ psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='postgis_template'"
        $ psql -d postgis_template -f /usr/share/postgresql/9.1/contrib/postgis-2.0/postgis.sql
        $ psql -d postgis_template -f /usr/share/postgresql/9.1/contrib/postgis-2.0/spatial_ref_sys.sql
        $ psql -d postgis_template -f /usr/share/postgresql/9.1/contrib/postgis-2.0/rtpostgis.sql
        $ psql -d postgis_template -f /usr/share/postgresql/9.1/contrib/postgis-2.0/topology.sql
        $ psql -d postgis_template -c "GRANT ALL ON geometry_columns TO PUBLIC;"
        $ psql -d postgis_template -c "GRANT ALL ON geography_columns TO PUBLIC;"
        $ psql -d postgis_template -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

        # Test
        $ createdb test -T postgis_template
        $ psql -d test

3. Create bostongreenmap database

        $ createdb -T postgis_template bostongreenmap

### PostGIS setup on Mac OS X (with [homebrew](http://mxcl.github.com/homebrew/))

1. Install PostGIS
 
        $ brew install postgis
        $ initdb /usr/local/var/postgres
        $ pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
 
2. Create PostGIS database template
 
        $ createdb postgis_template
        $ createlang plpgsql postgis_template
        $ psql -d postgis_template -f /usr/local/Cellar/postgis/2.0.3/share/postgis/postgis.sql
        $ psql -d postgis_template -f /usr/local/Cellar/postgis/2.0.3/share/postgis/spatial_ref_sys.sql
        $ psql -d postgis_template -f /usr/local/Cellar/postgis/2.0.3/share/postgis/rtpostgis.sql
        $ psql -d postgis_template -f /usr/local/Cellar/postgis/2.0.3/share/postgis/topology.sql
        $ psql -d postgis_template -c "GRANT ALL ON geometry_columns TO PUBLIC;"
        $ psql -d postgis_template -c "GRANT ALL ON geography_columns TO PUBLIC;"
        $ psql -d postgis_template -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

        # Test
        $ createdb test -T postgis_template
        $ psql -d test

## Project History

The first iteration of this project was created during Boston's Hack Day Challenge in 2011. A team of 7 volunteers (Christian Spanring, David Norcott, David Rafkind, Holly St. Clair, Patrick Robertson, Peter Gett, Tom Morris) prototyped the application in 48 hours, which was among the [winners of the challenge](http://www.boston.com/business/technology/innoeco/2011/02/winners_of_the_first-ever_bost.html). The original code repository is still available and can be found here: [https://github.com/bostongreen/bostongreen](https://github.com/bostongreen/bostongreen).

After the challenge, the Metropolitan Area Planning Council (MAPC), the employer of 2 of the volunteers, worked with Boston Parks Advocates and a group of Boston Parks Trustees to turn the application into a service for people who live and work in the Metro Boston Area. 

The code repository was moved to Code for Boston's GitHub account in Spring 2013. Code for Boston seems to be an excellent home for the project: it started as volunteer effort and should be owned by volunteers, it is a public service application built on top of open data and it is an open source project than can be replicated with local green space data in any other community.

---

© Boston Green Map contributors
