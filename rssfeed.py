#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom import minidom
import urllib2
import urlparse
import podepisode


# returns an array with all episodes in pod
def getPodEpisodes( url ):
	
	result = []

	# read url
	rsp = None
	rssData = None
	try:
		rsp = urllib2.urlopen( url )
		rssData = rsp.read()
	except:
		return None
	
	# parse xml
	xmlDoc = minidom.parseString( rssData )
	for node in xmlDoc.getElementsByTagName( "item" ):
		episode = _getPodEpisode( node )
		if episode != None:
			result.append( episode )
	return result

########################################################################

# private functions

def _getPodEpisodeContentUrl( enclosureElement ):
	if enclosureElement.hasAttribute( "url" ) == False:
		return None
	url = enclosureElement.getAttribute( "url" ).encode( "utf-8" )
	splitUrl = urlparse.urlsplit( url )
	protStr = splitUrl[ 0 ] + "://"
	result = protStr + urllib2.quote( url[ len(protStr): ] )
	return result

def _getPodEpisodeContentType( enclosureElement ):
	if enclosureElement.hasAttribute( "type" ) == False:
		return None
	result = enclosureElement.getAttribute( "type" )
	return result

def _getPodEpisodeTitle( titleElement ):
	result = None
	for child in titleElement.childNodes:
		if child.nodeType == minidom.Node.TEXT_NODE:
			result = child.data
		elif child.nodeType == minidom.Node.CDATA_SECTION_NODE:
			result = child.data
	result = result.strip()
	return result

def _getPodEpisodePublishedTime( publishedElement ):
	result = None
	for child in publishedElement.childNodes:
		if child.nodeType == minidom.Node.TEXT_NODE:
			result = child.data
	return result

def _getPodEpisode( rssItem ):

	url = None
	mimeType = None
	title = None
	publishedTime = None

	result = None

	for element in rssItem.childNodes:

		if element.nodeType == minidom.Node.ELEMENT_NODE: 
			if element.tagName == "enclosure":
				url = _getPodEpisodeContentUrl( element )
				mimeType = _getPodEpisodeContentType( element )
			if element.tagName == "title":
				title = _getPodEpisodeTitle( element )
			if element.tagName == "pubDate":
				publishedTime = _getPodEpisodePublishedTime( element )

	if url != None:
		result = podepisode.Episode( title = title, url = url, type = mimeType, publishedTime = publishedTime )
	return result
