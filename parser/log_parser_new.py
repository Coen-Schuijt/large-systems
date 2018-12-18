#!/usr/bin/env python3

import os
import csv
import sys
import pandas as pd

def get_args():
    try:
        path = sys.argv[1]
        return path
    except:
        print("Wrong arguments. Usage:\n./parse.py dir\ndir = Relative path to csv files")
        sys.exit(1)

def create_df(data):
    df = pd.Dataframe(data)

def parser(path):
    
    total_arr_10 = []
    docker_arr_10 = []
    orchestration_arr_10 = []
    
    total_arr_100 = []
    docker_arr_100 = []
    orchestration_arr_100 = []

    total_arr_200 = []
    docker_arr_200 = []
    orchestration_arr_200 = []

    repl = ['_10_', '_100_', '_200_']

    for entry in os.listdir(path):
        if entry.endswith('.log'):
            for i in repl:
                if i in entry:
                    with open(path + '/' + entry, 'r') as f:
                        data = f.readlines()
                        test = data[-3:]
                        for e,item in enumerate(test):
                            result = item.replace('\n','')
                            res = result[-8:]
                            if e == 0:
                                arr = 'total_arr{}'.format(i[-1:])
                                arr.append(res)
                            elif e == 1:
                                arr = 'docker_arr{}'.format(i[-1])
                                arr.append(res)
                            elif e == 2:
                                arr = 'orchestration_arr{}'.format(i[-1])
                                arr.append(res)

            if '_100_' in entry:
                with open(path + '/' + entry, 'r') as f:
                    data = f.readlines()
                    test = data[-3:]
                    for e,item in enumerate(test):
                        result = item.replace('\n','')
                        res = result[-8:]
                        if e == 0:
                            total_arr_100.append(res)
                        elif e == 1:
                            docker_arr_100.append(res)
                        elif e == 2:
                            orchestration_arr_100.append(res)

            if '_200_' in entry:
                with open(path + '/' + entry, 'r') as f:
                    data = f.readlines()
                    test = data[-3:]
                    for e,item in enumerate(test):
                        result = item.replace('\n','')
                        res = result[-8:]
                        if e == 0:
                            total_arr_100.append(res)
                        elif e == 1:
                            docker_arr_100.append(res)
                        elif e == 2:
                            orchestration_arr_100.append(res)
            

    print("Totals:        ", total_arr)
    print("Docker:        ", docker_arr)
    print("Orchestration: ", orchestration_arr)


if __name__ == "__main__":
    path = get_args()
    parser(path)
