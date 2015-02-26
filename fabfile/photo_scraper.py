## direction: hit database to find all parks with less than 3 photos. We need a postgis grid of bounding boxes. 
## We need to select out bounding boxes that intersect with the park queryset. 
## Then, iterate over each bounding box, making a call to the Flickr.photos.search endpoint. 
## the results should be loaded into a dbm, with coordinates. 
## the dbm should somehow be queried spatially against the filtered tables? This is because flickr returns only bounding boxes..
## Finally, join images spatially. ST_Intersect where each coord intersect with a park. Get that park's id because Parkimage is related to Park id. 
# http://gis.stackexchange.com/a/16390



from fabric.api import cd, run, put, env, task
from settings import PROJECT_ROOT, DJANGO_APP_PATH, CURATE_PATH
import anydbm
import csv
import os
import flickrapi
import sys
from fabric.contrib import django
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.settings_module('bostongreenmap.settings')
from parks.models import Park, Parkimage, get_extent_for_openlayers
from django.db import connection
from parks.models import Park, Parkimage
from django.db.models import Count
from django.contrib.gis.geos import Point, Polygon


MIN_PICTURE_COUNT=3


def get_parks():
	cursor = connection.cursor()
	parks_needing_images = Park.objects.annotate(num_photos=Count('images')).filter(num_photos__lt=MIN_PICTURE_COUNT)
	query_extent = get_extent_for_openlayers(parks_needing_images, 26986)
	print query_extent
	nrow = int((abs(query_extent[1][1]) - abs(query_extent.coords[0][1]))/0.0025)
	ncol = int((abs(query_extent[0][0]) - abs(query_extent.coords[1][0]))/0.0025)
	### fishnet function
	query = """CREATE OR REPLACE FUNCTION ST_CreateFishnet(
        nrow integer, ncol integer,
        xsize float8, ysize float8,
        x0 float8 DEFAULT 0, y0 float8 DEFAULT 0,
        OUT "row" integer, OUT col integer,
        OUT geom geometry)
    RETURNS SETOF record AS
		$$
		SELECT i + 1 AS row, j + 1 AS col, ST_Translate(cell, j * $3 + $5, i * $4 + $6) AS geom
		FROM generate_series(0, $1 - 1) AS i,
		     generate_series(0, $2 - 1) AS j,
		(
		SELECT ('POLYGON((0 0, 0 '||$4||', '||$3||' '||$4||', '||$3||' 0,0 0))')::geometry AS cell
		) AS foo;
		$$ LANGUAGE sql IMMUTABLE STRICT;
		SELECT ST_AsText(ST_Envelope(ST_Transform(ST_SetSRID(cells.geom,4326),4326))) AS bbox
		FROM ST_CreateFishnet({0}, {1}, 0.0025,0.0025, {2},{3}) AS cells;
	""".format(nrow,ncol,query_extent.coords[0][0],query_extent.coords[0][1])
	print query
	cursor.execute(query);
	print len(cursor.fetchall())
		

@task
def flickr_connect():
	flickr_key = os.environ.get('FLICKR_KEY')
	flickr_secret = os.environ.get('FLICKR_SECRET')
	bbox = "-71.1454299600001, 42.3716373610001, -71.1429299600001, 42.3741373610001"
	flickr = flickrapi.FlickrAPI(flickr_key, flickr_secret, format='parsed-json')
	# photos = flickr.photos.search(bbox= bbox, extras="license, geo, date_upload, owner_name")
	get_parks()
	# print(photos['photos']['total'])

# SELECT ST_AsText(ST_Envelope(cells.geom)) AS bbox
# FROM ST_CreateFishnet(4, 6, 10, 10) AS cells;

# SELECT ST_AsText(ST_Envelope(ST_Transform(ST_SetSRID(cells.geom,4326),26986))) AS bbox
# FROM ST_CreateFishnet(4, 6, 0.0025,0.0025, -71,42) AS cells;

# @task
# def write_curated_images_to_models():
# 	park_info = curated_park_info()
# 	count = 0
# 	for url, park_id, is_curated:
# 		# get the park
# 		try:
# 			park = Park.get(id=)
# 		# if you have a park, create a new Parkimage and save it

# 		# add that to the Park

def get(url):
	run("wget '{}'".format(url))
	split_name = url.split('/')
	picture_name = split_name[len(split_name)-1]
	return picture_name

def curated_park_info():
	file_path = PROJECT_ROOT+ '/media/parkmasterimages1.0.csv'
	park_info = []
	count = 0
	with open(file_path) as park_csv:
		for raw in csv.reader(park_csv, delimiter=","):
			if count == 0:
				# print [(i, x) for i, x in enumerate(tuple(raw))]
				count+=1
				continue

			row = tuple(raw)
			img_url, os_id, is_curated = row[15], row[1], bool("true")

			if is_curated:
				park_info.append( (img_url, os_id ) )
			count += 1
	return park_info


@task
def download_photos():
	db = anydbm.open('has_been_downloaded_2', 'c')
	with cd(env.code+'/../media/default_images'):
		download_count = 0
		skipped_count = 0
		for img_url, os_id in curated_park_info():
			try:
				if not img_url in db:
					picture_name = get(img_url)
					db[img_url] = picture_name
					download_count += 1
				else:
					skipped_count += 1
			except Exception as e:
				print e
			# print "%s in dbm: %s" % (key, key in db)
	print "Files Downloaded: %s" % download_count
	print "Files Skipped: %s" % skipped_count
	db.close()

@task
def write_photos_to_filesystem():
	park_info = curated_park_info()
	db = anydbm.open('has_been_downloaded_2', 'r')
	for img_url, os_id in park_info:
		if img_url in db[img_url]:
			photo_path = db[img_url]
			print img_url, photo_path

def setup_django_env():
	from django.conf import settings
	settings.configure(
	    DATABASE_ENGINE = 'postgresql_psycopg2',
	    DATABASE_NAME = 'db_name',
	    DATABASE_USER = 'db_user',
	    DATABASE_PASSWORD = 'db_pass',
	    DATABASE_HOST = 'localhost',
	    DATABASE_PORT = '5432',
	    TIME_ZONE = 'America/New_York',
	)


@task
def add_photos_to_db():
	### DJANGO CONFIGURATION SETUP ###
	import sys
	from fabric.contrib import django
	sys.path.append(PROJECT_ROOT)
	os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
	django.settings_module('bostongreenmap.settings')
	from parks.models import Park, Parkimage
	### END DJANGO SETUP #############

	db = anydbm.open('has_been_downloaded_2', 'r')
	for img_url, os_id in curated_park_info():
		if img_url in db:
			try:
				park = Park.objects.get(os_id=os_id)
			except Exception as e:
				print e
				continue

			### Create the image row and relate it to the Park
			filename = db[img_url]
			new_image_path = CURATE_PATH + '/' + filename

			p_img, created = Parkimage.objects.get_or_create(image=new_image_path, default=True)
			if created:
				park.images.add(p_img)
				# new_image = Parkimage.objects.get_or_create()
				print new_image_path + " added to " + park.name + "with id " + str(park.id)