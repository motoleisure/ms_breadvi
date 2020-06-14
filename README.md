# breadvi
bread vi

1.目录介绍
model/
    data/                   存放模型权重/网络配置/分类名称文件
    breadmodel.py           面包检测模型类
webserver/                  web服务模块，可视化订单
run_bread_service.py        主要程序文件，读取视频流，识别面包，推送数据到redis
test.py                     临时测试文件

2.面包检测模型类介绍
使用例子：
from model.breakmodel import BreadModel

BM = BreadModel()                           默认参数可以直接查看breadmodel.py源码
img = cv2.imread('xxx.jpg')                 
out_classes, out_scores, out_boxes = BM.inference(img)

模型默认调用yolov3较重的那个模型，如果需要加载其他模型，需要指定model_file和net_file

model_file = 'model/data/xxx.weights'
net_file = 'mode./data/xxx.cfg'

BM = BreadModel(model_file=model_file, net_file=net_file)
