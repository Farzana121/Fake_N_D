# -*- coding: utf-8 -*-
import csv



with open('f:/dataset_fake.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} dsfjksd {row[1]}')
            line_count += 1
        print(f'total {line_count}.')