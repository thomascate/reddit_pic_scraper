#!/usr/bin/env python
import praw
from imgurpython import ImgurClient
import imgurcreds
import re
import os
import urllib2
from time import sleep
from pprint import pprint

#reddit api setup
r = praw.Reddit(user_agent='toms scraperbot thomascate@gmail.com')
submissions = r.get_subreddit('wallpaperdump').get_hot(limit=50)

#imgur api setup
#creds are in imgurcreds.py
imgurclient = ImgurClient(imgurcreds.clientID, imgurcreds.clientSecret)

directUrls = { 'directLinks' : []}
directUrls['directLinks'] = list()
imgurAlbums = []
imgurImages = []

def get_url_type(url):
  imgurMatch        = re.match( r'^(http|https)\:\/\/imgur\.com', url, re.M|re.I)
  imgurAlbumMatch   = re.match( r'^(http|https)\:\/\/imgur\.com\/(a|gallery)\/', url, re.M|re.I)
  #imgurGalleryMatch = re.match( r'^(http|https)\:\/\/imgur\.com\/gallery\/', url, re.M|re.I)
  directLink        = re.match( r'.*\.jpg', url, re.M|re.I)

  if directLink:
  	urlType = "directLink"
  elif imgurAlbumMatch:
    urlType = "imgurAlbum"
  #elif imgurGalleryMatch:
    #urlType = "imgurGallery"
  elif imgurMatch:
  	urlType = "imgur"
  else:
  	urlType = "unknown"

  return urlType

def get_imgur_album_id(url):
  return url.rsplit("/")[4][0:5]

def get_imgur_ids_from_url(url):
  #these posts often contain lists of ids
  idPath = url.rsplit("/")[3]
  ids = []

  if "," in idPath:
    for imgurID in idPath.rsplit(","):
      ids.append(imgurID[0:5])

  else:
    ids.append(idPath[0:5])

  return ids

def get_imgur_ids_from_album(album):
  albumImages = imgurclient.get_album_images(album)
  return albumImages

def get_imgur_ids_from_gallery(gallery):
  return True

for post in submissions:
  sleep(1)
  #make sure it's a link
  if not post.is_self:

    if get_url_type(post.url) == "directLink":
      directUrls['directLinks'].append(post.url)

    elif get_url_type(post.url) == "imgurAlbum":
      albumID    = get_imgur_album_id(post.url)
      if not imgurclient.get_album(albumID).title:
        albumTitle = albumID
      else:
        albumTitle = imgurclient.get_album(albumID).title.replace("/","|")
      print "scraping " + albumTitle
      imgurIDs   = get_imgur_ids_from_album(albumID)
      directUrls[albumTitle] = list()

      for imgurID in imgurIDs:
        directUrls[albumTitle].append( imgurID.link )
       
    elif get_url_type(post.url) == "imgurGallery":
      print post.url

    elif get_url_type(post.url)  == "imgur":
      imgurImages = imgurImages + get_imgur_ids_from_url(post.url)


for album in imgurAlbums:
  print album

for key in directUrls:
  print key
  print len(directUrls[key])
  if not os.path.exists(key):
    os.mkdir(key)
  for url in directUrls[key]:
    filename = key + '/' +  url.rsplit("/")[-1]
    f = open(filename,'wb')
    f.write(urllib2.urlopen(url).read())
    f.close()
#pprint(directUrls)
#for image in imgurImages:
#  print image


#!/usr/bin/env python
import praw
from imgurpython import ImgurClient
import imgurcreds
import re
import os
import urllib2
from pprint import pprint

#reddit api setup
r = praw.Reddit(user_agent='toms scraperbot thomascate@gmail.com')
submissions = r.get_subreddit('wallpaperdump').get_hot(limit=5)

#imgur api setup
#creds are in imgurcreds.py
imgurclient = ImgurClient(imgurcreds.clientID, imgurcreds.clientSecret)

directUrls = { 'directLinks' : []}
directUrls['directLinks'] = list()
imgurAlbums = []
imgurImages = []

def get_url_type(url):
  imgurMatch        = re.match( r'^(http|https)\:\/\/imgur\.com', url, re.M|re.I)
  imgurAlbumMatch   = re.match( r'^(http|https)\:\/\/imgur\.com\/(a|gallery)\/', url, re.M|re.I)
  #imgurGalleryMatch = re.match( r'^(http|https)\:\/\/imgur\.com\/gallery\/', url, re.M|re.I)
  directLink        = re.match( r'.*\.jpg', url, re.M|re.I)

  if directLink:
  	urlType = "directLink"
  elif imgurAlbumMatch:
    urlType = "imgurAlbum"
  #elif imgurGalleryMatch:
    #urlType = "imgurGallery"
  elif imgurMatch:
  	urlType = "imgur"
  else:
  	urlType = "unknown"

  return urlType

def get_imgur_album_id(url):
  return url.rsplit("/")[4][0:5]

def get_imgur_ids_from_url(url):
  #these posts often contain lists of ids
  idPath = url.rsplit("/")[3]
  ids = []

  if "," in idPath:
    for imgurID in idPath.rsplit(","):
      ids.append(imgurID[0:5])

  else:
    ids.append(idPath[0:5])

  return ids

def get_imgur_ids_from_album(album):
  albumImages = imgurclient.get_album_images(album)
  return albumImages

def get_imgur_ids_from_gallery(gallery):
  return True

for post in submissions:

  #make sure it's a link
  if not post.is_self:

    if get_url_type(post.url) == "directLink":
      directUrls['directLinks'].append(post.url)

    elif get_url_type(post.url) == "imgurAlbum":
      albumID    = get_imgur_album_id(post.url)
      if not imgurclient.get_album(albumID).title:
        albumTitle = 'directLinks'
      else:
        albumTitle = imgurclient.get_album(albumID).title.replace("/","|")
      imgurIDs   = get_imgur_ids_from_album(albumID)
      directUrls[albumTitle] = list()

      for imgurID in imgurIDs:
        directUrls[albumTitle].append( imgurID.link )
       
    elif get_url_type(post.url) == "imgurGallery":
      print post.url

    elif get_url_type(post.url)  == "imgur":
      imgurImages = imgurImages + get_imgur_ids_from_url(post.url)


for album in imgurAlbums:
  print album

for key in directUrls:
  print key
  print len(directUrls[key])
  if not os.path.exists(key):
    os.mkdir(key)
  for url in directUrls[key]:
    filename = key + '/' +  url.rsplit("/")[-1]
    f = open(filename,'wb')
    f.write(urllib2.urlopen(url).read())
    f.close()
#pprint(directUrls)
#for image in imgurImages:
#  print image



