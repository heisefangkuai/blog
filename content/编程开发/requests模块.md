# requests 模块

## 1参数

1. url
2. headers
3. cookies
4. params
5. data，传请求体

    ```python
    requests.post(
        ...,
        data={'user':'alex','pwd':'123'}
    )

    GET /index http1.1\r\nhost:c1.com\r\n\r\nuser=alex&pwd=123
    ```

6. json，传请求体

    ```python
    requests.post(
        ...,
        json={'user':'alex','pwd':'123'}
    )

    GET /index http1.1\r\nhost:c1.com\r\nContent-Type:application/json\r\n\r\n{"user":"alex","pwd":123}
    ```

7. 代理 proxies

    ```python
    # 无验证
        proxie_dict = {
            "http": "61.172.249.96:80",
            "https": "http://61.185.219.126:3128",
        }
        ret = requests.get("https://www.proxy360.cn/Proxy", proxies=proxie_dict)

    # 验证代理
        from requests.auth import HTTPProxyAuth

        proxyDict = {
            'http': '77.75.105.165',
            'https': '77.75.106.165'
        }
        auth = HTTPProxyAuth('用户名', '密码')

        r = requests.get("http://www.google.com",data={'xxx':'ffff'} proxies=proxyDict, auth=auth)
        print(r.text)
    ```

8. 文件上传 files

    ```python
    # 发送文件
        file_dict = {
            'f1': open('xxxx.log', 'rb')
        }
        requests.request(
            method='POST',
            url='http://127.0.0.1:8000/test/',
            files=file_dict
        )
    ```

9. 认证 auth

    ```python
    内部：
        用户名和密码，用户和密码加密，放在请求头中传给后台。
        "用户:密码"
        base64("用户:密码")
        "Basic base64("用户|密码")"
        请求头：
            Authorization： "basic base64("用户|密码")"

    from requests.auth import HTTPBasicAuth, HTTPDigestAuth

    ret = requests.get('https://api.github.com/user', auth=HTTPBasicAuth('wupeiqi', 'sdfasdfasdf'))
    print(ret.text)
    ```

10. 超时 timeout

    ```python
    ret = requests.get('http://google.com/', timeout=1)
    print(ret)
    # timeout 第一个值是请求时间，第二个是返回时间
    ret = requests.get('http://google.com/', timeout=(5, 1))
    print(ret)
    ```

11. 允许重定向  allow_redirects

    ```python
    ret = requests.get('http://127.0.0.1:8000/test/', allow_redirects=False)
    print(ret.text)
    ```

12. 大文件下载 stream

    ```python
    from contextlib import closing
    with closing(requests.get('http://httpbin.org/get', stream=True)) as r1:
    # 在此处理响应。
    for i in r1.iter_content():
        print(i)
    ```

13. 证书 cert

    ```python
    百度、腾讯 => 不用携带证书（系统帮你做了）
    自定义证书
        requests.get('http://127.0.0.1:8000/test/', cert="xxxx/xxx/xxx.pem")
        requests.get('http://127.0.0.1:8000/test/', cert=("xxxx/xxx/xxx.pem","xxx.xxx.xx.key"))
    ```


14. 确认 verify =False ,类似于yum安装的 -y 参数
