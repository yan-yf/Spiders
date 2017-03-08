import requests
import re
import json
from bs4 import BeautifulSoup
from urlparse import urljoin

import pymongo
from pymongo import MongoClient
import random


class Music163(object):
    def __init__(self):
        self.name = 'music163'
        self.UA = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko)Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'
        ]
        self.headers = {
            'Cookie': 'appver=1.5.0.75771',
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        self.form_data = {
            'params': 'MLdHd98OgCy6FyF1iHjKEaNx+vcI8AoHgys1NasyRuaooT/AoEByjdWFml+vUbrXUKW2PUhaTHwnsK56ZDl8kh1zoB92IGUZJPQZQ86j8XoUg0aTcdg426Odd8uUWzPa',
            'encSecKey': 'ddb05389b2484153822e55859d797146e4041cffb5076f8076e053b659a081e5e03ef7a74479ce669ff1709b09dae0fb84ebdc6050f13a761d0711f5c2f235cd6dba31a8d6003780baa49ae1574fe83ec5804b61c8e43ac5bc6205feee85ae4508fe68780e80fec7d41a1facf154b1d5bb9b91b010cd69a5728de0db47935a75'
        }
        self.artists = []
        self.song_dict = {}
        self.songs_info_list = []

    def save_info_mongodb(self, songs_info):
    	client = MongoClient('mongodb://localhost:27017/')
    	db = client['Netease']
    	table = db['netsongs']
    	table.insert(songs_info)
    	db.close()

    def get_top_comments(self, url):
        song_id = re.findall('=\d+', url)
        self.song_dict['url'] = 'http://music.163.com/#' + url
        print song_id 
        song_id = song_id[0][1:]
        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token=' % (song_id,)
        try:
            r = requests.post(url, headers=self.headers, data=self.form_data)
            try:
                hot_comments_js = json.loads(r.text)['hotComments']
                total_comments = json.loads(r.text)['total']
                self.song_dict['CommentsNum'] = str(total_comments)
                print self.song_dict
                self.save_info_mongodb(self.song_dict)
                hot_comments = ''
                for item in hot_comments_js:
                    hot_comments = hot_comments + item['user']['nickname'] + ':' + item['content'] + '\r\n'
                with open('info.txt', 'a+') as f:
                    f.write(str(total_comments) + '\r\n')
                    f.write(hot_comments.encode('gbk', 'ignore').decode('gbk').rstrip() + '\r\n')
            except:
                print 'RequestsError\n'
            finally:
            	self.save_info_mongodb(self.song_dict)
        except:
            print 'Requests' + song_id
        finally:
        	self.save_info_mongodb(self.song_dict)

    def get_songs_url(self):
        url = 'http://music.163.com'
        s = requests.session()
        for item in self.artists:
            art_url = url + item.strip()
            self.headers['User-Agent'] = self.UA[random.randint(0, len(self.UA) - 1)]
            try:
                soup = BeautifulSoup(s.get(art_url, headers=self.headers).content, 'lxml')
                song_list = soup.find('ul', {'class': 'f-hide'})
                art_name = soup.find('title')
                # art_name = art_name.text.encode('gbk', 'ignore').decode('gbk')
                # art_name = re.findall('.+ - ', art_name)
                self.songs_info_list = []
                for song in song_list.find_all('a'):
                    self.song_dict['artist'] = art_name.text[0:-8]
                    self.song_dict['song'] = song.text
                    song_url = urljoin(art_url, str(song['href']))
                    with open('info.txt', 'a+') as f:
                        f.write(art_name.text.encode('gbk', 'ignore').decode('gbk')[0:-5] + song.text.encode('gbk', 'ignore').decode('gbk').rstrip() + '\r\n')
                    self.get_top_comments(song_url)
            except:
                print 'Max retries exceeded with url' + item.strip()

    def get_all_artist(self, url):
        print url
        self.headers['User-Agent'] = self.UA[random.randint(0, len(self.UA) - 1)]
        s = requests.session()
        soup = BeautifulSoup(s.get(url, headers=self.headers).content, 'lxml')
        main = soup.find('ul', {'class': 'm-cvrlst m-cvrlst-5 f-cb'})
        for artist in main.find_all('a', {'class': 'nm nm-icn f-thide s-fc0'}):
            artist_url = str(artist['href'])
            self.artists.append(artist_url)

    def start(self):
        # ids = ['1001', '1002', '1003', '2001', '2002', '2003',
        #        '4001', '4002', '4003', '6001', '6002', '6003',
        #        '7001', '7002', '7003']
        ids = ['1001']
        urls = []
        for id in ids:
            urls.append('http://music.163.com/discover/artist/cat?id=' + id)
        for url in urls:
            print url
            self.headers['User-Agent'] = self.UA[random.randint(0, len(self.UA) - 1)]
            s = requests.session()
            soup = BeautifulSoup(s.get(url, headers=self.headers).content, 'lxml')
            az = soup.find('ul', {'class': 'n-ltlst f-cb'})
            for item in az.find_all('a'):
                item_url = urljoin(url, str(item['href']))
                self.get_all_artist(item_url)
        self.artists = set(self.artists)
        print len(self.artists)
        self.get_songs_url()

if __name__ == '__main__':
    a = Music163()
    a.start()
