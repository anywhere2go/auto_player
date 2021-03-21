import time, os
import auto_player as player

def get_pictures():   
    player.screen_shot()

def auto_play_yuhun(round=50):
    count = 0
    while count < round:       
        ar1 = ['start_yys', 'exp_yys',]
        re = player.find_touch_any(ar1)
        if re == 'start_yys':
            print('开始新一轮...')
            count += 1
            #time.sleep(10)
        elif re == 'exp_yys':
            print('领取奖励...')
        elif re is None:
            ar2 = ['going_yys',]
            re = player.find_touch_any(ar2, False)
            if re == 'goging_yys':
                print('托管中...')
                time.sleep(5)


def function3():
    print('功能3未设置')

def menu(debug=False):

    menu_list = [
    [get_pictures, '获取当前屏幕截图'],
    [auto_play_yuhun, '自动刷图_御魂'],
    [function3, 'function3功能描述']
    ]

    start_time = time.time()
    print('程序启动，当前时间', time.ctime(), '\n')
    while True:
        i = 0
        for func, des in menu_list:
            msg = str(i) + ": " + des + '\n'
            print(msg)
            i += 1
        player.alarm(1)
        raw = input("选择功能模式：") if not debug else 1
        index = int(raw) if raw else 1
        func, des = menu_list[index]
        print('已选择功能： ' + des)
        func()

if __name__ == '__main__':
    menu()
