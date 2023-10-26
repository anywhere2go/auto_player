感谢anywheretogo大佬提供的脚本框架，此脚本在原作基础上加入了很多功能，也修复了一些问题。开发测试均基于体验服，平台为电脑桌面版新引擎测试（模拟器上由于画面不一致可能不能用）。

1. 安装python
此脚本兼容Windows/Mac系统，并支持ADB使用模拟器，对于不了解python的用户，首先要安装python官方的必要安装包：
3.7.6版本下载地址: https://www.python.org/downloads/release/python-376/， 选择对应的系统就好。

2. 配置程序环境
安装好python后还需要另外安装三个python库，分别是opencv，pyautogui，和mss。这个步骤Windows和Mac略有不同：
Windows：管理员身份打开命令行（cmd）或者powershell，然后分别运行 pip install opencv-python 和 pip install pyautogui 和 pip install mss 和 pip install Pillow。
Mac：在终端（terminal）下分别运行 pip3 install opencv-python 和 pip3 install pyautogui 和 pip3 install mss 和 pip3 install Pillow

3. 运行脚本
Windows下可使用IDLE或其他方式运行（比如powershell），然后打开yys.py脚本源代码，点击运行（F5）则开启脚本。macOS下推荐使用自带的终端Terminal，使用python3 yys.py 方式运行。
桌面版必须使用原始分辨率（模拟器需要设置成桌面版分辨率），其它分辨率则需要重新截图才能正常工作。另外游戏窗口务必要移动到左上角。

解放双手 Have fun!
