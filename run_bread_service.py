# -*- coding: utf-8 -*-

import cv2
import time
from imutils.video import FPS
import redis
import json

from model.breadmodel import BreadModel
#from vitool.video import VideoStream

DB = redis.StrictRedis(host='192.168.3.6', port=6379, db=0)

class_description = {
    'dgxs': '德国咸水',
    'fg': '法棍', 
    'hmlm': '黑麦黎麦', 
    'hmyzd': '黑麦鹰嘴豆', 
    'hmzl': '黑麦杂粮', 
    'qbt': '恰巴塔', 
    'tyh': '太阳花', 
    'wgr': '歪果仁'
}

def draw_frame(frame, out_classes, out_scores, out_boxes):
    for k in range(len(out_classes)):
        classlabel = out_classes[k]
        scores = out_scores[k]
        box = out_boxes[k]
        label = str(classlabel) + ": " + str(scores)
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0,0,255), 2)
        cv2.putText(frame, label, (box[0], box[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)
        
    return frame

def generate_order(out_classes):
    tot = {}
    for i in range(len(out_classes)):
        if out_classes[i] not in tot.keys():
            tot[out_classes[i]] = 0
        tot[out_classes[i]] += 1
    
    return tot
        
model_file = 'model/data/yolov3-tiny_cifar10_my_bread.weights'
net_file = 'model/data/yolov3-tiny_cifar10_my_bread.cfg'
confThreshold = 0.35
   
BM = BreadModel(model_file, net_file)

'''
### 视频
'''
cap = cv2.VideoCapture(0)
#cap.stream.stream.set(3,640)
#cap.stream.stream.set(4,480)

fps = FPS()
fps.start()

while True:
    res, frame = cap.read()
    if not(res):
        print('Camera Read Failed.')
        break
    frame_drawed = frame.copy()
    fps.update()
    
    out_classes, out_scores, out_boxes = BM.inference(frame)
    print("Done Detected")
    if len(out_classes) > 0:
        #frame_drawed = draw_frame(frame_drawed, out_classes, out_scores, out_boxes)
        order_dict = generate_order(out_classes)
        DB.set("BM_ORDER_DICT", json.dumps(order_dict))
    else:
        order_dict = {}
        DB.set("BM_ORDER_DICT", json.dumps(order_dict))
    #cv2.imshow('test', frame_drawed)
    #butt = cv2.waitKey(1) & 0xFF
    #if butt == ord('q'):
    #    break
    ### 睡眠1秒钟
    #time.sleep(1)
    
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
cap.release()
