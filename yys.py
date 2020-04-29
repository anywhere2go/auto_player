import cv2,numpy,time,random
import os,sys,pyautogui, traceback
import numpy as np
import mss
import action

# 读取文件 精度控制   显示名字
imgs = action.load_imgs()
pyautogui.PAUSE = 0.1

start_time = time.time()
#print('程序启动，现在时间', time.ctime())


#以上启动，载入设置
##########################################################

def log(f):
    def wrap(*agrs, **kwagrs):
        try:
            ans = f(*agrs, **kwagrs)
            return ans
        except:
            traceback.print_exc()
            time.sleep(60)

    return wrap

@log
def select_mode():
    print('''\n菜单：  鼠标移动到最右侧中止并返回菜单页面,
        1 结界突破
        2 自动御魂通关(司机)
        3 自动御魂通关(打手)
        4 自动御魂通关(单刷)
        5 自动探索副本(司机)
        6 自动探索副本(打手)
        7 自动探索副本(单刷)
        8 百鬼夜行
        9 斗技
        10 当前活动（万事屋）
        11 结界自动合卡，自动选择前三张合成
        12 抽卡
        13 式神升星
        ''')
    action.alarm(1)
    raw = input("选择功能模式：")
    index = int(raw)

    mode = [0, tupo, yuhun, yuhun2, yuhundanren,\
            gouliang, gouliang2, gouliang3,\
            baigui, douji, huodong,\
            card, chouka, shengxing]
    comand = mode[index]
    comand()

##########################################################
#结节突破
def tupo():
    cishu = 0
    while True :   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900)
        a,b = upleft
        c,d = downright
        
        #screen=np.array(ImageGrab.grab().convert('RGB'))
        #screen = screen[b:d,a:c]
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

        #寮突破CD
        want = imgs['liaotupo']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('寮突破')
            if cishu > 6:
                print('等待5分钟CD')
                t = 5*60
                time.sleep(t)
                cishu=0
        elif cishu >= 30:
            print('进攻次数上限')
            select_mode()

        want = imgs['jingonghuise']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            cishu=cishu+7
            print('进攻次数上限:',cishu)
        
        #奖励
        for i in ['jujue','queding',\
                  'shibai','jiangli','jixu',\
                  'jingong','jingong2',\
                  'lingxunzhang','lingxunzhang2','shuaxin']:
            want=imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target=screen
            pts=action.locate(target,want,0)
            if not len(pts)==0:
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(30,80) / 100
                if i == 'shibai':
                    cishu = cishu - 1
                    print('进攻次数：',cishu)
                elif i=='jingong' or i=='jingong2':
                    cishu = cishu + 1
                    print('进攻次数：',cishu)
                    t = random.randint(300,500) / 100
                print('突破中。。。',i)
                time.sleep(t)
                break


########################################################
#御魂司机
def yuhun():
    cishu=0
    while True :
        #鼠标移到最右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900) #上部并排

        a,b = upleft
        c,d = downright

        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

        #print('screen shot ok',time.ctime())
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足: ',pts[0])
            select_mode()

        #确定退出
        want = imgs['queding']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('确定退出')
            xy = action.cheat(pts[0], w, h-10 )
            pyautogui.click(xy)
            t = random.randint(15,30) / 100
            time.sleep(t)
            
        #自动点击通关结束后的页面
        for i in ['jujue','yuhuntiaozhan','liaotianguanbi',\
                  'ying','jiangli','jiangli2','jixu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if i == 'yuhuntiaozhan':
                    cishu = cishu + 1
                    print('挑战次数：',cishu)
                print('挑战中。。。',i)
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(200,300) / 100
                time.sleep(t)
                break
    
########################################################
#御魂打手
def yuhun2():
    cishu=0
    while True :
        #鼠标移到最右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900)

        a,b = upleft
        c,d = downright

        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

        #print('screen shot ok',time.ctime())
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足: ',pts[0])
            select_mode()

        #确定退出
        want = imgs['queding']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('确定退出')
            xy = action.cheat(pts[0], w, h-10 )
            pyautogui.click(xy)
            t = random.randint(15,30) / 100
            time.sleep(t)
            
        #如果队友推出则自己也退出
        want = imgs['kaishizhandou']
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
        for i in ['jujue','querenyuhun','jieshou2','jieshou1',\
                  'jieshou','ying','jiangli','kaishi','jixu',\
                  'shibai']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('挑战中。。。',i)
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(80,150) / 100
                time.sleep(t)
                break
            

########################################################
#御魂单人
def yuhundanren():
    cishu=0
    while True :   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900)

        a,b = upleft
        c,d = downright
        
        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足')
            select_mode()

        #次数检查
        if cishu > 200:
            print('次数上限')
            select_mode()
        
        #过关
        for i in ['jujue','ying','jiangli','tiaozhan','jixu']:
            want=imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target=screen
            pts=action.locate(target,want,0)
            if not len(pts)==0:
                print('挑战中。。。',i)
                if i == 'tiaozhan':
                    cishu=cishu+1
                    print('挑战次数：',cishu)
                for pt in pts:
                    pt = action.cheat(pt, w, h)
                    pyautogui.click(pt)
                    t = random.randint(100,300) / 100
                    time.sleep(t)
                break

