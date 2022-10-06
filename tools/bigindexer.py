import os, sys
from glob import glob

#dirlist = os.listdir('/afs/desy.de/user/b/beinsam/www/DisappearingTracks/Validation/')
#print dirlist

'''
python /afs/desy.de/user/b/beinsam/www/dir_indexer.py /afs/desy.de/user/b/beinsam/www/FastSim/Nano/27June2022 -r -t /afs/desy.de/user/b/beinsam/www/templates/default.html
python tools/bigindexer.py /afs/desy.de/user/b/beinsam/www/FastSim/Nano/27June2022/
'''

dirlist = []

def listdirs(rootdir):
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            dirlist.append(d)
            listdirs(d)


try: rootdir = sys.argv[1]
except: rootdir = '/afs/desy.de/user/b/beinsam/www/FastSim/Nano'
#rootdir = '/afs/desy.de/user/b/beinsam/www/pMSSMScanCompare/'
listdirs(rootdir)
#print dirlist


for direc in dirlist:
	subs = glob(direc+'/*')
	print "direc+'/*'", direc+'/*', subs[-1]
	if len(subs)>0 and ('.png' in subs[-1] or '.png' in subs[0]):
		command = 'python tools/whiphtml.py "'+direc+'/*.png"'
		print command
		os.system(command)