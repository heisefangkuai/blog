"""
信息收集之子域名爬取工具
"""

import requests,random,sys,itertools,os
from lxml import etree

class PaChong:

    url = ''
    user_agent = ''

    def __init__(self, url, *args):

        # 获取请求user_agent
        file = open("user_agents.txt","r")
        self.user_agent = file.readlines()

        self.url = url

        self.mains(self.url)
    
    def file(self, filename, datas):
        # 去重
        data = list(set(datas))

        # 判断文件是否存在,并保存txt
        path = os.getcwd() + '\\txt'
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path) 
        fp = open(".\\txt\\"+ filename +".txt",'w+')
        for i in data:
            fp.write(i+'\r')
        fp.close()


    def zzzj(self, urls):
        """
        站长之家子域名爬取
        http://tool.chinaz.com/subdomain/?domain=https://www.pingan.com/
        """

        url = "http://tool.chinaz.com/subdomain/?domain=" + urls
        UA = random.choice(self.user_agent).rstrip() 
        headers = {"User-Agent": UA}

        # 获取url页数
        r = requests.get(url=url, headers=headers, timeout=5,verify=False)
        r.encoding = 'utf-8'
        selector = etree.HTML(r.text)
        try:
            yeshu = selector.xpath("//span[@class='col-gray02'][1]/text()")[0][1:-4]
        except requests.exceptions.ConnectionError:
            print('++++++')
            yeshu = selector.xpath("//span[@class='col-gray02'][1]/text()")[0][1:-4]
        except requests.exceptions.ReadTimeout:
            print('----')
            yeshu = selector.xpath("//span[@class='col-gray02'][1]/text()")[0][1:-4]
        
        
        # 获取url
        urlList = []
        for a in range(1,int(yeshu) + 1):
            url1 = url + '&page=' + str(a)
            print(url1)
            r = requests.get(url=url1, headers=headers, timeout=50,verify=False)
            r.encoding = 'utf-8'
            selector = etree.HTML(r.text)
            try:
                urlList.append(selector.xpath("//div[@class='w23-0 subdomain']/a/text()"))
            except requests.exceptions.ConnectionError:
                print('++++++')
                urlList.append(selector.xpath("//div[@class='w23-0 subdomain']/a/text()"))
            except requests.exceptions.ReadTimeout:
                print('----')
                urlList.append(selector.xpath("//div[@class='w23-0 subdomain']/a/text()"))
            
        out = list(itertools.chain.from_iterable(urlList))  # 多层数组转单层数组
        self.file(filename = '站长之家', datas = out)
        

    def crtSh(self,urls):
        """
        https://crt.sh/子域名爬取
        https://crt.sh/?q=pingan.com
        """

        url = 'https://crt.sh/?q=' +  urls.split('.',1)[-1][:-1]
        print(url)
        UA = random.choice(self.user_agent).rstrip() 
        headers = {"User-Agent": UA,
        'Connection': 'close',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'}
        requests.packages.urllib3.disable_warnings()
        try:
            r = requests.get(url=url, headers=headers, timeout=50,verify=False)
        except requests.exceptions.ConnectionError:
            print('++++++')
            r = requests.get(url=url, headers=headers, timeout=50,verify=False)
        except requests.exceptions.ReadTimeout:
            print('----')
            r = requests.get(url=url, headers=headers, timeout=50,verify=False)
        r.encoding = 'utf-8'
        selector = etree.HTML(r.text)
        out = selector.xpath("//tr/td[5]/text()")
        self.file(filename = 'crtSh', datas = out)

    def mains(self,url):
        # self.zzzj(url)
        # self.crtSh(url)


x = PaChong(sys.argv[1])



