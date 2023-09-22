import time, os, random, threading
import cv2, numpy, pyautogui
from PIL import ImageGrab

#桌面模式下的鼠标操作延迟，程序已经设置随机延迟这里无需设置修改
pyautogui.PAUSE = 0.001
cwd = __file__.replace('auto_player.py', '')  #当前文件目录
wanted_path = f'{cwd}\\wanted'      #目标图片目录
#上面都不用改，下面是adb.exe文件所在路径要改，
#如果你已经加入系统PATH环境，就直接adb = 'adb',我的没加。 只用桌面模式话不用管
adb = 'D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe' #ADB文件路径
nxfd = 'C:\\Users\\Administrator\\Nox_share\\ImageShare' #模拟器共享文件路径

class Player(object):
    """docstring for Player"""
       # accuracy 匹配精准度 0~1 #adb_mode开启ADB模式  #adb_num连接第几台ADB设备
    def __init__(self, accuracy=0.8, adb_mode=True, adb_num=16384):
        super(Player, self).__init__()
        self.accuracy = accuracy  
        self.adb_mode = adb_mode  
        self.load_target()  
        if self.adb_mode:
            re = os.popen(f'{adb} devices').read()
            print(re)
            device_list = [e.split('\t')[0] for e in re.split('\n') if '\tdevice' in e]
            assert len(device_list) <= 1, '未检测到ADB连接设备'
            self.device = device_list[adb_num] 
            re = os.popen(f'{adb} -s {self.device} shell wm size').read()
            print(re)
        else:
            w, h = pyautogui.size()
            print(f'Physical size: {w}x{h}')

    #读取要查找的目标图片，名称为文件名
    #返回字典{name1:[cv2_image1, name1], name2:...}
    def load_target(self):
        target_map = {}
        path = wanted_path
        file_list = os.listdir(path)
        for file in file_list:
            name = file.split('.')[0]
            file_path = path + '/' + file
            content = [ cv2.imread(file_path) , name]
            target_map[name] = content
        print(target_map.keys())
        self.target_map = target_map
        return target_map

    #截屏并发送到目录./screen, 默认返回cv2读取后的图片
    def screen_shot(self, name='screen'):
        if self.adb_mode:         
            a = f'{adb} -s {self.device} shell screencap -p sdcard/Pictures/{name}.jpg'
            b = f'{adb} -s {self.device} pull sdcard/Pictures/{name}.jpg {cwd}\\screen'
            for cmd in [a, b]:
                os.system(cmd)
                time.sleep(0.02)
            screen = cv2.imread(f'{cwd}\\screen\\{name}.jpg')
            #screen = cv2.imread(f'{nxfd}\\{name}.jpg')
            #大部分模拟器截图自动同步到共享文件夹 其实不用PULL的
        else:
            screen = ImageGrab.grab()            
            if name != 'screen': #非默认情况才保存硬盘 否则直接读取内存文件
                screen.save(f'{cwd}\\screen\\{name}.jpg')
            screen = cv2.cvtColor(numpy.array(screen),cv2.COLOR_RGB2BGR)  
        print('截图已完成 ', time.ctime())        
        self.screen = screen
        return self.screen

    #随机位置偏移，默认左右5个像素
    def random_offset(self, position, range=5):
        x, y = position
        x += random.randint(-range, range)
        y += random.randint(-range, range)
        return (x, y)

    # ADB命令模拟点击屏幕，参数pos为目标坐标(x, y), 自带随机偏移
    # 或pyautogui鼠标点击，带偏移与延迟
    def touch(self, position):
        x, y = self.random_offset(position)
        if self.adb_mode: #手机点击
            cmd = f'{adb} -s {self.device} shell input touchscreen tap {x} {y}'
            os.system(cmd)
        else: #电脑点击
            origin = pyautogui.position()
            dt = random.uniform(0.01, 0.02)
            pyautogui.moveTo(x, y, duration=dt)
            pyautogui.mouseDown(button='left')
            time.sleep(dt) #有的游戏就是不能识别click,但是可以down加up，很奇怪
            pyautogui.mouseUp(button='left')
            pyautogui.moveTo(*origin, duration=dt)

    #拖动或长按
    def drag(self, position_start, end, second=0.2):
        sx, sy = self.random_offset(position_start)
        ex, ey = self.random_offset(end)
        if self.adb_mode:
            cmd = f'{adb} -s {self.device} shell input touchscreen swipe {sx} {sy} {ex} {ey}'
            os.system(cmd)
        else:
            origin = pyautogui.position() #记录原位，点完返回
            dt = random.uniform(0.01, 0.02)
            pyautogui.moveTo(sx, sy, duration=dt)
            pyautogui.dragTo(ex, ey, duration=second+dt)
            pyautogui.moveTo(*origin, duration=dt)

    #在图上标记位置p1左上，p2右下
    def mark(self, background, p1, p2):
        cv2.rectangle(background, p1, p2, (0, 0, 255), 3)

    #核心功能， 在background大图片上定位target_name对应的小图片位置
    #debug开启则会以图片形式显示查找结果
    def locate(self, background, target_name, debug=0):
        loc_pos = []
        target, c_name = self.target_map[target_name]
        h, w, _ = target.shape
        result = cv2.matchTemplate(background, target, cv2.TM_CCOEFF_NORMED)
        location = numpy.where(result >= self.accuracy)        
        dis = lambda a, b: ((a[0]-b[0])**2 + (a[1]-b[1])**2) **0.5 #计算两点距离
        for y, x in zip(*location):
            center = x + int(w/2), y + int(h/2)
            if loc_pos and dis(loc_pos[-1], center) < 20:  #忽略邻近重复的点
                continue
            else:
                loc_pos.append(center)
                p2 = x + w, y + h
                self.mark(background, (x, y), p2)

        if debug:  #在图上显示寻找的结果，调试时开启
            cv2.imshow(f'result for {target_name}:', background)
            cv2.waitKey(0) 
            cv2.destroyAllWindows()
        res = len(loc_pos)
        msg = f'查找结果：{c_name} 匹配到 {res} 个位置'
        print(msg)
        return loc_pos


    #裁剪Img以加速检测， area[h1,h2,w1,w2]为高宽范围百分比
    #选中区域为高h1%到h2% 宽w1%到w2%，返回裁剪后图片与左上角位置
    def cut(self, img, area=[0, 50, 0, 50]):
        h1, h2, w1, w2 = [e/100 for e in area]
        h, w, c = img.shape
        h1, h2 = int(h*h1), int(h*h2)
        w1, w2 = int(w*w1), int(w*w2)
        small = img[h1:h2, w1:w2, :]
        start = [w1, h1]
        return small, start

    #判断name_list中哪些目标存在，但不点击，全部目标遍历，返回同长度真假列表
    #输入[name1,name2...]返回[name1_result, name2_result...]
    def exist(self, name_list, area=None): 
        background = self.screen_shot()
        if area:
            background, start = self.cut(background, area)
        re = []
        name_list = name_list if type(name_list) == list else [name_list,]
        for name in name_list:
            loc_pos = self.locate(background, name)
            cur = len(loc_pos) > 0
            re.append(cur)
        re = re[0] if len(re) == 1 else re
        return re

    #寻找name_list中的目标，并点击第一个找到的目标，然后中止
    #注意有优先级顺序，找到了前面的就不会再找后面的
    #只返回第一个找到并点击的name，都没找到返回false
    def find_touch(self, name_list, area=None):
        background = self.screen_shot()
        if area:
            background, start = self.cut(background, area)
        re = False
        name_list = name_list if type(name_list) == list else [name_list,]
        for name in name_list:
            loc_pos = self.locate(background, name)
            if len(loc_pos) > 0:
                if area: #从裁剪后的坐标还原回裁前的坐标
                    loc_pos[0][0] += start[0] 
                    loc_pos[0][1] += start[1]
                self.touch(loc_pos[0]) #同一目标多个结果时只点第一个
                re = name
                break            
        return re
