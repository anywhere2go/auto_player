import cv2,time,random,os, datetime
import os,sys,pyautogui, traceback
import numpy as np
import mss
import action

#检测系统
print('操作系统:', sys.platform)
if sys.platform=='darwin':
    scalar=True
else:
    scalar=False

# 读取文件 精度控制   显示名字
imgs = action.load_imgs()
#pyautogui.PAUSE = 0.05
pyautogui.FAILSAFE=False

start_time = time.time()
#print('程序启动，现在时间', time.ctime())

#截屏，并裁剪以加速
upleft = (0, 0)
if scalar==True:
    downright = (1136,700)
else:
    downright = (1200, 700)
a,b = upleft
c,d = downright
monitor = {"top": b, "left": a, "width": c, "height": d}
start = time.time()

#constants
last_click=None

#以上启动，载入设置
##########################################################
def select_mode():
    global start
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("运行时间：{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
    print (datetime.datetime.now())

    print('''\n菜单：  鼠标移动到最右侧中止并返回菜单页面，0退出
        1 结界突破
        2 御魂(司机)
        3 御魂(打手)
        4 御魂(单刷)
        5 探索(司机)
        6 探索(打手)
        7 探索(单刷)
        8 百鬼夜行
        9 自动斗技
        10 当前活动
        11 结界自动合卡（太阴和伞室内）
        12 厕纸抽卡
        13 蓝蛋升级
        14 秘境召唤
        15 妖气封印和秘闻
        16 契灵（单刷）
        17 Debug模式
        ''')
    action.alarm(1)
    raw = input("选择功能模式：")
    try:
        index = int(raw)
    except:
        print('请输入数字')
        select_mode()

    mode = [0, tupo, yuhun, yuhun2, yuhundanren,\
            gouliang, gouliang2, gouliang3,\
            baigui, douji, huodong,\
            card, chouka, shengxing, mijing, yaoqi,\
            qilingdanren, debug]
    try:
        command = mode[index]
    except:
        print('数字超出范围')
        select_mode()

    if index==0:
        quit()
    else:
        start = time.time()
        command()

##########################################################
#结节突破
def tupo():
    global last_click
    count=0 #总次数
    cishu = 0
    refresh=0
    liaotu=None
    while True :   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        #im = np.array(mss.mss().grab(monitor))
        #screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
        #print(scalar)
        screen=action.screenshot(monitor)
        
        #cv2.imshow("Image", screen)
        #cv2.waitKey(0)

        #寮突破判断
        if liaotu==None:
            want = imgs['liaotupo']
            size = want[0].shape
            h, w , ___ = size
            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                liaotu=True
                print('寮突破')

            want = imgs['gerentupo']
            size = want[0].shape
            h, w , ___ = size
            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                liaotu=False
                print('个人突破')

            
        if liaotu==False:
            if cishu >= 31:
                print('进攻次数上限')
                select_mode()

        want = imgs['jingonghuise']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0 and liaotu==True:
            refresh=refresh+1
            print('进攻CD，暂停5分钟')
            t=60*5
            time.sleep(t)
        
        #奖励
        for i in ['jujue','queding',\
                  'shibai','ying','jiangli','jixu',\
                  'jingong','jingong2',\
                  'lingxunzhang','lingxunzhang2','lingxunzhang4',\
                  'shuaxin','zhunbei']:
            #print(i)
            want=imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target=screen
            pts=action.locate(target,want,0)
            if not len(pts)==0:
                if last_click==i:
                    if i=='jingong' or i=='jingong2':
                        refresh=refresh+7
                    else:
                        refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(15,50) / 100
                if i == 'shibai':
                    if cishu>0:
                        cishu = cishu - 1
                    if count>0:
                        count = count - 1
                    print('进攻总次数：',count)
                    t = random.randint(50,100) / 100
                elif i=='jingong' or i=='jingong2':
                    if refresh==0:
                        cishu = cishu + 1
                        count=count+1
                    print('进攻总次数：',count)
                    t = random.randint(500,800) / 100
                elif i=='lingxunzhang' or i=='lingxunzhang2' or i=='lingxunzhang4':
                    print('选择结界。。。',i)
                    t = random.randint(50,150) / 100
                else:
                    print('突破中。。。',i)
                time.sleep(t)
                break


########################################################
#御魂司机
def yuhun():
    global last_click
    cishu=0
    refresh=0
    while True :
        #鼠标移到最右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)
        
        #print('screen shot ok',time.ctime())
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足')
            select_mode()

        #自动点击通关结束后的页面
        for i in ['jujue','tiaozhan','tiaozhan2',\
                  'moren','queding','querenyuhun','ying','jiangli',\
                  'jixu','shibai']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                elif i=='querenyuhun':
                    refresh=refresh+2
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                if i == 'tiaozhan' or i=='tiaozhan2':
                    if refresh==0:
                        cishu=cishu+1
                    print('挑战次数：',cishu)
                    t = random.randint(50,150) / 100
                else:
                    print('挑战中。。。',i)
                    t = random.randint(50,100) / 100
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                time.sleep(t)
                break
    
########################################################
#御魂打手
def yuhun2():
    global last_click
    cishu=0
    refresh=0
    while True :
        #鼠标移到最右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足')
            select_mode()

        #如果队友推出则自己也退出
        want = imgs['tiaozhanhuise']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('队友已退出')
            want = imgs['likaiduiwu']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
                
        
        #自动点击通关结束后的页面
        for i in ['jujue','moren','queding','querenyuhun',\
                  'ying','jiangli','jixu',\
                  'jieshou2','jieshou','shibai']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                elif i=='querenyuhun':
                    refresh=refresh+2
                else:
                    refresh=0
                
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                elif refresh==0 and i=='jiangli' and not last_click=='querenyuhun':
                    #print('last',last_click)
                    cishu=cishu+1
                    print('挑战次数：',cishu)
                print('挑战中。。。',i)
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                last_click=i
                t = random.randint(15,30) / 100
                time.sleep(t)
                break
            

########################################################
#御魂单人
def yuhundanren():
    global last_click
    cishu=0
    refresh=0
    while True :   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足')
            select_mode()

        for i in ['jujue','querenyuhun','ying','jiangli','jixu',\
                  'tiaozhan','tiaozhan2','tiaozhan3','tancha','shibai']:
            want=imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target=screen
            pts=action.locate(target,want,0)
            if not len(pts)==0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                print('挑战中。。。',i)
                if i == 'tiaozhan' or i=='tiaozhan2' or i=='tiaozhan3' or i=='tancha':
                    if refresh==0:
                        cishu=cishu+1
                    print('挑战次数：',cishu)
                    t = random.randint(150,300) / 100
                else:
                    t = random.randint(15,30) / 100
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                time.sleep(t)
                break

########################################################
#探索司机
def gouliang():
    global last_click
    count=0
    refresh=0
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)

        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足 ')
            select_mode()

        want = imgs['queren']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('确认退出')
            try:
                queding = pts[1]
            except:
                queding = pts[0]
            xy = action.cheat(queding, w, h)
            pyautogui.click(xy)
            pyautogui.moveTo(xy)
            t = random.randint(15,30) / 100
            time.sleep(t)

        
        #设定目标，开始查找
        #进入后
        want=imgs['guding']

        #x1 = (785, 606)
        #x2 = downright
        #target = action.cut(screen, x1, x2)
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('正在地图中')
            
            want = imgs['left']
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if scalar:
                    right=(854/2, 528/2)
                else:
                    right = (854, 527)
                right = action.cheat(right, 10, 10)
                pyautogui.click(right)
                t = random.randint(50,80) / 100
                time.sleep(t)
                continue

            for i in ['boss', 'jian']:
                want = imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #print('重复次数：',refresh)
                    if refresh>6:
                        print('进攻次数上限')
                        select_mode()
                    
                    if refresh==0:
                        count=count+1
                    print('点击小怪',i)
                    print('探索次数：',count)
                    xx = action.cheat(pts[0], w, h)        
                    pyautogui.click(xx)
                    time.sleep(0.5)
                    break

            if i=='jian' and len(pts)==0:
                for i in ['queren', 'tuichu']:
                    want = imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    #x1,x2 = upleft, (965, 522)
                    #target = action.cut(screen, x1, x2)
                    target = screen
                    pts = action.locate(target,want,0)
                    if not len(pts) == 0:
                        print('退出中',i)
                        try:
                            queding = pts[1]
                        except:
                            queding = pts[0]
                        queding = action.cheat(queding, w, h)
                        pyautogui.click(queding)
                        t = random.randint(50,80) / 100
                        time.sleep(t)
                        break
                continue

        for i in ['jujue','queding','ying','querenyuhun',\
                  'jiangli','jixu',\
                  'tiaozhan','ditu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                    
                print('领取奖励',i)
                xy = action.cheat(pts[0], w, h )
                pyautogui.click(xy)
                if i=='queding':
                    t = random.randint(150,200) / 100
                else:
                    t = random.randint(15,30) / 100
                time.sleep(t)
                break

########################################################
#探索打手
def gouliang2():
    global last_click
    refresh=0
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足 ')
            select_mode()
        
        #进入后
        want = imgs['guding']
        pts = action.locate(screen,want,0)
        if not len(pts) == 0:
            print('正在地图中')
            
            want = imgs['xiao']
            pts = action.locate(screen,want,0)
            
            if not len(pts) == 0:
                print('组队状态中')
            else:
                print('退出重新组队')
                
                for i in ['queren', 'queren2','tuichu']:
                    want = imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    pts = action.locate(screen,want,0)
                    
                    if not len(pts) == 0:
                        if last_click==i:
                            refresh=refresh+1
                        else:
                            refresh=0
                        last_click=i
                        #print('重复次数：',refresh)
                        if refresh>6:
                            print('进攻次数上限')
                            select_mode()
                        
                        print('退出中',i)
                        try:
                            queding = pts[1]
                        except:
                            queding = pts[0]
                        queding = action.cheat(queding, w, h)
                        pyautogui.click(queding)
                        t = random.randint(50,80) / 100
                        time.sleep(t)
                        break
                continue

        for i in ['jujue','jieshou','querenyuhun','ying',\
                  'jiangli','jixu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if i=='jieshou':
                    a,b=pts[0]
                    if a<50:
                        break
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                    
                print('领取奖励',i)
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                if i=='jieshou' or i=='jieshou1':
                    t = random.randint(15,30) / 100
                else:
                    t = random.randint(15,30) / 100
                time.sleep(t)
                break
            
########################################################
#探索单人
def gouliang3():
    global last_click
    count=0
    refresh=0
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足 ')
            select_mode()

        want = imgs['queren']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        #x1,x2 = upleft, (965, 522)
        #target = action.cut(screen, x1, x2)
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('确认退出')
            try:
                queding = pts[1]
            except:
                queding = pts[0]
            xy = action.cheat(queding, w, h)
            pyautogui.click(xy)
            pyautogui.moveTo(xy)
            t = random.randint(15,30) / 100
            time.sleep(t)

        
        #设定目标，开始查找
        #进入后
        want=imgs['guding']

        #x1 = (785, 606)
        #x2 = downright
        #target = action.cut(screen, x1, x2)
        pts = action.locate(screen,want,0)
        if not len(pts) == 0:
            print('正在地图中')
            
            want = imgs['left']
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if scalar:
                    right=(854/2, 528/2)
                else:
                    right = (854, 527)
                right = action.cheat(right, 10, 10)
                pyautogui.click(right)
                t = random.randint(50,80) / 100
                time.sleep(t)
                continue

            for i in ['boss', 'jian']:
                want = imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #print('重复次数：',refresh)
                    if refresh>6:
                        print('进攻次数上限')
                        select_mode()
                    
                    if refresh==0:
                        count=count+1
                    print('点击小怪',i)
                    print('探索次数：',count)
                    if count>500:
                        print('次数上限')
                        select_mode()
                    xx = action.cheat(pts[0], w, h)        
                    pyautogui.click(xx)
                    time.sleep(0.5)
                    break

            if len(pts)==0:
                for i in ['queren','queren2','tuichu']:
                    want = imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    pts = action.locate(screen,want,0)
                    if not len(pts) == 0:
                        if last_click==i:
                            refresh=refresh+1
                        else:
                            refresh=0
                        last_click=i
                        #print('重复次数：',refresh)
                        if refresh>6:
                            print('进攻次数上限')
                            select_mode()
                    
                        print('退出中',i)
                        try:
                            queding = pts[1]
                        except:
                            queding = pts[0]
                        queding = action.cheat(queding, w, h)
                        pyautogui.click(queding)
                        t = random.randint(50,80) / 100
                        time.sleep(t)
                        break
                continue

        for i in ['jujue','querenyuhun',\
                  'tansuo','ying','jiangli','jixu','c28','ditu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                print('领取奖励',i)
                xy = action.cheat(pts[0], w, h )
                pyautogui.click(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
                break

########################################################
#百鬼
def baigui():
    global last_click
    refresh=0
    cishu=0
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)

        #设定目标，开始查找
        #进入后
        for i in ['baigui','gailv','douzihuoqu','miaozhun','baiguijieshu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                refresh=0
                print('点击',i)
                xy = action.cheat(pts[0], w, h )
                pyautogui.click(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
                continue

        want=imgs['inbaigui']
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            #print('正在百鬼中')
            want = imgs['blank']
            target = screen
            pts = action.locate(target,want,0)
            if len(pts) == 0:
                refresh=0
                #小怪出现！
                print('点击小怪')
                pts2 = (640, 450)
                xx = action.cheat(pts2, 100, 80)        
                pyautogui.click(xx)
                time.sleep(0.5)
                continue

        i='jinru'
        want = imgs[i]
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            if last_click==i:
                refresh=refresh+1
            else:
                refresh=0
                last_click=i
            print('重复次数：',refresh)
            if refresh>6:
                print('进攻次数上限')
                select_mode()
            cishu=cishu+1
            print('进入百鬼:',cishu)
            xy = action.cheat(pts[0], w, h-10 )
            pyautogui.click(xy)
            pyautogui.moveTo(xy)
            t = random.randint(10,20) / 100
            time.sleep(t)

        

        i='kaishi'
        want = imgs[i]
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            refresh=0
            print('选择押注界面')
            i='ya'
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts2 = action.locate(target,want,0)
            if not len(pts2) == 0:
                print('点击开始: ',pts[0])
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                pyautogui.moveTo(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
            else:
                #选择押注
                index=random.randint(0,2)
                pts2 = (300+index*340, 500)
                print('选择押注: ',index)
                
                xy = action.cheat(pts2, w, h-10 )
                pyautogui.click(xy)
                pyautogui.moveTo(xy)
                t = random.randint(50,100) / 100
                time.sleep(t)

                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                pyautogui.moveTo(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)


########################################################
#斗技
def douji():
    global last_click
    doujipaidui=0
    refresh=0
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()
        #截屏
        screen=action.screenshot(monitor)
        
        for i in ['jujue','shoudong','zidong','queren',\
                  'douji','douji3','douji4',\
                  'doujiqueren','doujiend','ying','jixu',\
                  'zhunbei','zhunbei2',\
                  'doujiquxiao']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                    
                if i=='douji' or i=='douji4':
                    doujipaidui=0
                    print('斗技开始',i)
                    xy = action.cheat(pts[0], w, h-10 )
                    pyautogui.click(xy)
                    t = random.randint(15,30) / 100
                    time.sleep(t)
                    break
                elif i=='doujiquxiao':
                    refresh=0
                    doujipaidui=doujipaidui+1
                    print('斗技搜索:',doujipaidui)
                    if doujipaidui>5:
                        doujipaidui=0
                        print('取消搜索')
                        xy = action.cheat(pts[0], w, h-10 )
                        pyautogui.click(xy)
                        t = random.randint(15,30) / 100
                        time.sleep(t)
                        break
                else:
                    print('斗技中。。。',i)
                    xy = action.cheat(pts[0], w, h-10 )
                    pyautogui.click(xy)
                    t = random.randint(50,100) / 100
                    time.sleep(t)
                    break

########################################################
#当前活动
def huodong():
    global last_click
    count=0
    refresh=0
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)

        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足 ')
            select_mode()
        
        for i in ['jujue','querenyuhun','queding',\
                  'hdtiaozhan','ying',\
                  'shibai','jixu','hdend','liaotianguanbi']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if i=='hdjiacheng':
                    refresh=0
                elif last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                print('活动中',i)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()

                t = 0
                if i=='hdtiaozhan':
                    if refresh==0:
                        count=count+1
                    print('挑战次数：',count)
                    if count>20:
                        select_mode()
                    t=1
                if i=='hdfaxian' or i=='hdfaxian2':
                    t=5
                #if i=='hdend':
                #    if refresh==0:
                #        print('疲劳度满，休息10分钟')
                        #t = 10*60
                        #time.sleep(t)
                xy = action.cheat(pts[0], w, h)
                pyautogui.click(xy)
                time.sleep(t)

##########################################################
#合成结界卡
def card():
    global last_click
    refresh=0
    while True:
        #鼠标移到右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)
        
        for i in ['taiyin2','sanshinei','taiyin3']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                print('结界卡*',i)
                xy = action.cheat(pts[0], w/2, h-10)
                pyautogui.click(xy)
                break
        if len(pts) == 0:
                print('结界卡不足')
                select_mode()
        

        for i in range(2):
            #截屏
            im = np.array(mss.mss().grab(monitor))
            screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

            want = imgs['taiyin']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if len(pts) == 0:
                print('结界卡不足')
                select_mode()
            else:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click='taiyin'
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                print('结界卡',i)
                xy = action.cheat(pts[0], w/2, h-10 )
                pyautogui.click(xy)
                pyautogui.moveTo(xy)

        #截屏
        screen=action.screenshot(monitor)

        want = imgs['hecheng']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            if last_click==i:
                refresh=refresh+1
            else:
                refresh=0
            last_click='hecheng'
            #print('重复次数：',refresh)
            if refresh>6:
                print('进攻次数上限')
                select_mode()
            
            print('合成中。。。')
            xy = action.cheat(pts[0], w, h-10 )
            pyautogui.click(xy)
            pyautogui.moveTo(xy)

        time.sleep(1)

##########################################################
#抽卡
def chouka():
    global last_click
    count=0
    while True:
        #鼠标移到右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)
        
        want = imgs['zaicizhaohuan']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            if count>200:
                print('次数上限')
                select_mode()
            count=count+1
            print('抽卡中。。。',count)
            xy = action.cheat(pts[0], w, h-10 )
            pyautogui.click(xy)
            #t = random.randint(1,3) / 100
            #time.sleep(t)

##########################################################
#蓝蛋升级
def shengxing():
    global last_click
    count=0
    refresh=0
    while True:
        #鼠标移到右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)
            
        for i in ['jineng','jixushengxing',\
                  'jixuyucheng','querenshengxing']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                print('升级中。。。',i)
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                if i=='querenshengxing':
                    if refresh==0:
                        count=count+1
                    print('升级个数：',count)
                    t = random.randint(250,350) / 100
                else:
                    t = random.randint(20,100) / 100
                    
                time.sleep(t)
                
##########################################################
#秘境召唤
def mijing():
    global last_click
    refresh=0
    while True:
        #鼠标移到右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)
        
        #检测聊天界面
        want = imgs['liaotianguanbi']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            #print('搜索秘境车中。。。')

            for i in ['jujue','mijingzhaohuan','mijingzhaohuan2']:
                want = imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #print('重复次数：',refresh)
                    if refresh>6:
                        print('进攻次数上限')
                        select_mode()
                    
                    print('秘境召唤。。。',i)
                    xy = action.cheat(pts[0], w, h-10 )
                    pyautogui.click(xy)
                    #t = random.randint(10,100) / 100
                    #time.sleep(t)
                    break
        else:
            for i in ['jujue','canjia','liaotian']:
                want = imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #print('重复次数：',refresh)
                    if refresh>6:
                        print('进攻次数上限')
                        select_mode()
                    
                    if i=='canjia':
                        print('加入秘境召唤！',i)
                    xy = action.cheat(pts[0], w, h-10 )
                    pyautogui.click(xy)
                    t = random.randint(10,30) / 100
                    time.sleep(t)
                    break

########################################################
#妖气封印和秘闻
def yaoqi():
    global last_click
    count=0
    refresh=0
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)
        
        #委派任务
        for i in ['jujue','jiangli','jixu','zhunbei',\
                  'shibai','zidongpipei','zudui2',\
                  'ying','tiaozhan3','tiaozhan4']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                    
                if i=='zidongpipei' or i=='tiaozhan3' or i=='tiaozhan4':
                    if refresh==0:
                        count=count+1
                    print('次数：',count)
                    t=100/100
                elif i=='shibai':
                    print('自动结束')
                    select_mode()
                else:
                    print('活动中。。。',i)
                    t = random.randint(30,80) / 100
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                time.sleep(t)
                break
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足')
            select_mode()

########################################################
#契灵单人
def qilingdanren():
    global last_click
    cishu=0
    refresh=0
    while True :   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏
        screen=action.screenshot(monitor)
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足')
            select_mode()

        for i in ['jujue','ying','jiangli','jixu',\
                  'qiling1','mingqi','queren3',\
                  'tiaozhan5','shibai','xiaozhiren']:
            want=imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target=screen
            pts=action.locate(target,want,0)
            if not len(pts)==0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                print('挑战中。。。',i)
                if i=='tancha' or i=='tiaozhan5':
                    if refresh==0:
                        cishu=cishu+1
                    print('挑战次数：',cishu)
                    t = random.randint(50,150) / 100
                elif i=='queren3':
                    t = random.randint(350,450) / 100
                else:
                    t = random.randint(15,30) / 100
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                time.sleep(t)
                break


##################################################################
def debug():
    #截屏
    screen=action.screenshot(monitor)
    cv2.imshow("Image", screen)
    print('点击截图，按任意键返回')
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    select_mode()
####################################################
if __name__ == '__main__':
    select_mode()

