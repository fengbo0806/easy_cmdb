from bs4 import BeautifulSoup

with open('arcdetil.html') as tagsss:
    soup = BeautifulSoup(tagsss, "html.parser", )
    # print(soup.contents)
    result = [soup.find('div', id='iSrcMediaInfoContainer').find('span', attrs={'class': 'media_url'}).get_text(),
              soup.find('div', id='optional_inputs').find('span', attrs={'class': 'media_url'}).get_text()]
    print(result)
