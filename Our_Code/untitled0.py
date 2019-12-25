# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 10:36:01 2019

@author: Dell
"""


with open('f:/dataset_fake.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            out_file = open(f'f:/DataSetFake/{row[0]}.txt', 'w', encoding='utf-8')
            out_file.write(row[1] + '\n' + row[2])
            line_count += 1
    print(f'total {line_count}.')

with open('f:/dataset_real.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            out_file = open(f'f:/DataSetReal/{row[0]}.txt', 'w', encoding='utf-8')
            out_file.write(row[1] + '\n' + row[2])
            line_count += 1
    print(f'total {line_count}.')