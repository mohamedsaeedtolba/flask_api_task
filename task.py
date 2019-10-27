# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 01:58:02 2019

@author: Dell
"""

import pandas as pd
import json
from os.path import join, dirname
from ibm_watson import ToneAnalyzerV3
from ibm_watson.tone_analyzer_v3 import ToneInput
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from googletrans import Translator
from langdetect import detect

data= pd.read_csv('7282_1.csv')

def preprocess(data): 
    
    hotels=data.categories == 'Hotels'
    data=data[hotels]
    data.insert(1, "index", range(21420), True)
    data=data.set_index('index')

    hotels_reviews=data['reviews.text']
    for i in range(len(hotels_reviews)):
        if len(str (data['reviews.text'][i])) > 500:
            #hotels_reviews = data['reviews.text'].drop(data['reviews.text'][i])
            
            del hotels_reviews[i]
    hotels_reviews=hotels_reviews.reset_index(drop=True)
    # remove non feature data that it cant trnslate
    del hotels_reviews[33] 
    del hotels_reviews[36]
    del hotels_reviews[18]
    del hotels_reviews[31]
    del hotels_reviews[30]
    del hotels_reviews[2040]
    del hotels_reviews[2028]
    del hotels_reviews[29]
    del hotels_reviews[2020]
    del hotels_reviews[1582]
    del hotels_reviews[38]
    del hotels_reviews[1578]
    del hotels_reviews[2020]
    del hotels_reviews[2015]
    del hotels_reviews[2026]
    hotels_reviews=hotels_reviews.reset_index(drop=True)
    return (hotels_reviews ,data) 
def translate(hotels_reviews):
    translator = Translator()
    trns=[]
    for i in range (len(hotels_reviews)):
        if detect(hotels_reviews[i]) != 'en':
            trns.append(translator.translate(hotels_reviews[i]))
        else:
            trns.append(hotels_reviews[i])
    return trns    
def tone_analyzer(trns):     
    for i in range(len(trns)):
        if len(str (trns[i])) > 500:
            #data_no_2000 = data['reviews.text'].drop(data['reviews.text'][i])
            del trns[i]
    trns=trns.reset_index(drop=True)
    authenticator = IAMAuthenticator('kh7kDLL9cUzVe3KgjW9sTjvUp5HB5kYB-vuy21D7_za4')
    service = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator)
    service.set_service_url('https://gateway-lon.watsonplatform.net/tone-analyzer/api')

    tone_list=[]
    for i in range(len(trns)):
        print("\ntone_review : ",i)
        utterances = [{
                'text': trns[i],
                'user': 'hotel_visitor'
                 } ]
        tone_chat= service.tone_chat(utterances).get_result()
        tone_list.append(tone_chat)
        print(json.dumps(tone_chat, indent=2))
    return tone_list    
        
'''
    score_list=[]
    for i in range(len(tone_list)):
        score_list.append(tone_list[i]['utterances_tone'][0]['tones']) 
    return score_list
        '''
   


def hotels_search(data):
    print(data.columns)
    name = data['name']
    name =list( dict.fromkeys(name))
    longitude = data['longitude']
    longitude =list( dict.fromkeys(longitude))
    city = data['city']
    city =list( dict.fromkeys(city))
    address = data['address']
    address =list( dict.fromkeys(address))
    latitude = data['latitude']
    latitude =list( dict.fromkeys(latitude))
    postalCode = data['postalCode']
    postalCode =list( dict.fromkeys(postalCode))
    province = data['province']
    province =list( dict.fromkeys(province))
    for colum in data.columns:
        colum = data[colum]
        colum =list( dict.fromkeys(colum))
    hotels=pd.DataFrame({'name': pd.Series(name), 'longitude':pd.Series(longitude),'city':pd.Series(city),'address':pd.Series(address),'latitude':pd.Series(latitude)
    ,'postalCode':pd.Series(postalCode),'province':pd.Series(province)})
    for i in range(299,342):
        hotels = hotels.drop([i], axis=0)
    hotels_names =hotels.set_index('name').T.to_dict('list')
    return hotels_names      # it is  the dictionary contain hotels and its data


def main(x):
    hotels_reviews=preprocess(data)
    #tone_list=tone_analyzer(translate(hotels_reviews))
    #x= input('enter search word or name of hotel  ')
    if str (x) == 'search':
        hotels_search(data)
        #tone_list
    else:
        hotels_names=hotels_search(data)
        print(hotels_names[str(x)])
if __name__ == '__main__':
    main()
        
        
        