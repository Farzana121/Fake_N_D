# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 10:36:01 2019
Creates Data Set as files from CSV
@author: Dell
reads titles from csv and prepares files
"""
import csv

with open('f:/dataset_fake.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            out_file = open(f'f:/TitleFake/{row[0]}.txt', 'w', encoding='utf-8')
            out_file.write(row[1])
            line_count += 1
    print(f'total {line_count}.')

with open('f:/dataset_real.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            out_file = open(f'f:/TitleReal/{row[0]}.txt', 'w', encoding='utf-8')
            out_file.write(row[1])
            line_count += 1
    print(f'total {line_count}.')