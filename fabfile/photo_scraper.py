from fabric.api import cd, run, put, env, task
import dbm
import csv
import os

from fabric.contrib import django
django.project('bostongreenmap')
# from bostongreenmap.parks import models

# from ..parks.models import Park

CSV_FILE_PATH = os.path.join(
	os.path.dirname(__file__),
	"../media/curated_parkimages/park_photos_final.csv"
)

PROJECT_ROOT = "/home/bruce/repos/bruce-bostongreenmap"
CURATE_PATH = PROJECT_ROOT+"/media/curated_parkimages"
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
	file_path = PROJECT_ROOT+ '/media/curated_parkimages/park_photos_final.csv'
	park_info = []
	count = 0
	with open(file_path) as park_csv:
		for raw in csv.reader(park_csv, delimiter=","):
			if count == 0:
				# print [(i, x) for i, x in enumerate(tuple(raw))]
				count+=1
				continue

			row = tuple(raw)
			url, park_id, is_curated = row[21], int(float(row[23])), bool(row[36])

			if is_curated: 
				park_info.append( (url, park_id ) )
			count += 1
	return park_info


@task
def download_photos():
	db = dbm.open('has_been_downloaded', 'c')
	with cd(env.code+'/../media/curated_parkimages'):
		download_count = 0
		skipped_count = 0
		for url, park_id in curated_park_info():
			try:
				if not url in db:
					picture_name = get(url)
					db[url] = picture_name
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
	db = dbm.open('has_been_downloaded', 'r')
	for url, park_id in park_info:
		if url in db[url]:
			photo_path = db[url]
			print url, photo_path


@task
def add_photos_to_db():
	print CURATE_PATH+"/has_been_downloaded"
	db = dbm.open(CURATE_PATH+'/has_been_downloaded', 'r')
	
	with cd(env.code+'/..'):
		for url, park_id in curated_park_info():
			if url in db:
				print url, park_id