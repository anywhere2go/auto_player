import cv2,numpy,time, os, random, subprocess
from winsound import Beep

#ADB命令手机截屏，并发送到当前目录,opencv读取文件并返回
def screen_shot(): 
    a = "adb shell screencap -p /data/data/screen.jpg"
    b = "adb pull /data/data/screen.jpg"

    command_list = [a, b]
    for i in command_list:
        os.system(i)

    screen=cv2.imread('screen.jpg')
    return screen

# ADB命令点击屏幕，参数pos为目标坐标
def touch(pos):
    x, y = pos
    a = "adb shell input touchscreen tap {0} {1}" .format(x, y)
    os.system(a)

#蜂鸣报警器，参数n为鸣叫资料
def alarm(n):
    frequency = 1500
    last = 500

    for n in range(n):   
        Beep(frequency,last)
        time.sleep(0.05)

#按【文件内容，匹配精度，名称】格式批量读取要查找的目标图片，精度统一为0.85，名称为文件名
def load_imgs():
    mubiao = {}
    path = os.getcwd() + '/jpg'
    file_list = os.listdir(path)

    for file in file_list:
        name = file.split('.')[0]
        file_path = path + '/' + file
        a = [ cv2.imread(file_path) , 0.85, name]
        mubiao[name] = a

    return mubiao

 #在背景查找目标图片，以列表形式返回查找目标的中心坐标，
 #screen是截屏图片，want是找的图片【按上面load_imgs的格式】，show是否以图片形式显示匹配结果【调试用】
def locate(screen, want, show=0):
    loc_pos = []
    want, treshold, c_name = want[0], want[1], want[2]
    result = cv2.matchTemplate(screen, want, cv2.TM_CCOEFF_NORMED)
    location = numpy.where(result >= treshold)

    h,w = want.shape[:-1] 

    n,ex,ey = 1,0,0
    for pt in zip(*location[::-1]):   
        x,y = pt[0] + int(w/2), pt[1] + int(h/2)
        if (x-ex) + (y-ey) < 15:  #去掉邻近重复的点
            continue
        ex,ey = x,y

        cv2.circle(screen, (x, y), 10, (0, 0, 255), 3)
            
        x,y = int(x), int(y)
        loc_pos.append([x, y])

    if show:  #在图上显示寻找的结果，调试时开启
        cv2.imshow('we get', screen)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()

    if len(loc_pos) == 0:
        print(c_name, 'not found')

    return loc_pos

#裁剪图片以缩小匹配范围，screen为原图内容，upleft、downright是目标区域的左上角、右下角坐标
def cut(screen, upleft, downright): 

    a,b = upleft
    c,d = downright
    screen = screen[b:d,a:c]

    return screen

#随机偏移坐标，防止游戏的外挂检测。p是原坐标，w、n是目标图像宽高，返回目标范围内的一个随机坐标
def cheat(p, w, h):
    a,b = p
    w, h = int(w/3), int(h/3)
    c,d = random.randint(-w, w),random.randint(-h, h)
    e,f = a + c, b + d
    y = [e, f]
    return(y)

#随机延迟，防止游戏外挂检测，延迟时间范围为【x, y】秒之间
def wait(x, y):
    t = random.uniform(x, y)
    time.sleep(t)


