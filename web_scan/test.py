from bs4 import BeautifulSoup
import re

with open('hongruan2.html') as tagsss:

    soup = BeautifulSoup(tagsss, "html.parser", )
    # print(soup.contents)
    result = [
        soup.find('div', id='356_0').findAll('span', ),
        # soup.find('div', id='iSrcMediaInfoContainer').find('span', attrs={'class': 'media_url'}).get_text(),
        # soup.find('div', id='optional_inputs').find('span', attrs={'class': 'media_url'}).get_text()
    ]
    item = soup.find('div', id='356_0').findAll('span', )[-1]

    a = list(filter(None, re.split('[\n|\t]', item.get_text())))
    print(a)

    # print(item.get_text().strip() )
    # print(result)
b = ['H264', '1920x1080', '@25fps', 'VBR', '3800Kbps ', '    ', 'MP2', '48.0kHz', '2', 'channels', '256', 'Kbps']
c = re.split('x',b[1])
d ,e =c[0],c[1]

print(d,e)