from ConfigParser import ConfigParser
from collections import namedtuple
import os

# named tuple that holds config
Config = namedtuple( "Config", "podlist history downloadPath separateDirs updateId3" )

def getConfig( configFile ):

	# defaults
	podlist = "~/.podagg/podlist"
	history = "~/.podagg/history"
	downloadPath = "~/podcasts/"
	separateDirs = True
	updateId3 = True
	
	cfgFile = ConfigParser()
	cfgFile.read( configFile )
	if cfgFile.has_option( "files", "podlist" ):
		podlist = cfgFile.get( "files", "podlist" )
	if cfgFile.has_option( "files", "history" ):
		history = cfgFile.get( "files", "history" )
	if cfgFile.has_option( "paths", "download_dir" ):
		downloadPath = cfgFile.get( "paths", "download_dir" )
	if cfgFile.has_option( "paths", "separate_dirs" ):
		separateDirs = cfgFile.getboolean( "paths", "separate_dirs" )
	if cfgFile.has_option( "misc", "update_id3" ):
		updateId3 = cfgFile.getboolean( "misc", "update_id3" )

	# expand path to support ~	
	podlist = os.path.expanduser( podlist )
	history = os.path.expanduser( history )
	downloadPath = os.path.expanduser( downloadPath )

	result = Config( podlist = podlist, history = history, downloadPath = downloadPath, separateDirs = separateDirs, updateId3 = updateId3 )

	return result