########################################################
#探索司机
def gouliang():
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900)
        downright2 = (1280, 720)

        a,b = upleft
        c,d = downright

        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
        #debug
        #cv2.imshow('image',im)
        #return
        ############################
        
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

        x1 = (785, 606)
        x2 = downright
        target = action.cut(screen, x1, x2)
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('正在地图中')
            
            want = imgs['left']
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
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
                    print('点击小怪',i)
                    xx = action.cheat(pts[0], w, h)        
                    pyautogui.click(xx)
                    time.sleep(0.5)
                    break

            if i=='jian' and len(pts)==0:
                for i in ['queren', 'tuichu']:
                    want = imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    x1,x2 = upleft, (965, 522)
                    target = action.cut(screen, x1, x2)
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

        for i in ['jujue','queding','ying','jiangli','jixu','c28','zudui','ditu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
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
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900)
        downright2 = (2550, 900)

        a,b = upleft
        c,d = downright

        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
        
        #设定目标，开始查找
        #进入后
        want = imgs['guding']

        x1 = (785, 606)
        x2 = downright
        target = action.cut(screen, x1, x2)
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('正在地图中')
            
            want = imgs['xiao']
            x1,x2 = (5, 405), (119, 560)
            target = action.cut(screen, x1, x2)
            pts = action.locate(target,want,0)
            
            if not len(pts) == 0:
                print('组队状态中')
            else:
                print('退出重新组队')
                
                for i in ['queren', 'tuichu']:
                    want = imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    x1,x2 = upleft, (965, 522)
                    target = action.cut(screen, x1, x2)
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

        want = imgs['jieshou']
        size = want[0].shape
        h, w , ___ = size
        x1,x2 = upleft, (250, 380)
        target = action.cut(screen, x1, x2)
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('接受组队')
            xx = pts[0]
            xx = action.cheat(xx, w, h)
            if xx[0] > 120:           
                pyautogui.click(xx)
                t = random.randint(40,80) / 100
                time.sleep(t)
            else:
                pass
            continue

        for i in ['jujue','ying','jiangli','jixu','zhunbei']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('领取奖励',i)
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(30,80) / 100
                time.sleep(t)
                break
            
########################################################
#探索单人
def gouliang3():
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900)
        downright2 = (1280, 720)

        a,b = upleft
        c,d = downright

        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
        #debug
        #cv2.imshow('image',im)
        #return
        ############################
        
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

        x1 = (785, 606)
        x2 = downright
        target = action.cut(screen, x1, x2)
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('正在地图中')
            
            want = imgs['left']
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
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
                    print('点击小怪',i)
                    xx = action.cheat(pts[0], w, h)        
                    pyautogui.click(xx)
                    time.sleep(0.5)
                    break

            if i=='jian' and len(pts)==0:
                for i in ['queren', 'tuichu']:
                    want = imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    x1,x2 = upleft, (965, 522)
                    target = action.cut(screen, x1, x2)
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

        for i in ['jujue','tansuo','ying','jiangli','jixu','c28','ditu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('领取奖励',i)
                xy = action.cheat(pts[0], w, h )
                pyautogui.click(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
                break

########################################################
#百鬼
def baigui():
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900)
        downright2 = (1280, 720)

        a,b = upleft
        c,d = downright

        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
        
        #设定目标，开始查找
        #进入后
        want=imgs['inbaigui']
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('正在百鬼中')
            
            want = imgs['blank']
            target = screen
            pts = action.locate(target,want,0)
            if len(pts) == 0:
                #小怪出现！
                print('点击小怪')
                pts2 = (640, 450)
                xx = action.cheat(pts2, 10, 10)        
                pyautogui.click(xx)
                time.sleep(0.5)
                continue

        want = imgs['jinru']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('进入百鬼: ',pts[0])
            xy = action.cheat(pts[0], w, h-10 )
            pyautogui.click(xy)
            pyautogui.moveTo(xy)
            t = random.randint(15,30) / 100
            time.sleep(t)

        want = imgs['kaishi']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('选择界面: ',pts[0])

            want = imgs['ya']
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
                
                xy = action.cheat(pts2, w, h-10 )
                pyautogui.click(xy)
                pyautogui.moveTo(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)

                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                pyautogui.moveTo(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)

        want = imgs['fenxiang']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('结束界面: ',pts[0])
            pts[0]=(1200, 100)
            xy = action.cheat(pts[0], w, h-10 )
            pyautogui.click(xy)
            pyautogui.moveTo(xy)
            t = random.randint(15,30) / 100
            time.sleep(t)

########################################################
#斗技
def douji():
    doujiauto=True
    doujipaidui=0
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900)
        downright2 = (1280, 720)

        a,b = upleft
        c,d = downright

        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

        #判断人机
        want = imgs['shoudong']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('对面是真人，准备退出')
            doujiauto=False
        
        for i in ['jujue','queren','douji','douji2','doujiend','ying',\
                  'doujiqueren','doujiother','duanwei',\
                  'liaotianguanbi','zhunbei','zhunbei2','tui',\
                  'doujiquxiao']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if doujiauto==True and i=='tui':
                    #print('准备退出',i)
                    break
                elif i=='douji':
                    doujipaidui=0
                    doujiauto=True
                    print('斗技开始',i)
                    xy = action.cheat(pts[0], w, h-10 )
                    pyautogui.click(xy)
                    t = random.randint(15,30) / 100
                    time.sleep(t)
                    break
                elif i=='doujiquxiao':
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
                    t = random.randint(15,30) / 100
                    time.sleep(t)
                    break

