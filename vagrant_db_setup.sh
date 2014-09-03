#!/bin/bash -x

# Because there is a botched migration somewhere, dumping data only does not work.
# We dump the database in it's entirety, with all relations intact.
# In the future we must fix migrations so that the fixtures file can be data-only.
# For now, we remove all existing relations, then read the dump entirely.
# Always version the dump data when updating, forcing the user to always update the documentation

# Debugging
# ‘Role “User” not found’
# Not everyone might be running using vagrant setup. If they are not, when they export
# the sql dump, they may not have the user of the database set as 'django', which is the default. 
# If that is the case, you must edit the sql file directly.

DJANGO_ROOT=/home/vagrant/bostongreenmap
SQL_FILENAME=$DJANGO_ROOT/bostongreenmap_dump.sql

echo 'This script assumes that you have a sql data dump in a file alled bostongreen_dump.sql at the root of the django directory'

# ensure sql file is readable
chmod a+r $SQL_FILENAME

sudo su postgres <<EOF

# Do the unfortunate hack of removing the entirety of the old database
psql bostongreenmap <<EOF2
drop schema public cascade;
create schema public;
\q
EOF2

# Import new data
psql bostongreenmap < $SQL_FILENAME

# Unfotunately, the dump does not have permissions on the postgis table spatial_ref_sys set correctly. Reset it manually.
# django is the default user when using vagrant
psql bostongreenmap <<EOF2
grant all privileges on table spatial_ref_sys to django;
\q
EOF2

EOF

