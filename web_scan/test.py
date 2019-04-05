from bs4 import BeautifulSoup

dataenco ={0: {'rowid': '0', 'switchStatus': True, 'name': '移动直播01', 'programStatus': -1, 'outbandwidth': '2000', 'width': '960',
     'height': '540', 'inPutFirst': 'rtmp://play.news.ghwx.com.cn/live1/ch ', 'outPutFirst': 'udp://@228.1.2.140:1000',
     'outPutSecond': 'http://10.78.64.195:1235/live01', 'outPutHttpFlow': 'http://10.78.64.195:1235/live01'},
 1: {'rowid': '1', 'switchStatus': True, 'name': '移动直播02', 'programStatus': -1, 'outbandwidth': '2000', 'width': '1280',
     'height': '720', 'inPutFirst': 'rtmp://bililive.kksmg.com/hls/vmix ', 'outPutFirst': 'udp://@228.1.2.140:2000',
     'outPutSecond': 'http://10.78.64.195:1236/live02', 'outPutHttpFlow': 'http://10.78.64.195:1236/live02'},
 2: {'rowid': '2', 'switchStatus': True, 'name': '移动直播03', 'programStatus': -1, 'outbandwidth': '2000', 'width': '1280',
     'height': '720', 'inPutFirst': 'rtmp://play.news.ghwx.com.cn/live2/channel2 ',
     'outPutFirst': 'udp://@228.1.2.140:3000', 'outPutSecond': 'http://10.78.64.195:1237/live03',
     'outPutHttpFlow': 'http://10.78.64.195:1237/live03'},
 3: {'rowid': '3', 'switchStatus': True, 'name': '移动直播04', 'programStatus': -1, 'outbandwidth': '2000', 'width': '1280',
     'height': '720', 'inPutFirst': 'rtmp://rtmpdist-w.quklive.com/live/w1553663022875771 ',
     'outPutFirst': 'udp://@228.1.2.140:4000', 'outPutSecond': 'http://10.78.64.195:1238/live04',
     'outPutHttpFlow': 'http://10.78.64.195:1238/live04'},
 4: {'rowid': '4', 'switchStatus': True, 'name': '移动直播05', 'programStatus': -1, 'outbandwidth': '2000', 'width': '1280',
     'height': '720', 'inPutFirst': 'http://192.168.169.12:8088/lianghui1 ',
     'outPutFirst': 'http://10.78.64.195:1239/live05', 'outPutHttpFlow': 'http://10.78.64.195:1239/live05',
     'outPutSecond': 'udp://@228.1.2.140:5000'},
 5: {'rowid': '5', 'switchStatus': True, 'name': '移动直播06', 'programStatus': -1, 'outbandwidth': '2000', 'width': '1280',
     'height': '720', 'inPutFirst': 'http://192.168.169.12:8088/lianghui1 ',
     'outPutFirst': 'http://10.78.64.195:1240/live06', 'outPutHttpFlow': 'http://10.78.64.195:1240/live06',
     'outPutSecond': 'udp://@228.1.2.141:1000'},
 6: {'rowid': '6', 'switchStatus': True, 'name': '移动直播07', 'programStatus': -1, 'outbandwidth': '2000', 'width': '1280',
     'height': '720', 'inPutFirst': 'rtmp://3357.liveplay.myqcloud.com/live/3357_43011163691611e6a2cba4dcbef5e35a ',
     'outPutFirst': 'http://10.78.64.195:1241/live07', 'outPutHttpFlow': 'http://10.78.64.195:1241/live07',
     'outPutSecond': 'udp://@228.1.2.141:2000'},
 7: {'rowid': '7', 'switchStatus': True, 'name': '移动直播08', 'programStatus': -1, 'outbandwidth': '2000', 'width': '1280',
     'height': '720', 'inPutFirst': 'http://dl.live.cntv.cn/direct_play?rid=10061&role=Creator ',
     'outPutFirst': 'http://10.78.64.195:1242/live08', 'outPutHttpFlow': 'http://10.78.64.195:1242/live08',
     'outPutSecond': 'udp://@228.1.2.141:3000'},
 8: {'rowid': '8', 'switchStatus': True, 'name': '移动直播09', 'programStatus': -1, 'outbandwidth': '2000', 'width': '1280',
     'height': '720', 'inPutFirst': 'rtmp://59.110.126.141/live/CCTV158b49aab907944541a2587b5e2a534adfH ',
     'outPutFirst': 'http://10.78.64.195:1243/live09', 'outPutHttpFlow': 'http://10.78.64.195:1243/live09',
     'outPutSecond': 'udp://@228.1.2.141:4000'},
 9: {'rowid': '9', 'switchStatus': True, 'name': '移动直播10', 'programStatus': -1, 'outbandwidth': '4000', 'width': '960',
     'height': '540', 'inPutFirst': 'rtmp://10.78.43.20/wxmlive/skating ',
     'outPutFirst': 'http://10.78.64.195:1244/live10', 'outPutHttpFlow': 'http://10.78.64.195:1244/live10',
     'outPutSecond': 'udp://@228.1.2.141:5000'},
 10: {'rowid': '10', 'switchStatus': True, 'name': '移动直播11', 'programStatus': -1, 'outbandwidth': '4000',
      'width': '960', 'height': '540', 'inPutFirst': '0 ', 'outPutFirst': 'udp://@228.1.2.144:1000',
      'outPutSecond': 'http://10.78.64.195:1245/live11', 'outPutHttpFlow': 'http://10.78.64.195:1245/live11'},
 11: {'rowid': '11', 'switchStatus': True, 'name': '移动直播12', 'programStatus': 1, 'outbandwidth': '4000', 'width': '960',
      'height': '540', 'inPutFirst': 'http://192.168.169.12:8088/lianghui2 ', 'outPutFirst': 'udp://@228.1.2.144:2000',
      'outPutSecond': 'http://10.78.64.195:1246/live12', 'outPutHttpFlow': 'http://10.78.64.195:1246/live12'},
 12: {'rowid': '12', 'switchStatus': True, 'name': '移动直播13', 'programStatus': -1, 'outbandwidth': '1000',
      'width': '960', 'height': '540', 'inPutFirst': 'rtmp://rtmpdist-w.quklive.com/live/w1537255242556775 ',
      'outPutFirst': 'udp://@228.1.2.144:3000', 'outPutSecond': 'http://10.78.64.195:1247/live13',
      'outPutHttpFlow': 'http://10.78.64.195:1247/live13'},
 13: {'rowid': '13', 'switchStatus': True, 'name': '移动直播14', 'programStatus': -1, 'outbandwidth': '1000',
      'width': '960', 'height': '540', 'inPutFirst': 'http://dl.live.cntv.cn/direct_play?rid=10061&role=Creator ',
      'outPutFirst': 'udp://@228.1.2.144:4000', 'outPutSecond': 'http://10.78.64.195:1248/live14',
      'outPutHttpFlow': 'http://10.78.64.195:1248/live14'},
 14: {'rowid': '14', 'switchStatus': True, 'name': '移动直播15', 'programStatus': -1, 'outbandwidth': '1000',
      'width': '960', 'height': '540', 'inPutFirst': 'rtmp://rtmpdist-w.quklive.com/live/w1542682109696713 ',
      'outPutFirst': 'udp://@228.1.2.144:5000', 'outPutSecond': 'http://10.78.64.195:1249/live15',
      'outPutHttpFlow': 'http://10.78.64.195:1249/live15'},
 15: {'rowid': '15', 'switchStatus': True, 'name': '移动直播16', 'programStatus': -1, 'outbandwidth': '1000',
      'width': '960', 'height': '540', 'inPutFirst': 'http://61.49.160.199:8080/live/cct ',
      'outPutFirst': 'udp://@228.1.2.145:1000', 'outPutSecond': 'http://10.78.64.195:1250/live16',
      'outPutHttpFlow': 'http://10.78.64.195:1250/live16'},
 16: {'rowid': '16', 'switchStatus': True, 'name': '移动直播17', 'programStatus': -1, 'outbandwidth': '1000',
      'width': '960', 'height': '540', 'inPutFirst': 'rtmp://10.78.43.20/live/officecut01 ',
      'outPutFirst': 'udp://@228.1.2.145:2000', 'outPutSecond': 'http://10.78.64.195:1251/live17',
      'outPutHttpFlow': 'http://10.78.64.195:1251/live17'},
 17: {'rowid': '17', 'switchStatus': True, 'name': '移动直播18', 'programStatus': -1, 'outbandwidth': '1000',
      'width': '960', 'height': '540',
      'inPutFirst': 'rtmp://59.110.126.141/live/CCTV12e5b1b1b16f644bdf9b972c9f13c3872aH ',
      'outPutFirst': 'udp://@228.1.2.145:3000', 'outPutSecond': 'http://10.78.64.195:1252/live18',
      'outPutHttpFlow': 'http://10.78.64.195:1252/live18'},
 18: {'rowid': '18', 'switchStatus': True, 'name': '移动直播19', 'programStatus': -1, 'outbandwidth': '1000',
      'width': '960', 'height': '540', 'inPutFirst': 'rtmp://59.110.127.144/live/CCTV2PGC1 ',
      'outPutFirst': 'udp://@228.1.2.145:4000', 'outPutSecond': 'http://10.78.64.195:1253/live19',
      'outPutHttpFlow': 'http://10.78.64.195:1253/live19'},
 19: {'rowid': '19', 'switchStatus': True, 'name': '移动直播20', 'programStatus': -1, 'outbandwidth': '4000',
      'width': '960', 'height': '540', 'inPutFirst': 'rtmp://vlive.people.com.cn/2010/1-18-11-29-1500/live_2 ',
      'outPutFirst': 'udp://@228.1.2.145:5000', 'outPutSecond': 'http://10.78.64.195:1254/live20',
      'outPutHttpFlow': 'http://10.78.64.195:1254/live20'}}
