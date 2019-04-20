from bs4 import BeautifulSoup
import re

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