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

def rmv_prep_zero(item):
    if item.startswith('0'):
        item_no_prep_zero = item[1:]
    return item_no_prep_zero

def min_to_sec(item):
    return

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

    for entry in os.listdir(path):
        if entry.endswith('.log'):
            if '_10_' in entry:
                with open(path + '/' + entry, 'r') as f_10:
                    data = f_10.readlines()
                    stripped_data = data[-3:]
                    for e,item in enumerate(stripped_data):
                        result_10 = item.replace('\n','')
                        seconds_10 = result_10[-9:]

                        res_10 = rmv_prep_zero(seconds_10)

                        if e == 0:
                            total_arr_10.append(res_10)
                        elif e == 1:
                            docker_arr_10.append(res_10)
                        elif e == 2:
                            orchestration_arr_10.append(res_10)
            elif '_100_' in entry:
                with open(path + '/' + entry, 'r') as f_100:
                    data = f_100.readlines()
                    stripped_data = data[-3:]
                    for e,item in enumerate(stripped_data):
                        result_100 = item.replace('\n','')
                        res_100 = result_100[-9:]
       
                        # Check if seconds starts with 0
#                        seconds = res_200[2:4]

                        if e == 0:
                            total_arr_100.append(res_100)
                        elif e == 1:
                            docker_arr_100.append(res_100)
                        elif e == 2:
                            if item.startswith('0'):
                                item = item[:]
                                print(item)
                            else:
                                orchestration_arr_100.append(res_100)

            elif '_200_' in entry:
                with open(path + '/' + entry, 'r') as f_200:
                    data = f_200.readlines()
                    stripped_data = data[-3:]
                    for e,item in enumerate(stripped_data):
                        result_200 = item.replace('\n','')
                        res_200 = result_200[-11:]
        
                        # Extract minutes
                        minutes = res_200[0]
                        int_mins = int(minutes)
                        #print("minutes", minutes)
                        #print(int_mins)

                        # Extract seconds
                        seconds = res_200[2:4]
                        int_secs = int(seconds)
                        #print("seconds", seconds)
                        #print(int_secs)

                        # If there is at least one minute
                        if int_mins > 0:
                            # Multiply the amount of minutes by 60 and add to seconds
                            int_secs += int_mins*60

                        # Split after comma
                        res_200_rmvd_min = res_200[4:]
                        #print("res_200_rmvd_min ", res_200_rmvd_min) 
                        res_200_float = str(int_secs) + res_200_rmvd_min

                        #print(res_200_float)

                        if e == 0:
                            total_arr_200.append(res_200_float)
                        elif e == 1:
                            docker_arr_200.append(res_200_float)
                        elif e == 2:
                            orchestration_arr_200.append(res_200_float)

    print("Totals 10:          ", total_arr_10)
    print("Docker 10:          ", docker_arr_10)
    print("Orchestration 10:   ", orchestration_arr_10,'\n')

    print("Totals 100:         ", total_arr_100)
    print("Docker 100:         ", docker_arr_100)
    print("Orchestration 100:  ", orchestration_arr_100,'\n')

    print("Totals 100:         ", total_arr_200)
    print("Docker 100:         ", docker_arr_200)
    print("Orchestration 100:  ", orchestration_arr_200)

if __name__ == "__main__":
    path = get_args()
    parser(path)
