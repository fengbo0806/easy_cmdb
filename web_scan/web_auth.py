import requests

# Sample Basic Auth Url with login values as username and password

url2 = "http:///cgi-bin/status.cgi"
user2 = ""
passwd2 = ""

'''test login to powersmart'''


class loginEncoder:
    def __init__(self, ipadd, username, passwd, targetType):
        self.ipadd = ipadd
        self.username = username
        self.passwd = passwd
        self.target = targetType
        self.loginURL = None
        self.getInfoURL = None

    def powersmart(self):
        orderId = 0
        self.getInfoURL = 'http://%s/encoder_status_new.cgi' % (self.ipadd,)
        self.getDeatilURL = 'http://%s/html/encoder/setup3.html?referer=1&id=%d' % (self.ipadd, orderId)

        req = requests.session()
        con = req.get(self.getInfoURL, headers={"If-Modified-Since": "0",
                                               'Host': '%s' % (self.ipadd),
                                               'Referer': 'http://%s/html/encoder/maininfo2.html?referer=1' % (
                                                   self.ipadd)}, cookies={'logined': 'gg'}).content
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(con, "html.parser", )
        # print(soup.encoder.id.get_text())
        result = dict()
        result[soup.encoder.id.get_text()] = {'id': soup.encoder.id.get_text(),
                                              'status': soup.encoder.status.get_text(),
                                              'name': soup.encoder.find('name').get_text(),
                                              'width': soup.encoder.width.get_text(),
                                              'height': soup.encoder.height.get_text(),
                                              'outbandwidth': soup.encoder.outbandwidth.get_text(), }

        for sibling in soup.encoder.next_siblings:
            '''
            <class 'bs4.element.Tag'>
            <class 'bs4.element.NavigableString'>
            '''
            if len(sibling) > 1:
                result[sibling.id.get_text()] = {'id': sibling.id.get_text(),
                                                 'status': sibling.status.get_text(),
                                                 'name': sibling.find('name').get_text(),
                                                 'width': sibling.width.get_text(),
                                                 'height': sibling.height.get_text(),
                                                 'outbandwidth': sibling.outbandwidth.get_text(), }
        '''
        {'0': [{'id': '0', 'status': '-1', 'name': '银川公共-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}], '1': [{'id': '1', 'status': '-1', 'name': '杭州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}], '2': [{'id': '2', 'status': '0', 'name': '广州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}], '3': [{'id': '3', 'status': '0', 'name': '福州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}], '4': [{'id': '4', 'status': '0', 'name': '郑州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}], '5': [{'id': '5', 'status': '0', 'name': '兰州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}]}
        '''
        for key in result.keys():
            import random
            # print(round(random.random(), 15))
            orderId = key
            'get_device.cgi?rnd=" + Math.random()'
            RequestURL = 'http://%s/get_encoder_1109.cgi?rnd=%f'%(self.ipadd,round(random.random(), 15))
            con = req.get(RequestURL, headers={"If-Modified-Since": "0",
                                                    'Host': '%s' % (self.ipadd),
                                                    'Referer': self.getDeatilURL
                                                   }, cookies={'logined': 'gg'}).content
            soup = BeautifulSoup(con, "html.parser", )
            import re
            for line in soup.prettify():
                if not line:
                    break
                re.split()
        return result
        # u',\n'
        # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
        # u' and\n'
        # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
        # u'; and they lived at the bottom of a well.'
        # None
        # print(content)
        # content = soup.find_all('encoder') #找到soup中所有的td标签，得到一个list
        # print(content)
        # regis_info = [] #新建一个空的列表，便于后续往里面添加数据
        # result={}
        # print(content.id)
        # for i in range(0, len(content)): #对content列表中的每一个元素进行遍历
        #     data = content[i].get_text() # 将每一个元素中包含的文本提取出来
        #     regis_info.append(data) # 追加到regis_info列表中
        #     i = i + 1 # 继续对content中的下一个元素进行处理
        # print(regis_info) # 将最终regis_info进行打印

        # print(soup.prettify())
        # print(soup.find_all('name'))


# testa = loginEncoder(ipadd='', username='sdf', passwd='sdf', targetType='sdf')
# testa.powersmart()
r8 = requests.session()
getDeatilURL = 'http:///html/encoder/setup3.html?referer=1&id=0'
'get_device.cgi?rnd=" + Math.random()'
RequestURL = 'http:///get_encoder_1109.cgi?rnd=0.736911286746887'

# con = r8.get(RequestURL, headers={"If-Modified-Since": "0",
#                                        # 'Host': '%s' % (self.ipadd),
#                                         'Referer': 'http:///html/encoder/setup3.html?referer=1&id=1'
#                                        }, cookies={'logined': 'gg'}).content
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(con, "html.parser", )
# print(soup.prettify())
import json
import js2py  # 没用

