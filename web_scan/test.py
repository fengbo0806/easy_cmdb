import re

searchHttpout = str(0) + '.*OutputURL_HTTP"]="'
searchUdpout = str(0) + '.*TSUDPIP"]="\d'
searchUdpoutPort = str(0) + '.*TSUDPPort"]=\d'
searchname = 'CCTV5'
with open('test23.html') as ht:
    # print(ht)
    for line in ht:
        for i in re.split(';',line):
            if re.search(searchname, i):
                print(i)
            # print(i)
        # if not line:
    #         break
    #     if re.search(searchname, line):
    #         print(line)
            # print(re.split('[=;]', line)[-2])

'''
channelCGIInfo[0]["OutputURL_HTTP"]="http://10.78.64.117:8088/ts0";
'''
