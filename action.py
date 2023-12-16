import cv2,time,os,random,sys,mss,copy,subprocess
import numpy
from PIL import ImageGrab

def startup():
    global scalar,adb_enable,adb_path
    #检测ADB
    if sys.platform=='win32':
        print('检测模拟器')
        mumu_path="C:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe"
        ld_path="C:\\leidian\\LDPlayer9\\adb.exe"
        if os.path.isfile(ld_path):
            print('检测到雷电模拟器')
            adb_path=ld_path
        elif os.path.isfile(mumu_path):
            print('检测到MuMu模拟器')
            adb_path=mumu_path
            comm=[adb_path,'connect','127.0.0.1:7555']
            out=subprocess.run(comm,shell=False,capture_output=True,check=False)
            out=out.stdout.decode('utf-8')
            print(out)
        else:
            adb_path=''
            out=''
    else:
        adb_path='adb'

    if len(adb_path)>0:
        comm=[adb_path,'devices']
        #print(comm)
        out=subprocess.run(comm,shell=False,capture_output=True,check=False)
        out=out.stdout.decode('utf-8')
        print(out)
        out=out.splitlines()
    if len(out)>1:
        out=out[1]
    if len(out)>1:
        print('监测到ADB设备，默认使用安卓截图')
        adb_enable=True
        
        screen=screenshot([])
        w=screen.shape[0]
        h=screen.shape[1]
        print('修改成桌面版分辨率')
        if w>=h:
            comm=[adb_path,"shell","wm","size","1136x640"]
            subprocess.run(comm,shell=False)
        elif w<h:
            comm=[adb_path,"shell","wm","size","640x1136"]
            subprocess.run(comm,shell=False)
    else:
        print('未监测到ADB设备，默认使用桌面版')
        adb_enable=False
        import pyautogui
        pyautogui.FAILSAFE=False

    #检测系统
    if sys.platform=='darwin' and not adb_enable:
        scalar=True
        scaling_factor=1/2
    else:
        scalar=False
        scaling_factor=1

    #截屏起点
    a=0

def reset_resolution():
    global adb_enable,adb_path
    if adb_enable:
        print('重置安卓分辨率')
        comm=[adb_path,"shell","wm","size","reset"]
        subprocess.run(comm,shell=False)

def screenshot(monitor):
    global adb_enable,adb_path
    if adb_enable:
        comm=[adb_path,"shell","screencap","-p"]
        image_bytes = subprocess.run(comm,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        image_bytes = image_bytes.stdout
        if sys.platform=='win32':
            #only for Windows, otherwise it will be None
            image_bytes = image_bytes.replace(b'\r\n', b'\n')
        image_bytes = numpy.fromstring(image_bytes, numpy.uint8)
        screen = cv2.imdecode(numpy.fromstring(image_bytes, numpy.uint8),cv2.IMREAD_COLOR)
        #print('screen: ',screen)
        #print('screen size: ',screen.shape[1],screen.shape[0])
        return screen

    with mss.mss() as sct:
        if scalar:
            #MSS
            #{"top": b, "left": a, "width": c, "height": d}
            #shrink monitor to half due to macOS default DPI scaling
            monitor2=copy.deepcopy(monitor)
            monitor2["width"]=int(monitor2["width"]*scaling_factor)
            monitor2["height"]=int(monitor2["height"]*scaling_factor)
            screen=sct.grab(monitor2)
            #mss.tools.to_png(screen.rgb, screen.size, output="screenshot.png")
            screen = numpy.array(screen)
            #print('Screen size: ',screen.shape)
            #MuMu助手默认拉伸4/3倍
            screen = cv2.resize(screen, (int(screen.shape[1]*0.75), int(screen.shape[0]*0.75)),
                                interpolation = cv2.INTER_LINEAR)
            #print('Screen size: ',screen.shape)
            screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
        else:
            screen = numpy.array(sct.grab(monitor))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
        return screen

    
#在背景查找目标图片，并返回查找到的结果坐标列表，target是背景，want是要找目标
def locate(target,want, show=bool(0), msg=bool(0)):
    loc_pos=[]
    want,treshold,c_name=want[0],want[1],want[2]
    result=cv2.matchTemplate(target,want,cv2.TM_CCOEFF_NORMED)
    location=numpy.where(result>=treshold)
    #print(location)

    if msg:  #显示正式寻找目标名称，调试时开启
        print(c_name,'searching... ')

    h,w=want.shape[:-1] #want.shape[:-1]

    n,ex,ey=1,0,0
    for pt in zip(*location[::-1]):    #其实这里经常是空的
        x,y=pt[0]+int(w/2),pt[1]+int(h/2)
        if (x-ex)+(y-ey)<15:  #去掉邻近重复的点
            continue
        ex,ey=x,y

        cv2.circle(target,(x,y),10,(0,0,255),3)

        if msg:
            print(c_name,'we find it !!! ,at',x,y)

        if scalar:
            x,y=int(x*scaling_factor),int(y*scaling_factor)
        else:
            x,y=int(x),int(y)
            
        loc_pos.append([x,y])

    if show:  #在图上显示寻找的结果，调试时开启
        print('Debug: show action.locate')
        cv2.imshow('we get',target)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()

    if len(loc_pos)==0:
        #print(c_name,'not find')
        pass

    return loc_pos


#按【文件内容，匹配精度，名称】格式批量聚聚要查找的目标图片，精度统一为0.95，名称为文件名
def load_imgs():
    global scalar
    mubiao = {}
    if scalar:
        path = os.getcwd() + '/png'
    else:
        path = os.getcwd() + '/png'
    file_list = os.listdir(path)
    for file in file_list:
        name = file.split('.')[0]
        file_path = path + '/' + file
        a = [ cv2.imread(file_path) , 0.95, name]
        mubiao[name] = a

    return mubiao

#蜂鸣报警器，参数n为鸣叫次数
def alarm(n):
    frequency = 1500
    duration = 500

    if os.name=='nt':
        import winsound
        winsound.Beep(frequency, duration)
    else:
        os.system('afplay /System/Library/Sounds/Sosumi.aiff')

#裁剪图片以缩小匹配范围，screen为原图内容，upleft、downright是目标区域的左上角、右下角坐标
def cut(screen,upleft,downright): 

    a,b=upleft
    c,d=downright
    screen=screen[b:d,a:c]

    return screen

#随机偏移坐标，防止游戏的外挂检测。p是原坐标，w、n是目标图像宽高，返回目标范围内的一个随机坐标
def cheat(p, w, h):
    a,b = p
    if scalar:
        w, h = int(w/3/2), int(h/3/2)
    else:
        w, h = int(w/3), int(h/3)
    if h<0:
        h=1
    c,d = random.randint(-w, w),random.randint(-h, h)
    e,f = a + c, b + d
    y = [e, f]
    return(y)

# 点击屏幕，参数pos为目标坐标
def touch(pos):
    global adb_enable
    #print(adb_enable)
    x, y = pos
    if adb_enable:
        comm=[adb_path,"shell","input","tap",str(x),str(y)]
        #print('Command: ',comm)
        subprocess.run(comm,shell=False)
    else:
        pyautogui.click(pos)






