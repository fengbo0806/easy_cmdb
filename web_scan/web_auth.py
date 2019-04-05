import requests
import re
from bs4 import BeautifulSoup
import hashlib

'''
selenium
'''


class EncoderOperater:
    '''
    use to log in the encoder server with http, and get the value from the web page,
    :return resultdict
    '''

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
        resultdict[soup.encoder.id.get_text()] = {'id': soup.encoder.id.get_text(),
                                                  'status': soup.encoder.status.get_text(),
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
                resultdict[sibling.id.get_text()] = {'id': sibling.id.get_text(),
                                                     'status': sibling.status.get_text(),
                                                     'name': sibling.find('name').get_text(),
                                                     'width': sibling.width.get_text(),
                                                     'height': sibling.height.get_text(),
                                                     'outbandwidth': sibling.outbandwidth.get_text(), }

        for key in resultdict.keys():
            import random
            orderId = key
            '''
            powersmart always send the get URL with a random number, like get_device.cgi?rnd= + Math.random()
            '''
            RequestURL = 'http://%s/get_encoder_1109.cgi?rnd=%f' % (self.ipadd, round(random.random(), 15))
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
        md5Mess = hashlib.md5()
        md5Mess.update(self.passwd)
        self.passwd = md5Mess.hexdigest()
        urllogin = 'http://%s/login' % (self.ipadd,)
        urlauth = "http://%s/auth" % (self.ipadd,)
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
            'Host': '10.78.64.207',
            'Origin': 'http://10.78.64.207',
            'Referer': 'http://10.78.64.207/login',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        }
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
    result = EncoderOperater(ipadd='ip', username='name', passwd='password', targetType='type')
    valuesDict = result.doOption()
    print(valuesDict)
