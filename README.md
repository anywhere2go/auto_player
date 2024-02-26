感谢anywheretogo大佬提供的脚本框架，此脚本在原作基础上加入了很多功能，也修复了一些问题。开发测试均基于体验服，平台为电脑桌面版和安卓（支持模拟器和实体机）。

1. 安装python
此脚本兼容Windows/Mac系统，并支持ADB使用模拟器，对于不了解python的用户，首先要安装python官方的必要安装包。下载地址: https://www.python.org/downloads/release/python-31011/， 选择对应的系统就好。

2. 配置程序环境
安装好python后还需要另外安装三个python库，分别是opencv，pyautogui，和mss。这个步骤Windows和Mac略有不同：
Windows/Linux：管理员身份打开命令行（cmd）或者powershell，然后运行 pip install opencv-python pyautogui mss
Mac：在终端（terminal）下分别运行 pip3 install opencv-python pyautogui mss

3. 运行脚本
Windows下可使用IDLE或其他方式运行（比如powershell/终端），然后打开yys.py脚本源代码，点击运行（F5）则开启脚本。安卓模拟器推荐使用自带的终端Terminal，使用python3 yys.py 方式运行。推荐使用雷电模拟器，MuMu模拟器会相对卡一些不知道什么原因。
桌面版必须使用原始分辨率即1136x640（安卓/模拟器会自动设置成桌面版分辨率），其它分辨率则需要重新截图才能正常工作。另外桌面版（非模拟器）游戏窗口务必要移动到左上角。退出脚本按CTRL+C即可。

解放双手 Have fun!
