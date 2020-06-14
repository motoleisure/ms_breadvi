# -*- coding: utf-8 -*-

import cv2

from model.breadmodel import BreadModel

def draw_frame(frame, out_classes, out_scores, out_boxes):
    for k in range(len(out_classes)):
        classlabel = out_classes[k]
        scores = out_scores[k]
        box = out_boxes[k]
        label = str(classlabel) + ": " + str(scores)
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0,0,255), 2)
        cv2.putText(frame, label, (box[0], box[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)
        
    return frame

model_file = 'model/data/yolov3-tiny_cifar10_my_bread.weights'
net_file = 'model/data/yolov3-tiny_cifar10_my_bread.cfg'
BM = BreadModel(model_file=model_file, net_file=net_file)

test_image_file = 'test_images_02.jpg'
image = cv2.imread(test_image_file)

out_classes, out_scores, out_boxes = BM.inference(image)
print("Done Detected")
if len(out_classes) > 0:
    frame_drawed = draw_frame(image, out_classes, out_scores, out_boxes)
    cv2.imshow('test', frame_drawed)


