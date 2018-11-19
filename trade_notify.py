import random
import hashlib
import hmac, time
import smtplib
# from email.mime.text import MIMEText
# from email import utils
import threading
import requests,datetime, itchat
from toolkit import Toolkit

class Jubi_web():
    def __init__(self):
        cfg = Toolkit.getUserData("data.cfg")
        self.public_key = cfg['public_key']
        self.private_key = cfg['private_key']
        self.w_name=u'Stefan'
        itchat.auto_login(hotReload=True)
        account=itchat.get_friends(self.w_name)
        for i in account:
            # print("pinyin: ",i[u'PYQuanPin'])
            if i[u'PYQuanPin']==self.w_name:
                self.toName= i['UserName']
                # print(self.toName)

    def send_wechat(self,name,content):
        w_content=name+' '+content
        itchat.send(w_content,toUserName=self.toName)
        time.sleep(1)
        itchat.send(w_content,toUserName='filehelper')

    def warming(self, coin, up_price, down_price):
        url = 'https://api.coinegg.im/api/v1/ticker/region/btc'
        while 1:
            # time.sleep(5)
            try:
                data = requests.post(url, data={'coin': coin}).json()
            except Exception as e:
                print (e)
                print ("time out. Retry")
                time.sleep(15)
                continue
            current = float(data['last'])
            print("current:{} up:{} down:{}".format(current, up_price, down_price))
            if current >= up_price:
                print ("Up to ", up_price)
                print ("current price ",current)
                self.send_wechat(coin,str(current))

                time.sleep(1200)
            if current <= down_price:
                print ("Down to ", down_price)
                print ("current price ",current)
                self.send_wechat(coin,str(current))
                time.sleep(1200)
        
    def multi_thread(self,coin_list,price_list):
        thread_num=len(coin_list)
        thread_list=[]
        for i in range(thread_num):
            t=threading.Thread(target=self.warming, args=(coin_list[i],price_list[i][0],price_list[i][1]))
            thread_list.append(t)
        for j in thread_list:
            j.start()
        for k in thread_list:
            k.join()

if __name__ == "__main__":
    obj = Jubi_web()
    coin_list = ['zet','doge']
    price_list = [[0.2,0.13],[0.03,0.024]]
    obj.multi_thread(coin_list,price_list)