
import requests
import hashlib
# nohup python -u test.py > out.log 2>&1 & linux后台运行
def urlMd5(urls = 'http://66.42.42.140:888/favicon.ico'):
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169",'Upgrade-Insecure-Requests':'1','Connection':'keep-alive','Cache-Control':'max-age=0',
    'Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'zh-CN,zh;q=0.8',
    "Referer": "https://www.google.com.hk/webhp?hl=zh-CN&sourceid=cnhp&gws_rd=ssl"}
    r = requests.get(url=urls, headers=headers, timeout=20,verify=False,)
    r.encoding = 'utf-8'
    if r.status_code==200:
        url_content = r.content
    m = hashlib.md5()
    m.update(url_content)
    md5 = m.hexdigest()
    print(md5)

def test(url):
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169",'Upgrade-Insecure-Requests':'1','Connection':'keep-alive','Cache-Control':'max-age=0',
    'Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'zh-CN,zh;q=0.8',
    "Referer": "https://www.google.com.hk/webhp?hl=zh-CN&sourceid=cnhp&gws_rd=ssl"}
    while True:
        url = "http://"+url+":888/pma"
        print(url)
        try:
            re = requests.get(url,headers=headers, timeout=5, verify=False)
        except:
            break
        if re.status_code == 200 and "phpMyAdmin" in re.text:
            print(url)
            f=open('f.txt','a')
            f.write("[+]存在宝塔phpmyadmin未授权漏洞: "+url)
            f.close()
            print("[+]存在宝塔phpmyadmin未授权漏洞: "+url)
        else:
            print(1)
            break

def main():
    a = 1
    b = 1
    c = 1
    d = 1
    for a in range(1,256):
        for b in range(1,256):
            for c in range(1,256):
                for d in range(1,256):
                    ips = str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d)
                    print(ips)
                    test(ips)

if __name__ == '__main__':
    main()
