#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 11:39:33 2021

@author: bizzy
"""
# https://www.data.go.kr/data/15085787/openapi.do

import requests


def Entry():
    url = 'http://apis.data.go.kr/1262000/CountryOverseasArrivalsService/getCountryOverseasArrivalsList'
    params ={
        'serviceKey' : "Sk4Syk+ddhdzDzSKdby8eRCdDfe912d+TxPmhp7Uq2UoxKrXMqgSQDv1vLQsOknyyNqHVICzTmwubry2uL7vig==",
        'pageNo': 1,
        'numOfRows': 200
    }
    
    response = requests.get(url, params=params)
    response_text = response.text
    response_text_dict = eval(response_text)
    EntryRequirement = response_text_dict['data']
    
    for er in EntryRequirement:
        er['country_name'] = er.pop('country_eng_nm')
        er['entry_requirement'] = er.pop('txt_origin_cn')
        er.pop('country_nm')
        er.pop('html_origin_cn')
        er.pop('notice_id')
        er.pop('title')
    
    return EntryRequirement


