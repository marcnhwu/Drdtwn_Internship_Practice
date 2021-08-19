#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 2.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No Match Intent!"
                }
            ]
        }
"""

from requests import post
from requests import codes
import math
try:
    from intent import Loki_item
    from intent import Loki_ice
    from intent import Loki_sweetness
    from intent import Loki_size
except:
    from .intent import Loki_item
    from .intent import Loki_ice
    from .intent import Loki_sweetness
    from .intent import Loki_size


import json
with open("account.info.py", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())
    
LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = accountDICT["username"]
LOKI_KEY = accountDICT["loki_project_key"]
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "Connect failed."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[]):
    resultDICT = {}
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # item
                if lokiRst.getIntent(index, resultIndex) == "item":
                    resultDICT = Loki_item.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # ice
                if lokiRst.getIntent(index, resultIndex) == "ice":
                    resultDICT = Loki_ice.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # sweetness
                if lokiRst.getIntent(index, resultIndex) == "sweetness":
                    resultDICT = Loki_sweetness.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # size
                if lokiRst.getIntent(index, resultIndex) == "size":
                    resultDICT = Loki_size.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)


userDefinedDICT = {"hot": ["熱", "熱的", "熱飲", "做熱的", "熱一點", "燙", "燙一點", "溫", "溫的", "室溫", "溫飲", "做溫的", "做常溫", "做常溫的"], "ice": ["冰", "冰塊", "正常冰", "少冰", "七分冰", "半冰", "五分冰", "三分冰", "一分冰", "微冰", "碎冰", "去冰", "冰塊少一點", "冰塊一點點", "冰的"], "item": ["原鄉四季", "原鄉", "四季茶", "四季", "極品菁茶", "極品菁", "極菁", "菁茶", "烏龍綠茶", "烏龍綠", "烏綠", "特級綠茶", "特級綠", "特綠", "特級", "綠茶", "特選普洱", "特選普", "特普", "特選", "普洱茶", "普洱", "翡翠烏龍", "翡翠烏", "烏龍茶", "烏龍", "翡翠", "錫蘭紅茶", "錫蘭紅", "錫蘭", "錫紅", "紅茶", "嚴選高山茶", "嚴選", "高山茶", "高山"], "size": ["超大", "大", "中", "小"], "sweetness": ["糖", "糖分", "甜", "甜度", "正常甜", "七分甜", "五分甜", "三分甜", "一分甜", "微甜", "微微甜", "全糖", "七分糖", "半糖", "五分糖", "三分糖", "一分糖", "糖七分", "糖五分", "糖三分", "糖一分", "微糖", "去糖", "無糖"]}

expandDICT = {"原鄉四季": ["原鄉四季", "原鄉", "四季茶", "四季"],
              "極品菁茶": ["極品菁茶", "極品菁", "極菁", "菁茶"],
              "烏龍綠茶": ["烏龍綠茶", "烏龍綠", "烏綠"],
              "特級綠茶": ["特級綠茶", "特級綠", "特綠", "特級", "綠茶"],
              "特選普洱": ["特選普洱", "特選普", "特普", "特選", "普洱茶", "普洱"],
              "翡翠烏龍": ["翡翠烏龍", "翡翠烏", "烏龍茶", "烏龍", "翡翠"],
              "錫蘭紅茶": ["錫蘭紅", "錫蘭", "錫紅", "紅茶"],
              "嚴選高山茶": ["嚴選高山茶", "嚴選", "高山茶", "高山"],
              "冰的": ["冰", "冰塊", "正常"],
              "熱的": ["熱", "熱的", "熱飲", "做熱的", "熱一點", "燙", "燙一點"],
              "溫的": ["溫", "溫的", "室溫", "溫飲", "做溫的", "做常溫", "做常溫的"]}


if __name__ == "__main__":
    from ArticutAPI import Articut
    articut = Articut(username=accountDICT["username"], apikey=accountDICT["articut_api_key"])
    

    # 句子一
    inputLIST = ["一杯紅茶和烏龍綠茶"]
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    #print("Result => {}".format(resultDICT))
    
    for i in range(0, len(resultDICT["amount"])):
        lv3DICT = articut.parse(resultDICT["amount"][i], level="lv3")
        #print(lv3DICT)
        amount = lv3DICT["number"][resultDICT["amount"][i]]
        resultDICT["amount"][i] = amount
        
        #get full item name
        for full, short in expandDICT.items():
            if resultDICT["item"][i] in short:
                resultDICT["item"][i] = full
                
        #get full ice name
        for full, short in expandDICT.items():
            if resultDICT["temperature"][i] in short:
                resultDICT["temperature"][i] = full
                   
    
    #check 1
    for j in range(len(resultDICT["amount"])):
        if "不確定" in resultDICT["temperature"][j]:
            print("溫度要怎麼調整呢？？")      
        elif resultDICT["temperature"][0] in Loki_item.userDefinedDICT["hot"] and resultDICT["temperature"][1] in Loki_item.userDefinedDICT["ice"]:
            print("你要熱的還是冰的？")
        elif "不確定" in resultDICT["sweetness"][j]:
            print("甜度要怎麼調整呢？")
        elif "不確定" in resultDICT["size"][j]:
            print("大杯還是小杯？")    
        else:
            print("您點了:\n",resultDICT["size"][j], resultDICT["item"][j], "X", resultDICT["amount"][j], resultDICT["temperature"][j], resultDICT["sweetness"][j])            
    
    #check 2
    for j in range(len(resultDICT["amount"])):
        print("您點了:\n{} X {} (溫度：{}, 甜度：{})".format(resultDICT["item"][j], resultDICT["amount"][j], resultDICT["temperature"][j], resultDICT["sweetness"][j]))

    print("\n")
    
    
    ## 句子二
    #inputLIST = ["兩杯大杯溫紅茶，甜度冰塊正常"] #兩杯大杯熱的錫蘭紅茶，甜度冰塊正常
    #filterLIST = []
    #resultDICT = runLoki(inputLIST, filterLIST)
    ##print("Result => {}".format(resultDICT))
    
    #lv3DICT = articut.parse(resultDICT["amount"], level="lv3")
    #amount = lv3DICT["number"][resultDICT["amount"]]
    #resultDICT["amount"] = amount

    ##get full item name
    #for full, short in expandDICT.items():
        #if resultDICT["item"] in short:
            #resultDICT["item"] = full

    ##get full ice name
    #for i in range(0, len(resultDICT["temperature"])):
        #for full, short in expandDICT.items():
            #if resultDICT["temperature"][i] in short:
                #resultDICT["temperature"][i] = full

            
    #if "不確定" in resultDICT["temperature"]:
        #print("溫度要怎麼調整呢？")
    #elif resultDICT["temperature"][0] in Loki_item.userDefinedDICT["hot"] and resultDICT["temperature"][1] in Loki_item.userDefinedDICT["ice"]:
        #print("你要{}還是{}？".format(resultDICT["temperature"][0], resultDICT["temperature"][1]))
    #elif "不確定" in resultDICT["sweetness"]:
        #print("甜度要怎麼調整呢？")
    #elif "不確定" in resultDICT["size"]:
        #print("大杯還是小杯？")
    #else:
        #print("您點了:\n",resultDICT["size"], resultDICT["item"], "X", resultDICT["amount"], resultDICT["temperature"], resultDICT["sweetness"])
    
    ##print("您點了:\n{} {} X {} (溫度：{}, 甜度：{})".format(resultDICT["size"], resultDICT["item"], resultDICT["amount"], resultDICT["ice"], resultDICT["sweetness"]))