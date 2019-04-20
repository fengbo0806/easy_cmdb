import requests
import re
from bs4 import BeautifulSoup
import hashlib
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import random
import time

'''
selenium
'''


class EncoderOperater:
    '''
    use to log in the encoder server with http, and get the value from the web page,
    :return resultdict
    {0: {'rowid': , 'switchStatus': , 'name': , 'programStatus': , 'outbandwidth': , 'width': , 'height': , 'inPutFirst':,
     'inPutSecond': , 'outPutFirst': , 'outPutHttpFlow': , 'outPutSecond': }}
    '''

    def __init__(self, ipadd=None, username=None, passwd=None, targetType=None, rawid='all'):
        self.ipadd = ipadd
        self.username = username
        self.passwd = passwd
        self.target = targetType
        self.loginURL = None
        self.getInfoURL = None
        self.inputUsr = None
        self.inputPas = None
        self.inputClick = None
        self.rawdi = rawid

    def doOption(self):
        judgeEncoder = {
            'powersmart': self.powersmart,
            'realmagic': self.realmagic,
            'arcvideo': self.arcvideo,
        }
        func = judgeEncoder.get(self.target, 'error')
        return func()

    def getRawIds(self, tagdic):
        if self.rawdi == 'all':
            return tagdic
        else:
            difflist = list(set(tagdic).difference(set(self.rawdi)))
            for keys in difflist:
                tagdic.pop(keys)
            return tagdic

    def loginTag(self):
        chromeDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver')
        option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        option.add_argument('lang=zh_CN.UTF-8')
        driver = webdriver.Chrome(chromeDir, chrome_options=option)
        driver.get(self.loginURL)
        driver.implicitly_wait(1)
        max_time = time.time() + 30
        while time.time() < max_time:
            if driver.find_element(By.ID, self.inputUsr[1]):
                print('load success')
                # driver.find_element(By.ID, self.inputUsr[1]).send_keys(self.username)
                break
            time.sleep(0.2)
        else:
            print('locator %s not found' % 'sss')
        if self.inputPas is not None:
            driver.find_element(self.inputPas[0], self.inputPas[1]).send_keys(self.passwd)
        driver.find_element(self.inputClick[0], self.inputClick[1]).click()
        driver.implicitly_wait(1)
        return driver

    def __powersmart(self):
        self.loginURL = 'http://%s/html/encoder/index.html' % (self.ipadd,)
        self.getInfoURL = 'http://%s/html/encoder/maininfo2.html?referer=1' % (self.ipadd,)
        self.getDeatilURL = 'http://%s/html/encoder/setup3.html?referer=1&id=0' % (self.ipadd,)
        self.inputUsr = [By.ID, 'loginname']
        self.inputPas = [By.ID, 'password']
        self.inputClick = [By.ID, 'Login_IndexImage']
        driver = self.loginTag()
        driver.find_element(By.ID, 'ChannelInfo_SettingImage1').click()
        time.sleep(1)
        driver.find_element(By.ID, 'leftEncodep').click()
        driver.implicitly_wait(1)
        # html =driver.find_element_by_xpath("*")
        html = driver.find_element_by_tag_name('html')

        # html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        print(html.get_attribute('innerHTML'))
        time.sleep(4)

        # driver.implicitly_wait(1)
        # driver.get(self.getDeatilURL)
        # while True:
        #     if driver.find_element(By.ID, 'Setup_ChannelName'):
        #         print('load success')
        #         # driver.find_element(By.ID, self.inputUsr[1]).send_keys(self.username)
        #         break
        #     time.sleep(0.2)
        driver.implicitly_wait(1)
        # print(driver.page_source)
        # driver.implicitly_wait(2)
        # print(driver)
        driver.quit()

    def powersmart(self):
        orderId = 0
        self.getInfoURL = 'http://%s/encoder_status_new.cgi' % (self.ipadd,)
        self.getDeatilURL = 'http://%s/html/encoder/setup3.html?referer=1&id=%d' % (self.ipadd, orderId)

        req = requests.session()
        con = req.get(self.getInfoURL, headers={"If-Modified-Since": "0",
                                                'Host': '%s' % (self.ipadd),
                                                'Referer': 'http://%s/html/encoder/maininfo2.html?referer=1' % (
                                                    self.ipadd)}, cookies={'logined': 'gg'}).content

        soup = BeautifulSoup(con, "html.parser", )
        # print(soup.encoder.id.get_text())
        resultdict = dict()
        resultdict[soup.encoder.id.get_text()] = {'rowid': soup.encoder.id.get_text(),
                                                  'switchStatus': soup.encoder.status.get_text(),
                                                  'name': soup.encoder.find('name').get_text(),
                                                  'width': soup.encoder.width.get_text(),
                                                  'height': soup.encoder.height.get_text(),
                                                  'outbandwidth': soup.encoder.outbandwidth.get_text(), }

        for sibling in soup.encoder.next_siblings:
            '''
            the sibling is not the same type of the original  tag ,it is just the next tag, in this circumstance
            next tag is 'bs4.element.Tag' or'bs4.element.NavigableString'
            '''
            if len(sibling) > 1:
                resultdict[sibling.id.get_text()] = {'rowid': sibling.id.get_text(),
                                                     'switchStatus': sibling.status.get_text(),
                                                     'name': sibling.find('name').get_text(),
                                                     'width': sibling.width.get_text(),
                                                     'height': sibling.height.get_text(),
                                                     'outbandwidth': sibling.outbandwidth.get_text(), }

        for key in resultdict.keys():
            import random
            orderId = key
            # print(type(key),key)
            '''
            powersmart always send the get URL with a random number, like get_device.cgi?rnd= + Math.random()
            '''
            'http://10.78.64.117/html/encoder/setup3.html?referer=1&id=0'
            RequestURL = 'http://%s/get_encoder_1109.cgi?rnd=%f' % (self.ipadd, round(random.random(), 15))
            # RequestURL = 'http://%s/html/encoder/setup3.html?referer=1&id=%d' % (self.ipadd, int(key))
            con = req.get(RequestURL, headers={"If-Modified-Since": "0",
                                               'Host': '%s' % (self.ipadd),
                                               'Referer': self.getDeatilURL
                                               }, cookies={'logined': 'gg'}).content
            soup = BeautifulSoup(con, "html.parser", )
            'channelCGIInfo[0]["OutputURL_HTTP"]="http://10.78.64.117:8088/ts0";'
            '''
            channelCGIInfo[0]["TSUDPIP"]="228.1.2.115";
            channelCGIInfo[0]["TSUDPPort"]=3000;
            '''
            searchHttpout = str(key) + '.*OutputURL_HTTP"]="http'
            searchUdpout = str(key) + '.*TSUDPIP"]="\d'
            searchUdpoutPort = str(key) + '.*TSUDPPort"]=\d'
            resultdict[key]['outPutFirst'] = None
            resultdict[key]['outPutSecond'] = None
            resultdict[key]['outPutSecond'] = None
            '''
            'inPutFirst':,
     'inPutSecond': , 'outPutFirst': , 'outPutHttpFlow': , 'outPutSecond'
            '''
            # print(soup.contents[0])
            for line in re.split('\n', soup.contents[0]):
                if not line:
                    break
                if re.search(searchHttpout, line, ):
                    resultdict[key]['outPutFirst'] = re.split('"', line)[-2]
                    print(line)
                if re.search(searchUdpout, line, ):
                    resultdict[key]['outPutSecond'] = re.split('"', line)[-2]
                    # print(line)
                if re.search(searchUdpoutPort, line, ):
                    resultdict[key]['outPutSecond'] = resultdict[key]['outPutSecond'] + ':' + str(
                        re.split('[=;]', line)[-2])
                    print(line)

        return resultdict

    def realmagic(self):
        '''
        login the realmagic code
        '''
        url = "http://%s/chinese/index.cgi?status___60" % (self.ipadd)
        auth_values = (self.username, self.passwd)
        response = requests.get(url, auth=auth_values)
        soup = BeautifulSoup(response.content, "html.parser", )
        midleresult = dict()
        resultdict = dict()
        encoderKeyValueCount = 0
        loopCheckNumber = 0
        encoderKeyValue = ('rowid', 'switchStatus', 'name', 'programStatus', 'video', 'sound', 'load')
        con = soup.find(text=re.compile('频道'))
        con = con.parent.parent
        for sibling in con.next_siblings:
            if sibling.name == 'tr':
                for child in sibling.children:
                    # print(child)
                    if child.name == 'td':
                        midleresult[encoderKeyValue[encoderKeyValueCount]] = child.text.strip()
                        encoderKeyValueCount = encoderKeyValueCount + 1
                resultdict[loopCheckNumber] = midleresult
                midleresult = dict()
                loopCheckNumber = loopCheckNumber + 1
                encoderKeyValueCount = 0
        for item in resultdict:
            if resultdict[item]['switchStatus'] == 'ON':
                resultdict[item]['switchStatus'] = True
            else:
                resultdict[item]['switchStatus'] = False
            '''
            some error with programStatus check,fix it Tomorrow
            '''
            if resultdict[item]['programStatus'] == '0[Q:0%]':
                resultdict[item]['programStatus'] = -1
            else:
                resultdict[item]['programStatus'] = 1
        if self.rawdi == 'all':
            pass
        else:
            difflist = list(set(resultdict).difference(set(self.rawdi)))
            for keys in difflist:
                resultdict.pop(keys)
        for item in resultdict:
            getEncUrl = "http://%s/chinese/index.cgi?enc_setup___%d" % (self.ipadd, item)
            responseEnc = requests.get(getEncUrl, auth=auth_values)
            soupEnc = BeautifulSoup(responseEnc.content, "html.parser", )

            getInputUrl = "http://%s/chinese/index.cgi?input_setup___%d" % (self.ipadd, item)
            responseInput = requests.get(getInputUrl, auth=auth_values)
            soupInput = BeautifulSoup(responseInput.content, "html.parser", )

            getOutputUrl = "http://%s/chinese/index.cgi?output_setup___%d" % (self.ipadd, item)
            responseOutput = requests.get(getOutputUrl, auth=auth_values)
            soupOutput = BeautifulSoup(responseOutput.content, "html.parser", )

            '''
            deal with the encode part,get the value of outbandwidth,width,height

            '''
            resultdict[item]['outbandwidth'] = soupEnc.find('input', id='enc_total_bitrate')["value"]
            resultdict[item]['width'] = soupEnc.find('input', id='enc_video_cwidth')["value"]
            resultdict[item]['height'] = soupEnc.find('input', id='enc_video_cheight')["value"]
            '''
            deal with the in put part,get the value of inPutFirst
            '''
            resultdict[item]['inPutFirst'] = soupInput.find('input', attrs={'name': 'ipinput_address___%d' % (item)})[
                "value"].strip()
            resultdict[item]['inPutSecond'] = soupInput.find('input', attrs={'name': 'ipinput_address2___%d' % (item)})[
                "value"].strip()
            '''
            deal with the out put part,get the value of outPutFirst,outPutSecond,outPutHttpFlow
            '''
            consult = soupOutput.find_all('span', attrs={'class': 'unwrap_label'})
            countNum = 0
            outPutKEY = ('outPutFirst', 'outPutSecond')
            for iItem in consult:
                if countNum > 1:
                    '''
                    only count to second,drop others
                    '''
                    break
                resultdict[item][outPutKEY[countNum]] = iItem.get_text().strip()
                if re.findall('http', resultdict[item][outPutKEY[countNum]]):
                    resultdict[item]['outPutHttpFlow'] = resultdict[item][outPutKEY[countNum]]
                countNum = countNum + 1

            '''
            drop unuse data
            '''
            resultdict[item].pop('video')
            resultdict[item].pop('sound')
            resultdict[item].pop('load')

        return resultdict

    def arcvideo(self):
        '''
        login the arcvideo server and get data
        this server need the selenium package to transfer JS data
        arcvideo send the password with md5 auth
        :return: resultdict
        '''
        resultdict = dict()
        keyvalue = 1
        # md5Mess = hashlib.md5()
        # md5Mess.update(self.passwd)
        # self.passwd = md5Mess.hexdigest()
        urllogin = 'http://%s/login' % (self.ipadd,)
        urlaction = "http://%s/listTask.action" % (self.ipadd,)
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
        archeaders = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '56',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': 'arcvideo-live-session=7CF0852280B76D0D65B5D62C07C12D44',
            'Host': 'ipadd',
            'Origin': 'http://ipadd',
            'Referer': 'http://ipadd/login',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        }
        chromeDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver')
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        driver = webdriver.Chrome(chromeDir, chrome_options=option)
        driver.get(urllogin)
        driver.find_element_by_name("username_1").send_keys(self.username)
        driver.find_element_by_name("password_1").send_keys(self.passwd)
        driver.find_element_by_class_name("input_submit").click()
        driver.implicitly_wait(5)
        driver.get(urlaction)
        '''
        '''
        soup = BeautifulSoup(driver.page_source, "html.parser", )
        con = soup.find('table', attrs={'class': 'appui_listview single_selection'})
        contr = con.find('tr')
        for sibling in contr.next_siblings:
            if sibling.name == 'tr':
                if sibling.find('a') is not None:
                    valuea = sibling.find('a').get_text()
                    resultdict[valuea] = dict()
                    keyvalue = valuea
                    resultdict[valuea]['rowid'] = valuea
                if sibling.find('div', attrs={'class': 'appui_text_ellipsis'}) is not None:
                    valuediv = sibling.find('div', attrs={'class': 'appui_text_ellipsis'}).get_text()
                    resultdict[keyvalue]['name'] = valuediv
                if sibling.find('td', attrs={'class': 'TaskStatusDesc TaskStatusGrey'}):
                    resultdict[keyvalue]['switchStatus'] = False
                    # valuetd = sibling.find('td', attrs={'class': 'TaskStatusDesc'}).get_text()
                    # if valuetd == '取消' or valuetd == '就绪':
                elif sibling.find('td', attrs={'class': 'TaskStatusDesc TaskStatusOrange'}):
                    resultdict[keyvalue]['switchStatus'] = True
                elif sibling.find('td', attrs={'class': 'TaskStatusDesc TaskStatusGreen'}):
                    resultdict[keyvalue]['switchStatus'] = True
        for keys in resultdict.keys():
            getEncUrl = 'http://%s/viewTask?taskId=%d&rnd=%f' % (self.ipadd, int(keys), random.random())
            driver.get(getEncUrl)
            soup = BeautifulSoup(driver.page_source, "html.parser", )
            print(soup.contents)
            # break
            fistset = str(keys) + '_0'
            secondset = str(keys) + '_1'
            if soup.find('div', id=fistset):
                resultdict[keys]['outPutFirst'] = soup.find('div', id=fistset).find('input', id='UrlBase')["value"] + \
                                                  soup.find('div', id=fistset).find('input', id='OutputLocation')[
                                                      "value"]
            if soup.find('div', id=secondset):
                resultdict[keys]['outPutSecond'] = soup.find('div', id=secondset).find('input', id='OutputLocation')[
                    "value"]
            '''
            get width and height
            '''
            encodespan = soup.find('div', id='356_0').findAll('span', )[-1]
            encodespanitem = list(filter(None, re.split('[\n|\t]', encodespan.get_text())))
            '''
             ['H264', '1920x1080', '@25fps', 'VBR', '3800Kbps ', '    ', 'MP2', '48.0kHz', '2', 'channels', '256',
                 'Kbps']
            '''
            wAndH = re.split('x', encodespanitem[1])
            resultdict[keys]['width'], resultdict[keys]['height'] = wAndH[0], wAndH[1]
            resultdict[keys]['outbandwidth'] = int(re.sub("\D", "", encodespanitem[4]))
            if soup.find('div', id='iSrcMediaInfoContainer').find('span', attrs={'class': 'media_url'}):
                resultdict[keys]['inPutFirst'] = soup.find('div', id='iSrcMediaInfoContainer').find('span', attrs={
                    'class': 'media_url'}).get_text()
            if soup.find('div', id='optional_inputs').find('span', attrs={'class': 'media_url'}):
                resultdict[keys]['inPutSecond'] = soup.find('div', id='optional_inputs').find('span', attrs={
                    'class': 'media_url'}).get_text()
        driver.close()
        return resultdict

    class GetEncoderStatus:
        def __init__(self, ipadd, username, passwd, targetType):
            self.ipadd = ipadd
            self.username = username
            self.passwd = passwd
            self.target = targetType
            self.loginURL = None
            self.getInfoURL = None

        def doOption(self):
            judgeEncoder = {
                'powersmart': self.powersmart,
                'realmagic': self.realmagic,
                'arcvideo': self.arcvideo,
            }
            func = judgeEncoder.get(self.target, 'error')
            return func()

        def powersamrt(self):
            pass

        def realmagic(self):
            pass

        def arcvideo(self):
            pass


