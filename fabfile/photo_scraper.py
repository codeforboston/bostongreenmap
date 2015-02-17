from fabric.api import cd, run, put, env, task
from settings import PROJECT_ROOT, DJANGO_APP_PATH, CURATE_PATH
import anydbm
import csv
import os

CSV_FILE_PATH = os.path.join(
	os.path.dirname(__file__),
	"../media/parkmasterimages1.0.csv"
)

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