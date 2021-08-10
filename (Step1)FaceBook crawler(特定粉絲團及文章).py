# coding: utf-8

# In[ ]:

# 匯入所需套件

import requests
import json
import pandas as pd 
from dateutil.parser import parse
import codecs
# -------------google API---------------
from google.cloud import language
from google.cloud import translate
# -------------爬蟲---------------
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import requests
from selenium.common.exceptions import NoSuchElementException
import itertools
from selenium import webdriver


# 抓取指定粉絲團的特定文章資訊：留言(id與其留言內容)、按讚(含各種符號於使用者id)、分享者的id，全部的id一起取，最後輸出有留言、按讚、分享的所有id(在同一個list)
def get_id(fanpage_id,post_id):
    token = input("token = ")
    res= requests.get("https://graph.facebook.com/v2.10/"+fanpage_id+"/posts?fields=message,id,comments{from,message},reactions{id,type,name},sharedposts{from}&access_token=%s" % token)
    userlist=[]
#     while 'paging' in res.json():
    for information in res.json()['data']:
        if information['id'] == post_id:
            if 'message' in information:
                user_information={}
                user_information['content'] = information['message']
                user_information['content'] = information['id']
                user_information['comment'] = {}
                user_information['comment']['data'] = []
                user_information['reactions'] = {}
                user_information['reactions']['data'] = []
                user_information['sharedposts'] = {}
                user_information['sharedposts']['data'] = []
            else:
                user_information['content'] = "NO MESSAGE"

    # -----------------------------------------------留言------------------------------------------------

            for i in information['comments']['data']:
                
                language_client = language.Client()
                translate_client = translate.Client()
                text = i['message']

    #----------------------translation API----------------------

                target = 'en'
                translation = translate_client.translate(
                    text,
                    target_language=target)
                trans = translation['translatedText']
                document = language_client.document_from_text(trans)

    #----------------------Natural Language API----------------------

                sentiment = document.analyze_sentiment().sentiment
                from_1 = {}
                from_1['from'] = {} 
                from_1['from']['name'] = i['from']['name']
                from_1['from']['id'] = i['from']['id']
                from_1['message'] = i['message']
                from_1['sentiment_score'] = sentiment.score
                from_1['sentiment_magnitude'] = sentiment.magnitude
                user_information['comment']['data'].append(from_1)
                
    #----------------------Analyze Entities----------------------                

                entity_response = document.analyze_entities()
                for entity in entity_response.entities:
                    form = {}
                    form['entity'] = {}
                    form['entity']['name'] = entity.name
                    form['entity']['type'] = entity.entity_type
                    form['entity']['metadata'] = entity.metadata
                    form['entity']['salience'] =entity.salience
                    user_information['comment']['data'].append(form)
                if i['from']['id'] in userlist:
                    pass
                else:
                    userlist.append(i['from']['id'])
                user_information['comment']['data'].append(from_1)
            if 'next' in information['comments']['paging']:
                res_1 = requests.get(information['comments']['paging']['next'])
                while 'next' in res_1.json()['paging']:
                    try:
                        for i in res_1.json()['data']:
                            from_1 = {}
                            from_1['from'] = {} 
                            from_1['from']['name'] = i['from']['name']
                            from_1['from']['id'] = i['from']['id']
                            from_1['message'] = i['message']

                            
                            if i['from']['id'] in userlist:
                                pass
                            else:
                                userlist.append(i['from']['id'])
                            user_information['comment']['data'].append(from_1)
                        res_1 = requests.get(res_1.json()['paging']['next'])
                    except:
                        pass
            else:
                pass

    # -----------------------------------------------按讚------------------------------------------------

            for i in information['reactions']['data']:
                from_2 = {}
                from_2['from'] = {}
                from_2['from']['id'] = i['id']
                from_2['from']['name'] = i['name']
                from_2['from']['type'] = i['type']
                if i['id'] in userlist:
                    pass
                else:
                    userlist.append(i['id'])
                user_information['reactions']['data'].append(from_2)
            res_2 = requests.get(information['reactions']['paging']['next'])
            while 'next' in res_2.json()['paging']:
                try:
                    for i in res_2.json()['data']:
                        
                        from_2 = {}
                        from_2['from'] = {}
                        from_2['from']['id'] = i['id']
                        from_2['from']['name'] = i['name']
                        from_2['from']['type'] = i['type']
                        if i['id'] in userlist:
                            pass
                        else:
                            userlist.append(i['id'])
                        user_information['reactions']['data'].append(from_2)
                    res_2 = requests.get(res_2.json()['paging']['next'])
                except:
                    pass
    # -----------------------------------------------分享------------------------------------------------

            for i in information['sharedposts']['data']:
                from_3 = {}
                from_3['from'] = {}
                from_3['from']['id'] = i['from']['id']
                from_3['from']['name'] = i['from']['name']
                if i['from']['id'] in userlist:
                    pass
                else:
                    userlist.append(i['from']['id'])
                user_information['sharedposts']['data'].append(from_3)
                res_3 = requests.get(res_3.json()['paging']['next'])
                while 'next' in res_3.json()['paging']:
                    try:
                        for i in res_3.json()['data']:
                            from_3 = {}
                            from_3['from'] = {}
                            from_3['from']['id'] = i['from']['id']
                            from_3['from']['name'] = i['from']['name']
                            user_information['sharedposts']['data'].append(from_3)
                        res_3 = requests.get(res_3.json()['paging']['next'])
                    except:
                        pass
