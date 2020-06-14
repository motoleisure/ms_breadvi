# -*- coding: utf-8 -*-

### 导入相关模块
import cv2
import numpy as np

class BreadModel(object):
    
    def __init__(self, model_file='model/data/yolov3-voc_my_bread.weights', net_file='model/data/yolov3-voc_my_bread.cfg', class_file='model/data/my_bread.names', gpu_fraction=0.15, input_image_size=(416,416), nmsThreshold=0.4, confThreshold=0.35):
        self.model_file = model_file
        self.net_file = net_file
        self.class_name = open(class_file, 'r').read().split("\n")[:-1]
        self.gpu_fraction = gpu_fraction
        self.input_image_size = input_image_size
        self.nmsThreshold = nmsThreshold
        self.confThreshold = confThreshold
        self.net = None
        self.load_model()
    
    ### 加载模型
    # 过程：使用Opencv加载darknet yolo模型
    def load_model(self): 
        self.net = cv2.dnn.readNetFromDarknet(self.net_file, self.model_file)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        
    ### 执行模型推理
    # 输入：单张图片， image_np
    # 输出：out_classes, out_scores, out_boxes
    def inference(self, image):
        ### 图片预处理
        pre_image = self.preprocess(image)
        
        ### 执行推理
        self.net.setInput(pre_image)
        outs = self.net.forward(self._getOutputsNames())
        
        # Remove the bounding boxes with low confidence
        out_classes, out_scores, out_boxes = self.postprocess(image, outs)
        
        return out_classes, out_scores, out_boxes
    
    ### 图片预处理函数
    # 输入： 单张图片，image_np
    # 输出： 预处理后的图片， blob, (n, channel, width, height)
    def preprocess(self, image):
        pre_image = cv2.dnn.blobFromImage(image, 1/255, self.input_image_size, [0,0,0], 1, crop=False)
        return pre_image
    
    def postprocess(self, image, outs):
        frameHeight = image.shape[0]
        frameWidth = image.shape[1]
        
        ### 过滤概率阈值
        classIds = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
    
        ### 非极大值抑制
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        
        ### 提取最终结果
        out_classes = []
        out_scores = []
        out_boxes = []
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            
            out_classes.append(self.class_name[classIds[i]])
            out_scores.append(confidences[i])
            out_boxes.append([left, top, left + width, top + height])
        
        return out_classes, out_scores, out_boxes
    
    ### 获取网络输出层的名称
    def _getOutputsNames(self):
        # Get the names of all the layers in the network
        layersNames = self.net.getLayerNames()
    	
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
