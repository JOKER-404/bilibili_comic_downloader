import json
import os
import requests
import re

cookie="" # 设置cookie值，直接粘贴字符串即可

def transCookie(cookie):
    cookie = cookie.split(';')
    cdict = dict()
    for c in cookie:
        c = c.split('=')
        cdict[c[0]] = c[1]
    return cdict


cookie = transCookie(cookie)


def getComicDetail(cid):
    url = "https://manga.bilibili.com/twirp/comic.v1.Comic/ComicDetail?device=pc&platform=web"
    postdict = {"comic_id": cid}
    res = requests.post(url, data=postdict, cookies=cookie)
    print(json.loads(res.text)['data']['ep_list'])
    eps = json.loads(res.text)['data']['ep_list']
    downloadable = dict()
    downloadinable = dict()
    for ep in eps:
        if ep["is_locked"] and not ep['is_in_free']:
            downloadinable[ep['title']] = ep['id']
        else:
            downloadable[ep['title']] = ep['id']
    print(downloadable)
    print()
    print(downloadinable)
    return downloadable


def getEpImageIndex(epid):
    url = "https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web"
    postdata = {"ep_id": epid}
    res = requests.post(url, data=postdata, cookies=cookie)
    index = json.loads(res.text)
    print(index['data']['images'])
    return index['data']['images']


def getImageToken(path):
    url = "https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web"
    path += '@1100w.jpg'

    postdict = {"urls": f"[\"{path}\"]"}
    res = requests.post(url, data=postdict, cookies=cookie)
    token = json.loads(res.text)['data'][0]
    print(token)
    return token['url'] + "?token=" + token['token']


def downloadImage(token, page):
    file = open(f"{page}.jpg", 'wb')
    res = requests.get(token)
    file.write(res.content)



a = getEpImageIndex(252052)

print(a[0]['path'])

def auto(cid, cname):
    os.makedirs(cname)
    os.chdir(f'.\\{cname}')
    eps = getComicDetail(cid)
    for ep in eps.keys():
        os.makedirs(ep)
        os.chdir(f'.\\{ep}')
        index = getEpImageIndex(eps[ep])
        page = 1
        for i in index:
            token = getImageToken(i['path'])
            downloadImage(token, page)
            page += 1
        os.chdir('..')


auto(25479, 'JOJO7') #第一个参数为漫画id，第二个为目录名称
