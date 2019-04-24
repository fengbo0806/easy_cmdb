from excelTrigger.readExcel import readExcel
import os
import  time
import re
import datetime

path = os.path.abspath('移动直播2019年.xls')
filename = '移动直播2019年.xls'
# print(path)
obj = readExcel(path, filename)
objDict = obj.typeOfExcel()
# print(objDict)
'''
{0: ('序号', '月份', '日期', '直播时间', '直播名称', '审核频道', '审核', '切换', '点播', '点播单号', '责任人', '对接人', '一级部门', '二级部门', '垫片', '收录地址',
     'CDN推送地址', '拉流地址', '备注', '分类', ''),
 1: (
 1.0, '1月', 43470.0, '11:20-11:50', '2019厦门国际银行东山岛国际半程马拉松赛新闻发布会', '体育08', 1.0, 0.0, 1.0, '20161115-8581', '盖振', '单妍',
 '央视影音事业群', '体育文化中心', '体育品牌宣传片',
 '主：rtmp://live2.maim5.com/live/star?auth_key=1548221187-0-0-b3fdda711a1ca8073de1961f89e4dab8\n备：rtmp://58.215.162.39/wxmlive/xiamen',
 'tiyuip8', 'rtmp://live.videobase.com.cn/live/wxtiyuip8', '右标', '发布会', ''), 2: (
2.0, '1月', 43470.0, '19:15-20:00', '问答亚洲杯 点将阿联酋', '体育01', 1.0, 0.0, 1.0, '20161115-8581', '张静', '张静', '央视影音事业群',
'体育文化中心', '体育品牌宣传片', 'rtmp://59.110.126.141/live/CCTV5b0f53053e2954943bb9c6bbe401396c9H', 'tiyuip1',
'rtmp://live.videobase.com.cn/live/wxtiyuip1', '右标', '亚洲杯', ''), 3: (
3.0, '1月', 43471.0, '7:30-12:00', '2019建发厦门马拉松赛', '体育06', 1.0, 0.0, 1.0, '20161115-8581', '盖振', '李姝宁', '央视影音事业群',
'体育文化中心', '2019厦门马拉松宣传片',
'主：rtmp://live2.maim5.com/live/xmmls1?auth_key=1548219955-0-0-da080d2286f0fd2c97c09638673e9ff1\n备：rtmp://58.215.162.39/wxmlive/xiamen',
'tiyuip6', 'rtmp://live.videobase.com.cn/live/wxtiyuip6', '右标', '马拉松', ''),
 4: (
 4.0, '1月', 43471.0, '10:00-11:00', '快来！2019萌主驾到！', 'LIVE08', 1.0, 0.0, 1.0, '20161207-8903', '郭亚南', '吴婷', '国际传播事业群',
 '熊猫直播专项项目组', '20190106熊猫垫片', '假直播：20190106熊猫录播视频', 'rtmp://newspush.live.wscdns.com/live/guochuan02',
 'rtmp://live.videobase.com.cn/live/ipanda', '左上：熊猫logo标+右下角标：成都大熊猫繁育研究基地；\n右侧：栏目条', '熊猫', ''), 5: (
5.0, '1月', 43471.0, '19:15-20:15', '国足发布会&赛前踩场训练', '体育01', 1.0, 0.0, 1.0, '20161115-8581', '龙志洲', '龙志洲', '央视影音事业群',
'体育文化中心', '体育品牌宣传片', 'rtmp://59.110.126.141/live/CCTV5134158528a1443a8bb22a7154f2070e6M', 'tiyuip1',
'rtmp://live.videobase.com.cn/live/wxtiyuip1', '右标', '亚洲杯', ''), 6: (
6.0, '1月', 43471.0, '20:00-23:00', '舞典华章-中国舞蹈“荷花奖”第11届颁奖盛典', 'LIVE02', 1.0, 0.0, 1.0, '20161207-8903', '兰军', '张御舲',
'微视频工作室', '', '网媒通用垫片',
'rtmp://tv.cdanet.org/wudianhuazhang/live_lud?auth_key=1546864260-0-0-ef7fcb29c74134791f990d154677e458',
'rtmp://newspush.live.wscdns.com/live/cctv_news02', 'rtmp://live.videobase.com.cn/live/wangmeizhibo222', '左标', '颁奖论坛',
''), 7: (
7.0, '1月', 43472.0, '9:30-21:30', '2018体育大生意年度峰会暨颁奖盛典', '体育07', 1.0, 0.0, 1.0, '20161115-8581', '盖振', '单妍', '央视影音事业群',
'体育文化中心', '体育品牌宣传片', 'rtmp://pull.live.jinshan.qiecdn.com/live/sportsmoney190107', 'tiyuip7',
'rtmp://live.videobase.com.cn/live/wxtiyuip7', '右标', '颁奖论坛', ''), 8: (
8.0, '1月', 43472.0, '17:30-19:00', '迎亚洲杯首战 国足赛前严阵以待', '体育01', 1.0, 0.0, 1.0, '20161115-8581', '龙志洲', '龙志洲', '央视影音事业群',
'体育文化中心', '体育品牌宣传片', 'rtmp://59.110.126.141/live/CCTV5232affb5f9e5458abc2a4baee039b1f1H', 'tiyuip1',
'rtmp://live.videobase.com.cn/live/wxtiyuip1', '右标', '亚洲杯', ''), 9: (
9.0, '1月', 43473.0, '14:25-14:45', '国足恢复训练+为国足首战打分', '体育01', 1.0, 0.0, 1.0, '20161115-8581', '臧金国', '臧金国', '央视影音事业群',
'体育文化中心', '体育品牌宣传片', 'rtmp://59.110.126.141/live/CCTV5a74ac729b97340fdb7ba54351057b883H', 'tiyuip1',
'rtmp://live.videobase.com.cn/live/wxtiyuip1', '右标', '亚洲杯', ''), 10: (
10.0, '1月', 43474.0, '8:00-9:00', '跨越现实到未来 从CES看10年后的生活', 'LIVE03', 1.0, 0.0, 0.0, '', '王圳', '王圳', '央视影音事业群',
'央视影音统筹运营中心', '央视网宣传片2018版', 'rtmp://play.news.ghwx.com.cn/live1/channel1',
'rtmp://newspush.live.wscdns.com/live/cctv_cbox01', '', '右标', '财经常规', ''), 11: (
11.0, '1月', 43474.0, '20:55-21:25', '直播：郑智回归 国足次战中场如何搭配', '体育01', 1.0, 0.0, 1.0, '20161115-8581', '张静', '张静', '央视影音事业群',
'体育文化中心', '体育品牌宣传片', 'rtmp://59.110.126.141/live/CCTV5042a02f272fc4b73a8ab22f376d993aeH', 'tiyuip1',
'rtmp://live.videobase.com.cn/live/wxtiyuip1', '右标', '亚洲杯', '')
'''
# print(objDict)
for item in objDict:
    if item == 0:
        continue
    '''
    1月 43471.0 20:00-23:00
舞典华章-中国舞蹈“荷花奖”第11届颁奖盛典 LIVE02 rtmp://tv.cdanet.org/wudianhuazhang/live_lud?auth_key=1546864260-0-0-ef7fcb29c74134791f990d154677e458
1.0 0.0 1.0
    '''
    # print(objDict[item][1], time.localtime(objDict[item][2] + 1546574130.0), objDict[item][3])
    print(re.split('[-——]',objDict[item][3]))
    print(objDict[item][4], objDict[item][5], objDict[item][15])
    print(objDict[item][6], objDict[item][7], objDict[item][8])

    if item > 5:
        break
    # firstsell = re.split('/', objDict[item][0])
    # secondsell = re.split(':', objDict[item][1])
    # thirdsell = re.split('/', objDict[item][2])
    # fourthsell = re.split(':', objDict[item][3])
    # startdate = datetime.datetime(int(firstsell[0]), int(firstsell[1]), int(firstsell[2]), int(secondsell[0]),
    #                               int(secondsell[1]))
    # enddate = datetime.datetime(int(thirdsell[0]), int(thirdsell[1]), int(thirdsell[2]), int(fourthsell[0]),
    #                             int(fourthsell[1]))

# Task.objects.get_or_create(taskName=objDict[item][4])
# Staff.objects.get_or_create(department=objDict[item][8], staffName=objDict[item][9])
# WorkPackage.objects.create(
#     startDate=startdate,
#     endDate=enddate,
#     programName=objDict[item][7],
#     programChannel=objDict[item][8],
#     inPutStream=objDict[item][9],
#     isRecode=objDict[item][10],
#     isLive=objDict[item][11],
#     notes=objDict[item][12],
#     task=Task.objects.get(taskName=objDict[item][4]),
#     adminStaff=Staff.objects.get(department=objDict[item][8], staffName=objDict[item][9]),
# )

print(time.localtime(43474.0 + 1547438126.0))
# print(time.time(2019/1/5))
# print(time.time(datetime.date(9999, 12, 31)))
# print(datetime.date.(datetime.date(2005, 7, 8)))
dt = "2019-01-5 0:0:0"
dt2 = "2019-01-5 0:0:3"

#转换成时间数组
timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
timeArray2 = time.strptime(dt2, "%Y-%m-%d %H:%M:%S")
#转换成时间戳
timestamp = time.mktime(timeArray)
timestamp2 = time.mktime(timeArray2)
print(timestamp-timestamp2)