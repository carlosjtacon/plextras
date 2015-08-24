import sys, os, shutil

if len(sys.argv) != 3:
	print "Usage: sudo python plextras.py \"[film name]\" [file/folder route]"
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
os.mkdir(file_folder + "/Behind The Scenes", 0755)
os.mkdir(file_folder + "/Deleted Scenes", 0755)
os.mkdir(file_folder + "/Interviews", 0755)
os.mkdir(file_folder + "/Scenes", 0755)
os.mkdir(file_folder + "/Trailers", 0755)