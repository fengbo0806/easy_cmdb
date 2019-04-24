from bs4 import BeautifulSoup
import re
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "http://10.78.64.30/cgi-bin/status.cgi"
auth_values = ('root', '12345')
response = requests.get(url, auth=auth_values)
soup = BeautifulSoup(response.content, "html.parser", )
'''
<input checked="" id="in3" name="tuner_check" onclick="check3();" type="checkbox" value="1">
<input id="tun1_id" name="tuner_bitrate" readonly="readonly" size="12" type="text" value="38.013544"/>
<input name="Strength_Seport" readonly="readonly" size="12" type="text" value="-33.0"/>
<td><input name="tuner_valid_bitrate" readonly="readonly" size="12" type="text" value="33.990344"/>
<input name="tuner_format" readonly="readonly" size="12" type="text" value="188"/>
'''

print(soup.contents)
class loginencoder(object):
    pass
    loginURL = 'http://'
    passwd = ''
    chromeDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver')
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    option.add_argument('lang=zh_CN.UTF-8')
    driver = webdriver.Chrome(chromeDir, chrome_options=option)
    driver.get(loginURL)
    driver.find_element(By.ID, 'password').send_keys(passwd)
    driver.find_element(By.ID, 'Login_IndexImage').click()
    driver.implicitly_wait(1)
    # print(driver.page_source)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "html")))

    baseContext = BeautifulSoup(driver.page_source, "html.parser", )
    programsInfo = baseContext.find_all('ul', attrs={'class': 'spritesAll ul1'})
    # print(len(programsInfo))
    programsMain = baseContext.find_all('td', attrs={'id': 'ChannelInfo_ChannelIndex0'})
    programsbackup = baseContext.find_all('td', attrs={'id': 'ChannelInfo_ChannelIndex1'})
    for rowid in range(0, len(programsInfo)):
        countSubNum = 0
        driver.find_element(By.ID, 'ChannelInfo_SettingImage%d' % (rowid,)).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "html")))
        # WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"html")))
        # print(driver.page_source)
        driver.find_element(By.ID, 'Setup_MainChannel').click()
        print('rowid:',str(rowid+1) + str(countSubNum))
        print(driver.find_element(By.XPATH, '//input[@name="ChannelName"]').get_attribute("value"))
        print(driver.find_element(By.XPATH, '//td[@id="VideoSize_l"]').text)
        print(driver.find_element(By.XPATH, '//span[@id="OutputURL_HTTP_sub1"]').get_attribute('innerHTML'))
        print(driver.find_element(By.XPATH, '//input[@name="TSUDPIP"]').get_attribute("value"))
        print(driver.find_element(By.XPATH, '//input[@name="TSUDPPort"]').get_attribute("value"))
        print(driver.find_element(By.XPATH, '//input[@name="TSUDPPort"]').get_attribute("value"))
        # driver.find_element(By.XPATH, '//input[@name="TSUDPPort"]').get_attribute("value")
        test = driver.find_element(By.XPATH, '//td[@id="VideoSize_l"]').text
        if re.search('Auto', test):
            pass
        else:
            print(test)

        # print('----')
        # if programsbackup:
        #     countSubNum=countSubNum+1
        #     print('rowid:', str(rowid + 1) + str(countSubNum))
        #     # driver.find_element(By.ID, 'Setup_SubChannel1').click()
        #     print(driver.find_element(By.XPATH, '//td[@id="VideoSize_l_sub1"]').text)
        #     print(driver.find_element(By.XPATH, '//span[@id="OutputURL_HTTP_sub1"]').get_attribute('innerHTML'))
        #     print(driver.find_element(By.XPATH, '//input[@name="TSUDPIP_sub1"]').get_attribute("value"))
        #     print(driver.find_element(By.XPATH, '//input[@name="TSUDPPort_sub1"]').get_attribute("value"))
        # driver.get('http://10.78.64.117/html/encoder/maininfo2.html?referer=1')

    driver.close()
    driver.quit()


