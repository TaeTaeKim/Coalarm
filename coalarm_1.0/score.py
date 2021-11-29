#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 10:45:31 2021

@author: krc
"""


import pymysql

conn = pymysql.connect(host='13.209.17.131', user="coalarm", password="coalarm", db="coalarm", charset="utf8")
cur = conn.cursor()
# cur.execute('TRUNCATE TABLE corona_data') # 테이블 레코드 비우기
' ec2-13-209-17-131.ap-northeast-2.compute.amazonaws.com'