########################################################
#当前活动
def huodong():
    count=0
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900)
        downright2 = (1280, 720)
        a,b = upleft
        c,d = downright

        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

        #委派任务
        want = imgs['hdchufa']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('出发',i)
            xy = action.cheat(pts[0], w, h-10 )
            pyautogui.click(xy)
            t = random.randint(30,80) / 100
            time.sleep(t)
        
        for i in ['jujue','liaotianguanbi','jiangli','jixu','zhunbei',\
                  'shibai','querenyuhun','hdtouzi',\
                  'hdtiaozhan','hdtiaozhan2',\
                  'hdqueren','huodongjiangli',\
                  'hdtufa','hddiaocha','hdshijian','hdshijian2',\
                  'hdjuexing','hdtijiao',\
                  'hdlingqu','hdqianwang','hdqianwang2']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if i=='hdtiaozhan' or i=='hdtiaozhan2' or i=='hdlingqu':
                    count=count+1
                    print('活动次数：',count)
                print('活动中。。。',i)
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(30,80) / 100
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

##########################################################
#合成结界卡
def card():
    while True:
        #鼠标移到右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900)
        downright2 = (1280, 720)

        a,b = upleft
        c,d = downright

        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

        for i in ['taiyin2','sanshinei','taiyin3']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('结界卡*',i)
                xy = action.cheat(pts[0], w/2, h-10)
                pyautogui.click(xy)
                t = random.randint(30,80) / 100
                time.sleep(t)
                break
        if len(pts) == 0:
                print('结界卡不足')
                select_mode()
        

        for i in range(2):
            #截屏
            monitor = {"top": b, "left": a, "width": c, "height": d}
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
                print('结界卡',i)
                xy = action.cheat(pts[0], w/2, h-10 )
                pyautogui.click(xy)
                pyautogui.moveTo(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)

        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

        want = imgs['hecheng']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('合成中。。。')
            xy = action.cheat(pts[0], w, h-10 )
            pyautogui.click(xy)
            pyautogui.moveTo(xy)
            t = random.randint(15,30) / 100
            time.sleep(t)

        t = random.randint(15,30) / 100
        time.sleep(1)

##########################################################
#抽卡
def chouka():
    while True:
        #鼠标移到右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900)
        downright2 = (1280, 720)

        a,b = upleft
        c,d = downright

        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
        
        for i in ['cezhi','zaicizhaohuan']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('抽卡中。。。')
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                #t = random.randint(1,3) / 100
                #time.sleep(t)
                break

##########################################################
#式神升星
cishu=0
def shengxing():
    while True:
        #鼠标移到右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 900)
        downright2 = (1280, 720)

        a,b = upleft
        c,d = downright

        #截屏
        monitor = {"top": b, "left": a, "width": c, "height": d}
        im = np.array(mss.mss().grab(monitor))
        screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
        
        for i in ['jixushengxing','querenshengxing']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('升星中。。。',i)
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                if i=='querenshengxing':
                    t=random.randint(250,300) / 100
                else:
                    t = random.randint(30,100) / 100
                time.sleep(t)
                break
####################################################
if __name__ == '__main__':
    select_mode()