with open('powersmartcgidetail2.html', encoding='utf8') as data:
    # data = js2py.eval_js(data)
    data = json.load(data)
print(data)
url7 = 'http:///html/encoder/index.html'
url8 = 'http:///login_new.cgi?user=&password='
url9 = 'http:///html/encoder/maininfo2.html?referer=1'
url10 = 'http:///encoder_status_new.cgi'
# r7 = requests.get(url7)
# r8 = requests.session()
# print(r8.post(url9,headers={'Content-Type': 'application/x-www-form-urlencoded'}))
#
# con = r8.get(url10,headers={"If-Modified-Since": "0",
#                             'Host':'',
#                             'Referer':'http:///html/encoder/maininfo2.html?referer=1'},cookies={'logined':'gg'}).content
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(con,"html.parser",)
#
# print(soup.prettify())
# print(soup.find_all('name'))

# print(r8.get(url10).text)

'''test login the ruima code'''
url = "http:///chinese/index.cgi?status___60"
user = ""
passwd = ""
auth_values = (user, passwd)
# response = requests.get(url, auth=auth_values)
# print(response.content)

# from bs4 import BeautifulSoup
# soup = BeautifulSoup(response.content,"html.parser",)
#
# print(soup.prettify())

# test log in the hongruan code
url11 = 'http:///login'
url3 = "http:///auth"
user3 = ""

import hashlib

mess = hashlib.md5()
mess.update(b'')
passwd3 = mess.hexdigest()
# import http.cookiejar, urllib.request
# cj = http.cookiejar.CookieJar()
# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
# r = opener.open(url11)
# print(cj)
# from urllib import request, parse
# # data = parse.urlencode(<your data dict>).encode()
# req =  request.Request(url11, ) # this will make the method "POST"
# # resp = request.urlopen(req)
# print(resp)
# postdata=urllib.parse.urlencode({'username': 'Admin',
# 'password':passwd3})
import urllib

archeaders = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '56',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'arcvideo-live-session=7CF0852280B76D0D65B5D62C07C12D44',
    'Host': '10.78.64.207',
    'Origin': 'http://10.78.64.207',
    'Referer': 'http://10.78.64.207/login',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
}
# form_data = [('username',''),('password','')]
# s=requests.Session()
# print(s.get(url11).headers)
# reqh=s.post(url3,data=form_data,headers=archeaders,timeout = 3).history
# for i in reqh:
#     print(i.headers)
# if s.cookies.get_dict():        #保持cookie有效
#     s.cookies.update(s.cookies)
# print(s.cookies)
# print(s.get('http:///listTask.action?pager.pageIndex=1&pager.pageSize=100').text)
'''





'''
# s= requests.get(url11)
# print(s.cookies)
# print('s1')
# s1= requests.post(url3,data=form_data,cookies=s.cookies,headers={'Content-Type': 'application/x-www-form-urlencoded',})
# print(s1)
# print(s.get('http:///listTask.action').content)

# print(s.cookies)
# s=requests.post(url3,data={'username': 'Admin','password':passwd3},headers={'Content-Type':'application/x-www-form-urlencoded'})
# s=requests.post(url3,data={"mimeType": "application/x-www-form-urlencoded",
#             "text": "username=&password=",
#             "params": [
#               {
#                 "name": "username",
#                 "value": ""
#               },
#               {
#                 "name": "password",
#                 "value": ""
#               }
#             ]})
# print(url3)
# print(s.text)
# #
# s=requests.Session()
# url4="http:///listTask.action?pager.pageIndex=1&pager.pageSize=100"
# cookies = {'arcvideo-live-session':'E6EEF0E839E034E025162291A13B8C11'}
# r = requests.get(url='http:///login')
# postdata2={"postData": {
#             "mimeType": "application/x-www-form-urlencoded",
#             "text": "username=Admin&password=319d13257a0f1058a95afd022d3730ab",
#             "params": [
#               {
#                 "name": "username",
#                 "value": ""
#               },
#               {
#                 "name": "password",
#                 "value": ""
#               }
#             ]
#           }}
# data={'username': '','password':''}
# r1 = requests.post(url3,data,)
# print(r1.cookies)
# url5='http:///login_new.cgi?user=manager&password='
# r2=requests.Session()
# r2.post(url5,cookies='')
# print('url5')
# print(r2.cookies)
# url6='http:///html/encoder/maininfo2.html?referer=1'
# r3 = requests.get(url6)
# print(r3.status_code)
# r=requests.post(url3,data={'username': 'Admin','password':passwd3},headers={'mimeType':'application/x-www-form-urlencoded'})
# r = requests.get(url4, cookies=cookies)
# response = s.get(url4,cookies='arcvideo-live-session=E6EEF0E839E034E025162291A13B8C11; Path=/; HttpOnly')
# print(r.cookies)
# print(r1.cookies)

# r = requests.get(url='http:///')
# print(response)
""""""
