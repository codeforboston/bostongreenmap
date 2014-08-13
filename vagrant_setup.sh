#!/bin/bash -x
apt-get update -qq
apt-get install -y python-software-properties
apt-add-repository -y ppa:ubuntugis/ppa
add-apt-repository ppa:chris-lea/node.js
apt-get update -qq
apt-get install -y \
        python-pip \
        postgresql-9.1-postgis-2.0 \
        python-psycopg2 \
        libpq-dev \
        postgresql-client \
        python-dev \
        python-virtualenv \
        build-essential \
        ruby \
        rubygems \
        gem \
        curl \
        vim \
        nodejs

gem install --no-ri --no-rdoc sass -v 3.2.13
gem install --no-ri --no-rdoc compass -v 0.12.2

cd bostongreenmap/client
npm install -g grunt-cli # grunt-cli is global so we can just type 'grunt'
npm install # finally, install dependencies
grunt handlebars:compile
cd ../..

su postgres <<EOF
psql <<EOF2
update pg_database set datistemplate=false where datname='template1';
drop database template1;
create database template1 with owner=postgres encoding='UTF-8'

  lc_collate='en_US.utf8' lc_ctype='en_US.utf8' template template0;
update pg_database set datistemplate=true where datname='template1';
drop database postgis_template;
EOF2
createdb postgis_template -EUTF8
createlang plpgsql postgis_template
psql -d postgis_template -f /usr/share/postgresql/9.1/contrib/postgis-2.0/postgis.sql
psql -d postgis_template -f /usr/share/postgresql/9.1/contrib/postgis-2.0/spatial_ref_sys.sql
psql -d postgis_template -f /usr/share/postgresql/9.1/contrib/postgis-2.0/rtpostgis.sql
psql -d postgis_template -f /usr/share/postgresql/9.1/contrib/postgis-2.0/topology.sql
psql -d postgis_template -c "GRANT ALL ON geometry_columns TO PUBLIC;"
psql -d postgis_template -c "GRANT ALL ON geography_columns TO PUBLIC;"
psql -d postgis_template -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"
createuser django --no-password --createdb --no-createrole --no-superuser
psql <<EOF2
 ALTER ROLE django WITH PASSWORD 'django'
EOF2
createdb -O django -T postgis_template bostongreenmap
psql -f bostongreenmap/fixtures/green.sql bostongreenmap
EOF

if [ ! -d virtualenv ]; then
    virtualenv virtualenv
fi
cd virtualenv
source ./bin/activate
pip install -r ../bostongreenmap/requirements.txt
cd ..

cd bostongreenmap
if [ ! -f bostongreenmap/local_settings.py ]; then
    cat > bostongreenmap/local_settings.py <<EOF
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
EOF
fi

python manage.py syncdb --noinput
python manage.py migrate --noinput