# testa = loginEncoder(ipadd='10.78.64.195', username='admin', passwd='cntv.cn@real', targetType='sdf')
# aaa = testa.realmagic()
# print(aaa)
# testlist = list()
url1 = "http://10.78.64.193/chinese/index.cgi?status___60"
url2 = "http://10.78.64.193/chinese/index.cgi?input_setup___0"
url3 = "http://10.78.64.193/chinese/index.cgi?enc_setup___0"
url4 = "http://10.78.64.193/chinese/index.cgi?output_setup___0"
'''
<frame src="index.cgi?input_setup___0" name="mainFrame" id="mainFrame" title="mainFrame" noresize="noresize">
<input class="edit" name="ipinput_address___0" size="39" type="text" value="http://192.168.169.12:8088/yuxuan1 "/>
      <span class="unwrap_label">
       udp://@228.2.1.15:1000
      </span>
'''
# user = "admin"
# passwd = "cntv.cn@real"
# auth_values = (user, passwd)
# response=requests.session()
# response.get(url1, auth=auth_values)

# con = response.get(url4,auth=auth_values).content
#
# soup = BeautifulSoup(con, "html.parser", )
# print(soup.prettify())
with open('ruimainput.html') as con:
    soup = BeautifulSoup(con, "html.parser", )
    #
    print(soup.find('input', attrs={'name': 'ipinput_address___0'})["value"])
    #     print(soup.find_all('span',attrs={'class':'unwrap_label'}))
    # conslut = soup.find_all('span', attrs={'class': 'unwrap_label'})
    # countNum = 0
    # for i in conslut:
    #     print(i.get_text().strip())
    #     countNum = countNum + 1
    #     if countNum > 1:
    #         break
    '''
    http://10.78.64.193:4001/tiyu01
udp://@228.2.1.15:1000
outPutFirst = models.CharField(max_length=255, null=True, blank=True)
outPutSecond = models.CharField(max_length=255, null=True, blank=True)
outPutHttpFlow = models.URLField()
    '''

