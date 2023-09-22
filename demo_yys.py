from auto_player import Player
# from auto_ocr_player import OCR_Player
import time

# #OCR文字识别  桌面模式（不能遮挡游戏窗口）
# myplayer = OCR_Player(accuracy=0.6, adb_mode=True)
# while True:
# 	myplayer.find_touch(['s挑战', '点击屏幕继续'])
# 	time.sleep(1)

#CV图像匹配  ADB模式（确保设备ADB连接成功）
myplayer = Player(accuracy=0.8, adb_mode=True)
while True:
	myplayer.find_touch(['yys_tiaozhan', 'black','yys_jixu'])
	time.sleep(1)