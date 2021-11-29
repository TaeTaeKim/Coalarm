#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 07:59:09 2021

@author: bizzy
"""
import csv


def geochart_iso_from_csv():
    with open('geochart_iso.csv', 'r') as f: 
        reader = csv.reader(f) 
        for line in reader: 
            countries = line 
    return countries
