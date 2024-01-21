import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage
import os

LINE_TOKEN = os.environ.get("LA_LINETOKEN")
CNAME = os.environ.get("LA_CNAME")
PAGEURL = os.environ.get("LA_PAGEURL")
UPPERCOMMENT = os.environ.get("LA_UPPERCOMMENT")
GROUP_ID = os.environ.get("GROUP_ID")

with open("lastid.txt","r") as f:
    LASTID = int(f.read())
LASTID_NEW = None

print("Start Process")

linebot = None
response = requests.get(PAGEURL)
soup = BeautifulSoup(response.text, 'html.parser')
commentelems = soup.find("ol",{"class":"commets-list"}).find_all("li")
for a in commentelems:
    Id = int(a["id"].replace("comment-",""))
    Name = a.find("cite",{"class":"fn comment-author"}).text
    if CNAME not in Name:
        continue
    if LASTID >= Id:
        continue
    Pushdate = a.find("span",{"class":"st-comment-datetime"}).text
    Commenttext = a.find("div",{"class":"st-comment-content"}).text
    sendtext  = UPPERCOMMENT+"\n"
    sendtext += "名前："+Name+"\n"
    sendtext += Pushdate+"\n"
    sendtext += Commenttext
    if linebot == None:
        linebot = LineBotApi(LINE_TOKEN)
    line_bot_api.push_message(GROUP_ID, TextSendMessage(text = sendtext))
    if LASTID_NEW == None or Id > LASTID_NEW:
        LASTID_NEW = Id

if LASTID_NEW != None and type(LASTID_NEW) == int:
    with open("lastid.txt", "w") as f:
        f.write(str(LASTID_NEW))
print("Success Process")
