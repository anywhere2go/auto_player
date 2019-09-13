import cv2,numpy,time,random
import os,sys,pyautogui, traceback
from PIL import ImageGrab
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
        1 结界自动合卡，自动选择前三张合成 
        2 自动通关魂十，自动接受组队并确认通关
        3 自动通关业原火，单刷
        4 自动刷组队狗粮（打手模式），          
        5 单刷探索副本，无法区分经验BUFF
        6 百鬼夜行
        7 斗技
        8 日轮之塔
        ''')
    action.alarm(1)
    raw = input("选择功能模式：")
    index = int(raw)

    mode = [0, card, yuhun, yeyuanhuo, goliang, solo, baigui, douji, rilun]
    comand = mode[index]
    comand()

##########################################################
#合成结界卡，较简单，未偏移直接点
def card():
    while True:
        #鼠标移到右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.7:
            select_mode()

        screen = ImageGrab.grab()
        screen.save('screen.png')
        screen = cv2.imread('screen.png')

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 768)
        downright2 = (1280, 720)

        a,b = upleft
        c,d = downright
        screen = screen[b:d,a:c]

        want = imgs['taiyin']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if len(pts) == 0:
            select_mode()
        
        x, y, z = (370, 238), (384, 385), (391, 525)  #前三张卡的位置
        zz = (871, 615)               #合成按钮位置
        for i in [x, y, z ,zz]:
            pyautogui.click(i)
            time.sleep(0.1)
        time.sleep(0.5)


########################################################
#魂十通关
def yuhun():
    while True :
        #鼠标移到最右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        screen = ImageGrab.grab()
        screen.save('screen.png')
        screen = cv2.imread('screen.png')

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (2550, 770) #上部并排

        a,b = upleft
        c,d = downright
        screen = screen[b:d,a:c]

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
                
        
        #这里是自动接受组队
        for i in ['jieshou2',"jieshou"]:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            x1,x2 = upleft, (430, 358)
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
                    break
                else:
                    pass
                continue

        #自动点击通关结束后的页面
        for i in ['ying','jiangli','kaishi','jixu' ]:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                for pt in pts:
                    pt = action.cheat(pt, w, h)
                    pyautogui.click(pt)
                    t = random.randint(100,200) / 1000
                    time.sleep(t)
                break
    select_mode()

########################################################
#业原火通关
def yeyuanhuo():
    while True :   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        screen = ImageGrab.grab()
        screen.save('screen.png')
        screen = cv2.imread('screen.png')

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1426, 798)

        a,b = upleft
        c,d = downright
        screen = screen[b:d,a:c]

        print('screen shot ok',time.ctime())
        
        #设定目标，开始查找

        #过关
        for i in ['ying','jiangli','tiaozhan','jixu']:
            want=imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target=screen
            pts=action.locate(target,want,0)
            if not len(pts)==0:
                for pt in pts:
                    pt = action.cheat(pt, w, h)
                    pyautogui.click(pt)
                    t = random.randint(20,50) / 100
                    time.sleep(t)
                break

########################################################
#狗粮通关
def goliang():
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        screen = ImageGrab.grab()
        screen.save('screen.png')
        screen = cv2.imread('screen.png')

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 768)
        downright2 = (2550, 768)

        a,b = upleft
        c,d = downright
        screen = screen[b:d,a:c]

        print('cursor:',pyautogui.position())
        
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
                        print('退出中')
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

        for i in ['ying','jiangli','jixu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('领取奖励')
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
                break

########################################################
#单人探索
def solo():
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        screen = ImageGrab.grab()
        screen.save('screen.png')
        screen = cv2.imread('screen.png')

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 768)
        downright2 = (1280, 720)

        a,b = upleft
        c,d = downright
        screen = screen[b:d,a:c]

        #print('screen shot ok',time.ctime())
        #print(pyautogui.position())
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足: ',pts[0])
            select_mode()


        
        want = imgs['queren']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        x1,x2 = upleft, (965, 522)
        target = action.cut(screen, x1, x2)
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('确认退出: ',pts[1])
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

            want = imgs['jian']
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('点击小怪')
                xx = action.cheat(pts[0], 10, 10)        
                pyautogui.click(xx)
                time.sleep(0.5)
                continue
            else:
                for i in ['queren', 'tuichu']:
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
                        pyautogui.click(queding)
                        t = random.randint(50,80) / 100
                        time.sleep(t)
                        break
                continue

        for i in ['ying','jiangli','jixu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('领取奖励')
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
                break

        want = imgs['tansuo']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('进入地图: ',pts[0])
            xy = action.cheat(pts[0], w, h-10 )
            pyautogui.click(xy)
            pyautogui.moveTo(xy)
            t = random.randint(15,30) / 100
            time.sleep(t)

########################################################
#百鬼
def baigui():
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        screen = ImageGrab.grab()
        screen.save('screen.png')
        screen = cv2.imread('screen.png')

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 768)
        downright2 = (1280, 720)

        a,b = upleft
        c,d = downright
        screen = screen[b:d,a:c]

        #print('screen shot ok',time.ctime())
        #print(pyautogui.position())
        
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
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        screen = ImageGrab.grab()
        screen.save('screen.png')
        screen = cv2.imread('screen.png')

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 768)
        downright2 = (1280, 720)

        a,b = upleft
        c,d = downright
        screen = screen[b:d,a:c]

        for i in ['douji','doujiend','ying','doujiqueren','tui','doujiother']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('领取奖励')
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(15,30) / 100
                time.sleep
                break

########################################################
#
def rilun():
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        screen = ImageGrab.grab()
        screen.save('screen.png')
        screen = cv2.imread('screen.png')

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 768)
        downright2 = (2550, 768)

        a,b = upleft
        c,d = downright
        screen = screen[b:d,a:c]

        #print('cursor:',pyautogui.position())
        
        #设定目标，开始查找
        for i in ['queren','queding','baoxiang','yueliang','ying','jiangli','jixu','zhunbei','xiayiceng','xiayiceng2','danren','yuhunjiacheng','gaoliang','zhunbeirita']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('进行中。。。')
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
                break

####################################################
if __name__ == '__main__':
    select_mode()