if __name__ == '__main__':
    '''
    use for test 
    '''

    testobj = EncoderOperater(ipadd='10.78.64.207', username='Admin', passwd='Arc123456', targetType='arcvideo', )
    result = testobj.doOption()
    # print(result.)
    '''
    use to log in the encoder server with http, and get the value from the web page,
    :return resultdict
    {0: {'rowid': , 'switchStatus': , 'name': , 'programStatus': , 'outbandwidth': , 'width': , 'height': , 'inPutFirst':,
     'inPutSecond': , 'outPutFirst': , 'outPutHttpFlow': , 'outPutSecond': }}
     {'0': {'id': '0', 'status': '0', 'name': 'CCTV4HD-卫星备2017', 'width': '640', 'height': '360', 'outbandwidth': '308'}, '1': {'id': '1', 'status': '0', 'name': 'CCTV5HD-总控备', 'width': '640', 'height': '360', 'outbandwidth': '308'}, '2': {'id': '2', 'status': '0', 'name': 'CCTV4HD-卫星备2017', 'width': '1920', 'height': '1080', 'outbandwidth': '8000'}, '3': {'id': '3', 'status': '0', 'name': 'CCTV5HD-总控备', 'width': '1920', 'height': '1080', 'outbandwidth': '8000'}}

    '''

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import os

    ''' 
    chromeDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver')
    print(chromeDir)
    # driver = webdriver.Chrome('/path/to/chromedriver')

    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    driver = webdriver.Chrome(chromeDir, chrome_options=option)
    url = "https://www.baidu.com"
    driver.get("http://ipadd/login")
    driver.find_element_by_name("username_1").send_keys("")
    driver.find_element_by_name("password_1").send_keys("")
    driver.find_element_by_class_name("input_submit").click()
    driver.implicitly_wait(5)
    driver.get("http://ipadd/listTask.action")
    
    "http://ipadd/viewTask?taskId=323&rnd=0.4677657860893727"
    
    '''
    # from bs4 import BeautifulSoup
    #
    # with open('hongruan.html') as htmlts:
    #     soup = BeautifulSoup(htmlts, "html.parser", )
    #     # soup.find()
    #     con = soup.find('table', attrs={'class': 'appui_listview single_selection'})
    #     # print(con)
    #     con2 = con.find('tr')
    #     # print(con2)
    #     for sibling in con2.next_siblings:
    #         # if sibling.find('div')==-1:
    #         #     print(sibling)
    #         # elif sibling.find('div')==None:
    #         #     print(sibling)
    #         # if len(sibling) > 1:
    #         if sibling.name == 'tr':
    #             # print(sibling)
    #             if sibling.find('a') is not None:
    #                 print(sibling.find('a').get_text())
    #             if sibling.find('div', attrs={'class': 'appui_text_ellipsis'}) is not None:
    #                 print(sibling.find('div', attrs={'class': 'appui_text_ellipsis'}).get_text())
