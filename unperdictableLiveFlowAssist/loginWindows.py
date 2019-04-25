import winrm
f = open(r'\\172.20.215.6\公共文件夹\00000A移动直播1324532&&&……&&为了让你们一眼就看到\移动直播2019年.xls')
f.close()
#
# c = winrm.Session('172.20.215.6', auth=('薛丹', '123456'), transport='ntlm')
# c.run_cmd('ipconfig')