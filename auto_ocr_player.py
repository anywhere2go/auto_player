# coding: utf-8
from auto_player import Player
import paddlehub as hub

class OCR_Player(Player):
    """docstring for OCR_player"""
    def __init__(self, accuracy=0.6, adb_mode=False, adb_num=0):
        super(OCR_Player, self).__init__(accuracy, adb_mode, adb_num)
        self.ocr = hub.Module(name="chinese_ocr_db_crnn_mobile", enable_mkldnn=True)
        self.accuracy = accuracy

    def read(self, debug=False):
        screen = self.screen_shot()
        imgs = [screen,]
        results = self.ocr.recognize_text(
                            images=imgs,         # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
                            use_gpu=False,            # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
                            output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
                            visualization=debug,       # 是否将识别结果保存为图片文件；
                            box_thresh=self.accuracy,           # 检测文本框置信度的阈值；
                            text_thresh=self.accuracy)          # 识别中文文本置信度的阈值；
        data = results[0]['data']
        return data

    def find_touch(self, key_list, debug=False):
        data = self.read(debug)
        key_list = [key_list,]if type(key_list) == str else key_list
        re = False
        for key in key_list:
            if key[0] == 's':
                key = key[1:]
                found = [e for e in data if key == e['text']]
            else:
                found = [e for e in data if key in e['text']]
            msg = f'目标：{key},  找到数量：{len(found)}'
            print(msg)
            if found:
                p1, _, p2, _ = found[0]['text_box_position']
                (x1, y1), (x2, y2) = p1, p2
                center = (int((x1+x2)/2), int((y1+y2)/2))
                self.touch(center)
                re = key
                break
        return re

    def exist(self, key_list, debug=False):
        data = self.read(debug)
        key_list = [key_list,]if type(key_list) == str else key_list
        re = []
        for key in key_list:
            if key[0] == 's':
                key = key[1:]
                found = [e for e in data if key == e['text']]
            else:
                found = [e for e in data if key in e['text']]
            msg = f'目标：{key},  找到数量：{len(found)}'
            re.append(len(found))
        re = re[0] if len(re) == 1 else re
        return re



