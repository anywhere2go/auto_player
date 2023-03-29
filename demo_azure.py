from auto_ocr_player import OCR_Player
import time

myplayer = OCR_Player(accuracy=0.6, adb_mode=True)

tuiyi = ['键退', '确定', '点击继续', '没找到符合条件']
zhuxian = ['立刻前往', '再次前往', 's整理', '迎击']
huodong = ['刻前',  '北地', '出击', '战斗胜利', '确定']
yanxi = ["次数不足", '关闭', '开始', '综合实力', '出击', "评价", "功勋", "确定",]

steps = zhuxian
yx, bd = myplayer.exist(['演习', '北地'])
if yx:
	steps = yanxi
elif bd:
	steps = huodong

while 1:
    re = myplayer.find_touch(steps)
    if re == '次数不足':
        break
    if re == '整理':
    	while myplayer.find_touch(tuiyi) != '没找到符合条件':
    		time.sleep(1)
    	myplayer.find_touch(['取消',])
    if re == '迎击':
    	myplayer.find_touch(['自律',])
    	time.sleep(3)
    time.sleep(1)
