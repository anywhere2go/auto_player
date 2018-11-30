import cv2, time, random, os
import action

debug_mode = 0

# 读取文件
imgs = action.load_imgs()

os.system("adb devices")
start_time = time.time()
print('程序启动，现在时间', time.ctime())
print('菜单：1 结界自动合卡，2 自动通关魂十，3 自动通关业原火，4 自动刷组队狗粮（打手模式） ')
#以上启动，载入设置

##########################################################
if debug_mode:
    mode = debug_mode
else:
    raw = input("选择功能模式：")
    mode = int(raw)

action.alarm(1)
print("开始运行")

##########################################################
#合成结界卡，较简单，未偏移直接点
while mode == 1:
    x, y, z = (370, 238), (384, 385), (391, 525)  #前三张卡的位置
    zz = (871, 615)               #合成按钮位置
    for i in [x, y, z ,zz]:
        action.touch(i)
        time.sleep(0.1)
    time.sleep(0.2)

########################################################
#魂十通关
while mode == 2 :   
    screen = action.screen_shot()
    
    print('screen shot ok',time.ctime())
    
    #设定目标，开始查找
    #自动点击通关结束后的页面
    for i in ['ying','jiangli','kaishi','jixu' ,'zhunbei']:
        want = imgs[i]
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target, want, 0)
        if not len(pts) == 0:
            for pt in pts:
                pt = action.cheat(pt, w, h)
                action.touch(pt)
            break

########################################################
#业原火通关
while mode == 3 :   #直到取消，或者出错
    screen = action.screen_shot()

    print('screen shot ok',time.ctime())
    
    #设定目标，开始查找

    #过关
    for i in ['ying','jiangli','tiaozhan','jixu']:
        want = imgs[i]
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts=action.locate(target, want, 0)
        if not len(pts)==0:
            pt = pt[0]
            pt = action.cheat(pt, w, h)
            action.touch(pt)
            break


########################################################
#狗粮通关
while mode == 4:   #直到取消，或者出错
    screen = action.screen_shot()

    #截屏，并裁剪以加速
    upleft=(0, 0)
    downright=(1358, 768)
    downright2=(2550, 768)

    print('screen shot ok',time.ctime())
    
    #设定目标，开始查找
    #进入地图后
    want=imgs['guding'] #固定阵容，即在地图中

    x1 = (785, 606)
    x2 = downright
    target = action.cut(screen, x1, x2)
    pts = action.locate(target,want,0)
    if not len(pts) == 0:
        print('正在地图中')
        
        want = imgs['xiao']  #笑脸表情，表示在组队状态中
        x1,x2 = (5, 405), (119, 560)
        target = action.cut(screen, x1, x2)
        pts = action.locate(target, want, 0)
        if not len(pts) == 0:
            print('组队状态中')
        else:
            print('退出重新组队')
            
            for i in ['queren', 'tuichu']: #否，即队友已退出，跟随退出重新组队
                want = imgs[i]
                size = want[0].shape
                h, w , ___ = size
                x1,x2 = upleft, (965, 522)
                target = action.cut(screen, x1, x2)
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    print('退出中')
                    try:
                        queding = pts[1]
                    except:
                        queding = pts[0]
                    queding = action.cheat(queding, w, h)
                    action.touch(queding)
                    break
            continue

    #不在地图中，接受组队
    want = imgs['jieshou']
    size = want[0].shape
    h, w , ___ = size
    x1,x2 = upleft, (250, 380)
    target = action.cut(screen, x1, x2)
    pts = action.locate(target,want, 0)
    if not len(pts) == 0:
        print('接受组队')
        xx = pts[0]
        xx = action.cheat(xx, w, h)
        if xx[0] > 120:           
            action.touch(xx)
        else:
            pass
        continue

    #确认通关
    for i in ['ying','jiangli','jixu']:
        want = imgs[i]
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('领取奖励')
            xy = action.cheat(pts[0], w, h-10 )
            action.touch(xy)
            break
    
    #定时器，建议每次隔60分钟提醒一次，不要一次连续刷太久
    now_time = time.time()
    if now_time - start_time > 60 * 60:  #默认60分钟
        start_time = now_time
        action.alarm(10)

