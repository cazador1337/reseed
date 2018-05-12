#author: cazador1337
import fnmatch
import os
import abapi

class fileman(object):
    def getFiles(self, dir):
        fullpath = []
        name = []
        for root, dirnames, filenames in os.walk(dir):
            for filename in filenames:                
                if filename.endswith(('.mkv', '.avi', '.ogm', '.mp4')):
                    fullpath.append(os.path.join(root, filename))
                    name.append(filename)
        return name, fullpath