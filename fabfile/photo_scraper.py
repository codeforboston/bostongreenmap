from fabric.api import cd, run, put, env, task
from fabric.operations import sudo
import dbm
import csv
import os

def get(url):
	run("wget '{}'".format(url))
	split_name = url.split('/')
	picture_name = split_name[len(split_name)-1]
	return picture_name

def curated_park_info():
	file_path = os.path.join(
		os.path.dirname(__file__),
		'../media/curated_parkimages/park_photos_final.csv'
	)
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
	for url in ['https://farm4.staticflickr.com/3709/14292507832_6dcee9cfca_b.jpg',
					'https://farm8.staticflickr.com/7119/6942731872_7a8849e263_b.jpg']:
		print "filesystem name for %s: %s" % (url, db[url])
	db.close()
