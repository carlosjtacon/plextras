# ===============================================================
# Youtube Stuff
# ===============================================================

from apiclient.discovery import build
from apiclient.errors import HttpError

DEVELOPER_KEY = "REPLACE_ME"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(query, max_results):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

	# Call the search.list method to retrieve results matching the specified query term.
	search_response = youtube.search().list(
		q=query,
		part="id,snippet",
		maxResults=max_results
	).execute()

	videos = []
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
		  videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))

	print "Videos:\n", "\n".join(videos), "\n"


# ===============================================================
# Main Script
# ===============================================================

import sys, os, shutil

if len(sys.argv) != 3:
	print "Usage: sudo python plextras.py \"[film name]\" [file/folder route]" # Add max results (?)
	exit()

film_name = sys.argv[1]
file_folder = sys.argv[2]

# Making a parent folder for the file
if os.path.isfile(file_folder):
	file_folder_new = file_folder + "_dir"
	os.mkdir(file_folder_new, 0755)
	shutil.move(file_folder, file_folder_new + "/" + os.path.basename(file_folder))
	os.rename(file_folder_new, file_folder)

# Plex folder scheme
if not os.path.exists(file_folder + "/Behind The Scenes"):
	os.mkdir(file_folder + "/Behind The Scenes", 0755)
if not os.path.exists(file_folder + "/Deleted Scenes"):
	os.mkdir(file_folder + "/Deleted Scenes", 0755)
if not os.path.exists(file_folder + "/Interviews"):
	os.mkdir(file_folder + "/Interviews", 0755)
if not os.path.exists(file_folder + "/Scenes"):
	os.mkdir(file_folder + "/Scenes", 0755)
if not os.path.exists(file_folder + "/Trailers"):
	os.mkdir(file_folder + "/Trailers", 0755)

# Youtube Trailer Search
try:
	youtube_search(film_name + "trailer", 1)
except HttpError, e:
	print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