'''
19: {'rowid': '19', 'switchStatus': True, 'name': '移动直播20', 'programStatus': -1, 'outbandwidth': '4000',
     'width': '960', 'height': '540',
     'inPutFirst': 'rtmp://vlive.people.com.cn/2010/1-18-11-29-1500/live_2 ',
     'outPutFirst': 'udp://@228.1.2.145:5000', 'outPutSecond': 'http://10.78.64.195:1254/live20',
     'outPutHttpFlow': 'http://10.78.64.195:1254/live20'}}
     '''

# for sibling in con.next_siblings:
#     print(sibling)
# class ="tab_content even" value="331" >
# < div
#
#
# class ="appui_text_ellipsis" style="display:inline-block;vertical-align:middle;" > 阿里云-CCTV5+HD < / div >
# print(driver.page_source)
# print(driver.find_element_by_tag_name('table').text)
# try:
#     WebDriverWait(driver.get("http://ipadd/#listTask.action"), 5)
#
# finally:
#     driver.quit()
# print(driver.page_source)
# for link in driver.find_element_by_xpath("//*[@href]"):
#     print(link.get_attribute('href'))
# driver.get(url)
# print(driver.title)

# result = EncoderOperater(ipadd='ip', username='name', passwd='password', targetType='arcvideo')
# valuesDict = result.doOption()
# print(valuesDict)
# driver = webdriver.Firefox()

# import time
#
# time.sleep(1)
# print(pagedata.page_source)
# for link in driver.find_element_by_xpath("//*[@href]"):
#     print(link.get_attribute('href'))
