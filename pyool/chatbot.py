import requests 
import time 


# Defining ChatBot specific Class to send messages to Dingtalk 

class ChatBot: 

    def send_markdown(self, payload, access_token): 
        url = "https://oapi.dingtalk.com/robot/send?access_token=" + str(access_token)  
        headers = {"Content-Type": "application/json;charset=utf-8"}

        attemps = 0 

        while attemps < 3: 
            print("Sending to Dingtalk .....")

            r = requests.post(url, headers = headers, json = payload) 

            if (r.text == """{"errcode":0,"errmsg":"ok"}""" or r.text == """{"errmsg":"ok","errcode":0}"""): 
                print("Message is sent.")
                break 

            else: 
                attemps += 1
                error = "Attemps {}, error {}. Retrying ....."
                error = error.format(attemps, r.text) 
                print(error) 
                time.sleep(10)
                continue 
            
            raise RuntimeError("Cannnot send message due to %s" % r.text) 


    def send2ding(self, title, message, access_token):
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": message 
            }, 
            "at": {}
        }

        self.send_markdown(payload = payload, access_token = access_token)
