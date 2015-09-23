from __future__ import unicode_literals
import youtube_dl
import sys, os, shutil

# =====================================================================================================
# Confirmation Prompt: @ http://code.activestate.com/recipes/541096-prompt-the-user-for-confirmation/
# =====================================================================================================

def confirm(prompt=None, resp=True):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """
    
    if prompt is None:
        prompt = 'Download Extra?'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print 'please enter y or n.'
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False


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
			print ("%s (%s)" % (search_result["snippet"]["title"], search_result["snippet"]["channelTitle"])).encode('utf-8')
			if confirm():
				videos.append(("%s" % (search_result["id"]["videoId"])).encode('utf-8'))
				# videos.append(("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"])).encode('utf-8'))

	# print "Videos:\n", "\n".join(videos), "\n"
	return videos


# ===============================================================
# Main Script
# ===============================================================

if len(sys.argv) != 3:
	print "Usage: sudo python plextras.py \"[film name]\" [file/folder route]" # Add max results (?)
	exit()

film_name = sys.argv[1]
file_folder = sys.argv[2]

# Making a parent folder for the file
if os.path.isfile(file_folder):
	file_folder_new = os.path.splitext(file_folder)[0]
	os.mkdir(file_folder_new, 0755)
	shutil.move(file_folder, file_folder_new + "/" + os.path.basename(file_folder))
	file_folder = file_folder_new

# Plex folder scheme
if not os.path.exists(file_folder + "/Behind The Scenes"):
	os.mkdir(file_folder + "/Behind The Scenes", 0755)
if not os.path.exists(file_folder + "/Interviews"):
	os.mkdir(file_folder + "/Interviews", 0755)
if not os.path.exists(file_folder + "/Scenes"):
	os.mkdir(file_folder + "/Scenes", 0755)
if not os.path.exists(file_folder + "/Trailers"):
	os.mkdir(file_folder + "/Trailers", 0755)

def youtube_download(path, search, max_results):
	# Youtube Trailer Search
	try:
		videos = youtube_search(search, max_results)
	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

	# Download using youtube-dl library

	ydl_opts = {
		'outtmpl':path +'/%(title)s.%(ext)s'
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download(videos)

youtube_download(file_folder + '/Behind The Scenes', film_name + "behind the scenes", 3)
youtube_download(file_folder + '/Behind The Scenes', film_name + "breakdown", 2)
youtube_download(file_folder + '/Interviews', film_name + "interview", 4)
youtube_download(file_folder + '/Scenes', film_name + "scene", 2)
youtube_download(file_folder + '/Scenes', film_name + "anatomy of a scene", 1)
youtube_download(file_folder + '/Trailers', film_name + "trailer", 1)

