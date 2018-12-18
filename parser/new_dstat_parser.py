#!/usr/bin/env python3

import os
import csv
import sys

def get_args():
    try:
        path = sys.argv[1]
        return path
    except:
        print("Wrong arguments. Usage:\n./parse.py dir\ndir = Relative path to csv files")
        sys.exit(1)

def parser(path):
    for entry in os.listdir(path):
        if entry.endswith('.csv'):
            if '_10_' in entry:
 
                x_arr = []
                y_arr = []

                with open(path + '/' + entry, 'r') as f:
                    length = 0
                    for _ in range(6):
                       next(f)

                    data = csv.reader(f, delimiter=',')

                    for e,row in enumerate(data):
                        print(e,row)
                        length += 1

if __name__ == "__main__":
    path = get_args()
    parser(path)
