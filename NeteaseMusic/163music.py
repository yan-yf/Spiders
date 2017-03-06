import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random


class Music163(object):
    # headers['User-Agent'] = UA[random.randint(0, len(UA) - 1)]
    def __init__(self):
        self.name = 'music163'
        self.UA = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko)\
             Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) \
            AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; \
            .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'
        ]
        self.headers = {
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        self.artists = []
        '''/artist?id=6452'''
        '''http://music.163.com/#/artist?id=6452'''

    def get_top_comments(self, url):
        pass

    def get_songs_url(self):
        url = 'http://music.163.com'
        for item in self.artists:
            art_url = url + item
            self.headers['User-Agent'] = self.UA[random.randint(0, len(self.UA) - 1)]
            s = requests.session()
            s.keep_alive = False
            soup = BeautifulSoup(s.get(art_url, headers=self.headers).content, 'lxml')
            song_list = soup.find('ul', {'class': 'f-hide'})
            for song in song_list.find_all('a'):
                song_url = urljoin(art_url, str(song['href']))
                self.get_top_comments(song_url)

    def get_all_artist(self, url):
        print(url)
        self.headers['User-Agent'] = self.UA[random.randint(0, len(self.UA) - 1)]
        s = requests.session()
        s.keep_alive = False
        soup = BeautifulSoup(s.get(url, headers=self.headers).content, 'lxml')
        main = soup.find('ul', {'class': 'm-cvrlst m-cvrlst-5 f-cb'})
        for artist in main.find_all('a', {'class': 'nm nm-icn f-thide s-fc0'}):
            artist_url = str(artist['href'])
            self.artists.append(artist_url)

    # 爬取歌手主页
    def start(self):
        ids = ['1001', '1002', '1003', '2001', '2002', '2003',
               '4001', '4002', '4003', '6001', '6002', '6003',
               '7001', '7002', '7003']
        # ids = ['1001']
        urls = []
        for id in ids:
            urls.append(f'http://music.163.com/discover/artist/cat?id={id}')
        for url in urls:
            print(url)
            self.headers['User-Agent'] = self.UA[random.randint(0, len(self.UA) - 1)]
            s = requests.session()
            s.keep_alive = False
            soup = BeautifulSoup(s.get(url, headers=self.headers).content, 'lxml')
            az = soup.find('ul', {'class': 'n-ltlst f-cb'})
            for item in az.find_all('a'):
                item_url = urljoin(url, str(item['href']))
                self.get_all_artist(item_url)
        self.artists = set(self.artists)
        print(len(self.artists))
        self.get_songs_url()

if __name__ == '__main__':
    a = Music163()
    a.start()