# r8 = requests.session()
getDeatilURL = 'http:///html/encoder/setup3.html?referer=1&id=0'
'get_device.cgi?rnd=" + Math.random()'
RequestURL = 'http:///get_encoder_1109.cgi?rnd=0.736911286746887'

# con = r8.get(RequestURL, headers={"If-Modified-Since": "0",
#                                        # 'Host': '%s' % (self.ipadd),
#                                         'Referer': 'http:///html/encoder/setup3.html?referer=1&id=1'
#                                        }, cookies={'logined': 'gg'}).content
# from bs4 import BeautifulSoup
#

#     print(soup.find('input', id='enc_video_cheight')["value"])
# for link in soup.find_all('a'):
#     print(link.get('href'))
# for child in soup.tr.children:
#     print(child)
#     print('*'*10)
# for link in soup.find_all('tr'):
#     # for con in link.contents:
#         # if len(con)>1:
#     testlist.append(link.contents[5])
#         # print(con)
#     print('-'*10)
# print(testlist)
# print(soup.a.next_siblings)
#
#     midleresult = dict()
#     resultdict = dict()
#     encoderKeyValueCount = 0
#     loopCheckNumber = 0
#     encoderKeyValue = ('id', 'status', 'name', 'width', 'height', 'outbandwidth', '7')
#     con = soup.find(text=re.compile('频道'))
#     con = con.parent.parent
#     for sibling in con.next_siblings:
#         if sibling.name == 'tr':
#             for child in sibling.children:
#                 # print(child)
#                 if child.name == 'td':
#                     midleresult[encoderKeyValue[encoderKeyValueCount]] = child.text.strip()
#                     encoderKeyValueCount = encoderKeyValueCount + 1
#             resultdict[loopCheckNumber] = midleresult
#             loopCheckNumber = loopCheckNumber + 1
#             encoderKeyValueCount = 0
# print(resultdict)
'''
    {'0': [{'id': '0', 'status': '-1', 'name': '银川公共-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}], '1': [{'id': '1', 'status': '-1', 'name': '杭州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}], '2': [{'id': '2', 'status': '0', 'name': '广州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}], '3': [{'id': '3', 'status': '0', 'name': '福州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}], '4': [{'id': '4', 'status': '0', 'name': '郑州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}], '5': [{'id': '5', 'status': '0', 'name': '兰州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}]}
    ['0', 'ON', '移动直播01', '0[Q:0%]', '0', '0', '1%', '1', 'ON', '移动直播02', '0[Q:0%]', '0', '0', '1%', '2', 'ON', '移动直播03', '1234[Q:100%]', '179120', '335864', '0%', '3', 'ON', '移动直播04', '1335[Q:100%]', '179226', '336061', '0%', '4', 'ON', '移动直播05', '0[Q:0%]', '0', '0', '0%', '5', 'ON', '移动直播06', '0[Q:0%]', '0', '0', '0%', '6', 'ON', '移动直播07', '0[Q:0%]', '0', '0', '0%', '7', 'ON', '移动直播08', '0[Q:0%]', '0', '0', '0%', '8', 'ON', '移动直播09', '0[Q:0%]', '0', '0', '0%', '9', 'ON', '移动直播10', '0[Q:0%]', '0', '0', '0%', '10', 'ON', '移动直播11', '0[Q:0%]', '0', '0', '0%', '11', 'ON', '移动直播12', '0[Q:0%]', '0', '0', '0%', '12', 'ON', '移动直播13', '0[Q:0%]', '0', '0', '0%', '13', 'ON', '移动直播14', '0[Q:0%]', '0', '0', '0%', '14', 'ON', '移动直播15', '0[Q:0%]', '0', '0', '0%', '15', 'ON', '移动直播16', '0[Q:0%]', '0', '0', '0%', '16', 'ON', '移动直播17', '0[Q:0%]', '0', '0', '0%', '17', 'ON', '移动直播18', '0[Q:0%]', '0', '0', '0%', '18', 'ON', '移动直播19', '0[Q:0%]', '0', '0', '0%', '19', 'ON', '移动直播20', '0[Q:0%]', '0', '0', '0%']
    {0: {'id': '0', 'status': 'ON', 'name': '移动直播01', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '1%'}, 1: {'id': '1', 'status': 'ON', 'name': '移动直播02', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '1%'}, 2: {'id': '2', 'status': 'ON', 'name': '移动直播03', 'width': '1234[Q:100%]', 'height': '179120', 'outbandwidth': '335864', '7': '0%'}, 3: {'id': '3', 'status': 'ON', 'name': '移动直播04', 'width': '1335[Q:100%]', 'height': '179226', 'outbandwidth': '336061', '7': '0%'}, 4: {'id': '4', 'status': 'ON', 'name': '移动直播05', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 5: {'id': '5', 'status': 'ON', 'name': '移动直播06', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 6: {'id': '6', 'status': 'ON', 'name': '移动直播07', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 7: {'id': '7', 'status': 'ON', 'name': '移动直播08', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 8: {'id': '8', 'status': 'ON', 'name': '移动直播09', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 9: {'id': '9', 'status': 'ON', 'name': '移动直播10', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 10: {'id': '10', 'status': 'ON', 'name': '移动直播11', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 11: {'id': '11', 'status': 'ON', 'name': '移动直播12', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 12: {'id': '12', 'status': 'ON', 'name': '移动直播13', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 13: {'id': '13', 'status': 'ON', 'name': '移动直播14', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 14: {'id': '14', 'status': 'ON', 'name': '移动直播15', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 15: {'id': '15', 'status': 'ON', 'name': '移动直播16', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 16: {'id': '16', 'status': 'ON', 'name': '移动直播17', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 17: {'id': '17', 'status': 'ON', 'name': '移动直播18', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 18: {'id': '18', 'status': 'ON', 'name': '移动直播19', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}, 19: {'id': '19', 'status': 'ON', 'name': '移动直播20', 'width': '0[Q:0%]', 'height': '0', 'outbandwidth': '0', '7': '0%'}}

'''

# print(sibling.contents[1].get_text(),sibling.contents[3].get_text())
# print(sibling.td.get_text())


# with open('powersmartcgidetail2.html', encoding='utf8') as data:
#     # data = js2py.eval_js(data)
#     data = json.load(data)
# print(data)
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
target = 'realmagic'


def powersmart():
    print('powersmart')


def realmagic():
    print('realmagic')


def arcvideo():
    print('arcvideo')


def doOption():
    judgeEncoder = {
        'powersmart': powersmart,
        'realmagic': realmagic,
        'arcvideo': arcvideo,
    }
    func = judgeEncoder.get('realmagic')
    print(0)
    return func()
