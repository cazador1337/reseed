# -*- coding: utf-8 -*-
#author: cazador1337

import requests, urllib2, urllib
import json
import sys
import tempfile, os, urllib, io, gzip

user_agent = 'Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0'
headers = {'User-Agent': user_agent}

class animebytes(object):
    url = 'https://animebytes.tv/scrape.php'
    name = 'AnimeBytes'
    supported_categories = {'anime':'anime', 'music':'music'}
    username = '<username>'
    passkey = '<passkey>'    

    def search(self, anime, cat='anime'):

        print("Searching for: "+anime['anime_title'])
        flag = int(input("Use Filter (0/1=N/Y): "))
        data = self.retrieve_url(self.url+'?torrent_pass=%s&username=%s&type=%s&searchstr=%s' % (self.passkey, self.username, cat, anime['anime_title']))
        jd = json.loads(self.fixdata(data))
        res = []
        try:
            for group in jd['Groups']:            
                for torrent in group['Torrents']:
                    if (self.filter(torrent, anime, flag)):
                        res.append(self.createRes(group, torrent))
        except:
            n = input("Try Tiping a new name: ")
            anime['anime_title'] = n
            return self.search(anime)
        return res
    
    def fixdata(self, data):
        #f = open('log.txt', 'w', encoding='utf-8')
        #f.write(data)
        res = ""
        for line in data.splitlines():
            if line.find('DescriptionHTML') == -1:
                res += line
        return res
    
    def retrieve_url(self, url):
        return requests.get(url, headers = headers).text

    def download_torrent(self, info, dir, name):
        """ Download file at url and write it to a file, return the path to the file and the url """        
        file, path = tempfile.mkstemp(prefix=name.replace(":", "")+"-",suffix='.torrent', dir=dir)
        file = os.fdopen(file, "wb")
        # Download url
        dat = requests.get(info, headers = headers)
        # Write it to a file
        file.write(dat.content)
        file.flush()
        file.close()
        # return file path
        return path

    def createRes(self, group, torrent):
        res = {'SeriesName': group['SeriesName'],
        'Synonymns': group['Synonymns'],
        'FullName': group['FullName'],
        'Property': torrent['Property'],
        'Link': torrent['Link'],
        'Size': torrent['Size'],
        'FileCount': torrent['FileCount']}

        return res
    
    def filter(self, torrent, anime, flag):
        bol = flag == 0
        try:
            bol = bol or torrent['Property'].find(anime['release_group']) != -1
        except:
            pass

        try:   
            bol = bol or torrent['Property'].find(anime['video_resolution']) != -1
        except:
            pass

        try:   
            bol = bol or torrent['Property'].find(anime['source']) != -1
        except:
            pass
        return bol