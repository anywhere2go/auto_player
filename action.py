import cv2,time,os,random,sys,mss,copy,subprocess,pyautogui
import numpy
from PIL import ImageGrab

#检测ADB
out=subprocess.run("adb devices",shell=True,capture_output=True,check=False)
out=out.stdout.decode('utf-8')
print(out)
if " device" in out:
    print('监测到ADB设备，默认使用模拟器')
    adb_enable=True
else:
    print('未监测到ADB设备，默认使用桌面版')
    adb_enable=False

#检测系统
if sys.platform=='darwin' and not adb_enable:
    scalar=True
    scaling_factor=1/2
else:
    scalar=False
    scaling_factor=1

#截屏起点
a=0

def screenshot(monitor):
    if adb_enable:
        image_bytes = subprocess.run("adb shell screencap -p",shell=True,stdout=subprocess.PIPE)
        image_bytes = image_bytes.stdout
        #print(image_bytes)
        screen = cv2.imdecode(numpy.fromstring(image_bytes, numpy.uint8),cv2.IMREAD_COLOR)
        #print(screen)
        #print('screen: ',screen.shape[1],screen.shape[0])
        return screen
    
    if scalar:
        #MSS
        sct = mss.mss()
        #{"top": b, "left": a, "width": c, "height": d}
        #shrink monitor to half due to macOS default DPI scaling
        monitor2=copy.deepcopy(monitor)
        monitor2["width"]=int(monitor2["width"]*scaling_factor)
        monitor2["height"]=int(monitor2["height"]*scaling_factor)
        screen=mss.mss().grab(monitor2)
        #mss.tools.to_png(screen.rgb, screen.size, output="screenshot.png")
        screen = numpy.array(screen)
        #print('Screen size: ',screen.shape)
        #MuMu助手默认拉伸4/3倍
        screen = cv2.resize(screen, (int(screen.shape[1]*0.75), int(screen.shape[0]*0.75)),
                            interpolation = cv2.INTER_LINEAR)
        #print('Screen size: ',screen.shape)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
    else:
        screen = numpy.array(mss.mss().grab(monitor))
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
        command="adb shell input tap {0} {1}" .format(x, y)
        #print('Command: ',command)
        subprocess.run(command,shell=True)
    else:
        pyautogui.click(pos)






