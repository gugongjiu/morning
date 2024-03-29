from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = '440307'
girl_birthday = '09-03'
boy_birthday = '11-28'

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = ['ozwzw6rzU02nSRoaDWAMEfCf75T8', 'o5-N56ESeHQNqYmQTalM2JSf_2m4']

template_id = os.environ["TEMPLATE_ID"]


def get_today():
    weekday = 0
    if datetime.now().isoweekday() == 1:
        weekday = "星期一"
    elif datetime.now().isoweekday() == 2:
        weekday = "星期二"
    elif datetime.now().isoweekday() == 3:
        weekday = "星期三"
    elif datetime.now().isoweekday() == 4:
        weekday = "星期四"
    elif datetime.now().isoweekday() == 5:
        weekday = "星期五"
    elif datetime.now().isoweekday() == 6:
        weekday = "星期六"
    elif datetime.now().isoweekday() == 7:
        weekday = "星期日"
    return str(date.today()) + " " + weekday


def get_weather():
    url = "https://restapi.amap.com/v3/weather/weatherInfo?key=65d8f52f1a30b4a96d97ae771738cd70&city=" + city
    res = requests.get(url).json()
    print(res)
    weather = res['lives'][0]
    return weather['weather'], weather['temperature'], weather['humidity'], weather['windpower']


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_gril_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + girl_birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_boy_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + boy_birthday, "%Y-%m-%d")
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


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, humidity, wind = get_weather()
data = {"today": {"value": get_today(), "color": get_random_color()},
        "city": {"value": city, "color": get_random_color()},
        "weather": {"value": wea, "color": get_random_color()},
        "temperature": {"value": temperature, "color": get_random_color()},
        "humidity":{"value": humidity, "color": get_random_color()},
        "wind":{"value": wind, "color": get_random_color()},
        "love_days": {"value": get_count(), "color": get_random_color()},
        "gril_birthday": {"value": get_gril_birthday(), "color": get_random_color()},
        "boy_birthday": {"value": get_boy_birthday(), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()}
        }
res = wm.send_template(user_id[0], template_id, data)
print(res)
# res = wm.send_template(user_id[1], template_id, data)
# print(res)
