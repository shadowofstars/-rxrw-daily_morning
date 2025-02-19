from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

'''
def get_leo_info():
    info = requests.get('https://api.vvhan.com/api/horoscope?type=leo&time=today')
    if info.status_code != 200:
        return get_leo_info()
    info_data = info.json()['data']
    fortune='整体运势: '+str(info_data['fortune']['all'])+'\t爱情运势: '+str(info_data['fortune']['love'])+'\t工作运势: '+str(info_data['fortune']['work'])+'\t金钱运势: '+str(info_data['fortune']['money'])
    lucky_color = info_data['luckycolor']
    all_description=info_data['fortunetext']['all']
    love_description = info_data['fortunetext']['love']
    health_description = info_data['fortunetext']['health']
    return fortune,lucky_color,all_description,love_description,health_description

fortune,lucky_color,all_description,love_description,health_description = get_leo_info()
"fortune":{'value':fortune},
"lucky_color":{'value':lucky_color},
"all_description":{'value':all_description},
"love_description":{'value':love_description},
"health_description":{'value':health_description},
'''



client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()

lucky_score = random.randint(60,90)
data = {"weather":{"value":wea},
        "temperature":{"value":temperature},
        "love_days":{"value":get_count()},
        "birthday_left":{"value":get_birthday()},
        "lucky_score":{'value':lucky_score},
        "words":{"value":get_words(),"color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
