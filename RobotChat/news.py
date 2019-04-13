from fake_useragent import UserAgent
import itchat
import requests
import json
import time


class News(object):
    ua = UserAgent()
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': ua.random,
    }
    url = 'http://news.cctv.com/china/data/index.json'

    def crawl(self, url):
        response = requests.get(url, headers=self.headers, timeout=20)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text

    def parser(self, count=1, _news=[]):
        _news.clear()
        content = json.loads(self.crawl(self.url))
        if content:
            for new in content.get('rollData'):
                if count > 15:
                    break
                _news.append(str(count) + '、' + new['title'])
                count += 1
            return _news

    def run(self):
        itchat.auto_login(hotReload=True)
        while True:
            others = time.strftime('%H:%M', time.localtime())
            if '8:30' == others or '14:17' == others:
                try:
                    data = self.parser()
                except Exception as error:
                    print(error)
                else:
                    if data:
                        content = '\n'.join(data)
                        itchat.send_msg(f'{time.strftime("%Y-%m-%d", time.localtime())} -- 简报|{time.strftime("%A",time.localtime())}\n\n{content}',toUserName='filehelper')
                time.sleep(60 * 60 * 6)


if __name__ == '__main__':
    briefing = News()
    briefing.run()