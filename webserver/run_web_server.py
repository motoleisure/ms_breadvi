# -*- coding: utf-8 -*-

import flask
import redis
import json

db = redis.StrictRedis(host="localhost", port=6379, db=0)
ORDER_KEY = 'BM_ORDER_DICT'
# initialize our Flask application and Redis server
app = flask.Flask(__name__)

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

class_price = {
    'dgxs': 18,
    'fg': 20, 
    'hmlm': 12, 
    'hmyzd': 12, 
    'hmzl': 26, 
    'qbt': 22, 
    'tyh': 16, 
    'wgr': 18
}

def show_shopping_list():
    ORDER_DICT = db.get(ORDER_KEY)
    if ORDER_DICT is not None:
        SHOPPING_LIST = json.loads(ORDER_DICT.decode('utf-8'))
    
        shopping_list_table = "<tr><th width='50px'>商品编号</th><th width='300px'>商品名称</th><th width='40px'>数量</th><th width='60px'>单价(元)</th></tr>"
        tr_style = "onmouseover=" + '"' + "this.style.backgroundColor='#ffff66';" + '"' + " onmouseout=" + '"' + "this.style.backgroundColor='#ffffff';" + '"'
        tot_price = 0
        tot_num = 0
        
        for key, value in SHOPPING_LIST.items():
            shopping_list_table += "<tr " + tr_style + "><td style='color:blue;'>" + '1' + "</td><td style='color:blue;'>" + class_description[key] + "</td><td style='color:blue;'>+" + str(value) + "</td><td style='color:blue;'>" + str(class_price[key]) + "</td></tr>"
            tot_num += value
            tot_price += class_price[key] * value
    
        shopping_list_table += "<tr><td style='color:blue;'>总价</td><td style='color:blue;'></td><td style='color:blue;'>" + str(tot_num) + "</td><td style='color:blue;'>" + str(tot_price) + "</td></tr>"
    
    return shopping_list_table
    
@app.route("/")
def homepage():
    print(flask.request.path)
    return app.send_static_file("shoppinglist.html")

@app.route("/getshoppinglist", methods=["GET"])
def getshoppinglist():
    # 网页客户端调用，用于ajax自动更新shopping list
    #SHOPPING_LIST = update_shopping_list_from_db_v2(cabinet_id)
    SHOPPING_LIST_TABLE = show_shopping_list()
    return SHOPPING_LIST_TABLE

if __name__ == "__main__":
    print("* Starting web service...")
    app.run()