# -----------------------------------------------匯出------------------------------------------------
            with open('test.json', 'wb') as outfile:
                json.dump(user_information, codecs.getwriter('utf-8')(outfile), ensure_ascii=False)
    return userlist


# -----------------------------------------------執行------------------------------------------------

get_id('','')

# ------------------------------------------------留言、按讚、分享分開取id，可分別分析------------------------------------------

def get_reactions_id(fanpage_id,post_id):
    token = input('token = ')
    res= requests.get("https://graph.facebook.com/v2.10/"+fanpage_id+"/posts?fields=message,id,comments{from,message},reactions{id,type,name},sharedposts{from}&access_token=%s" % token)
    reactions_id=[]
    for i in information['reactions']['data']:
        for information in res.json()['data']:
            if information['id'] == post_id:
                from_2 = {}
                from_2['from'] = {}
                from_2['from']['id'] = i['id']
                from_2['from']['name'] = i['name']
                from_2['from']['type'] = i['type']
                reactions_id.append(i['id'])
                user_information['reactions']['data'].append(from_2)
        #             print(user_information)
            res_2 = requests.get(information['reactions']['paging']['next'])
            while 'next' in res_2.json()['paging']:
                try:
                    for i in res_2.json()['data']:
                        from_2 = {}
                        from_2['from'] = {}
                        from_2['from']['id'] = i['id']
                        from_2['from']['name'] = i['name']
                        from_2['from']['type'] = i['type']
                        reactions_id.append(i['id'])
                        user_information['reactions']['data'].append(from_2)
                    res_2 = requests.get(res_2.json()['paging']['next'])
                except:
                    pass
    return reactions_id


def get_comment_id(fanpage_id,post_id):
    token = input('token = ')
    res= requests.get("https://graph.facebook.com/v2.10/"+fanpage_id+"/posts?fields=message,id,comments{from,message},reactions{id,type,name},sharedposts{from}&access_token=%s" % token)
    comment_id=[]
    for information in res.json()['data']:
        if information['id'] == post_id:
            if 'message' in information:
                user_information = {}
                user_information['comment'] = {}
                user_information['comment']['data'] = []
                
            else:
                user_information['content'] = "NO MESSAGE"
            for i in information['comments']['data']:
                comment_id.append(i['from']['id'])
            if 'next' in information['comments']['paging']:
                res_1 = requests.get(information['comments']['paging']['next'])
                while 'next' in res_1.json()['paging']:
                    try:
                        for i in res_1.json()['data']:
                            comment_list.append(i['from']['id'])
                        res_1 = requests.get(res_1.json()['paging']['next'])
                    except:
                        pass
            else:
                pass
    return comment_id


def get_sharedposts_id(fanpage_id,post_id):
    token = input('token = ')
    res= requests.get("https://graph.facebook.com/v2.10/"+fanpage_id+"/posts?fields=message,id,comments{from,message},reactions{id,type,name},sharedposts{from}&access_token=%s" % token)
    sharedposts_id=[]
    for information in res.json()['data']:
        if information['id'] == post_id:
            if 'message' in information:
                user_information = {}
                user_information['sharedposts'] = {}
                user_information['sharedposts']['data'] = []
                
            else:
                user_information['content'] = "NO MESSAGE"
            for i in information['sharedposts']['data']:
                sharedposts_id.append(i['from']['id'])
    return sharedposts_id
