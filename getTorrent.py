#author: cazador1337
import anitopy.anitopy as ani
import fileman, abapi, sys, os
from torrent import decode

if __name__ == "__main__":
    fman = fileman.fileman()    
    dir = sys.argv[1]
    files, path = fman.getFiles(dir)
    ab = abapi.animebytes()
    
    print("Choose a file for searching: ")
    i = 0
    for f in files:
        print i, f
        i += 1
    pos = input("Number: ")

    links = ab.search(ani.parse(files[pos]))
    print("Found: %i Torrent(s)"%(len(links)))
    if (len(links)!=1):
        print("Searching inside .torrent for your files!!")
        torrents = []
        flag = False
        for link in links:
            torrent = ab.download_torrent(link['Link'], dir, link['SeriesName'])
            raw = open(torrent, "rb").read()
            data = decode(raw)            
            try:
                for name in data["info"]["files"]:
                    if(name['path'][0].find(files[pos]) != -1):
                        os.rename(torrent, torrent.replace(torrent[torrent.rfind("\\"): len(torrent)], "\\"+data['info']['name']+".torrent"))
                        flag = True
                        break
            except:
                if(data['info']['name'].find(files[pos]) != -1):
                    os.rename(torrent, torrent.replace(torrent[torrent.rfind("\\"): len(torrent)], "\\"+data['info']['name']+".torrent"))
                    flag = True
            if(flag):
                print("Found!!")
                break
            else:
                os.remove(torrent)

        
    else:
        path = ab.download_torrent(links[0]['Link'], dir, links[0]['SeriesName'])
        raw = open(path, "rb").read()
        data = decode(raw)
        os.rename(path, path.replace(path[path.rfind("\\"): len(path)], "\\"+data['info']['name']+".torrent"))        
        print("Finished!")