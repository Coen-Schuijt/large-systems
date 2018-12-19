#!/usr/bin/env python3

import os
import sys

def get_args():
    """Gets the arguments from the command line"""
    try:
        path = sys.argv[1]
        return path
    except:
        print("Wrong arguments. Usage:\n./parse.py dir\ndir = Relative path to csv files")
        sys.exit(1)

def return_seconds(item):
    """
    Function that splits the first part of the time mesurements, and returns the result in seconds.
    Takes  : Time measurement in the format [mm:ss.ffffff]
    Returns: Time measurement in the format   [sss.ffffff]
    """

    # Parse minutes and seconds
    minutes = item[0:2]
    int_minutes = int(minutes)
    seconds = item[3:5]
    int_seconds = int(seconds)
    
    # Everything after the comma, to be concatenated later.
    res_stripped = item[5:]

    # If there are minutes, add them to seconds
    if int(minutes) > 0:
        int_seconds += int_minutes*60
        res_in_seconds = str(int_seconds) + res_stripped
        return res_in_seconds
    # Otherwise, strip the zero
    elif int(minutes) == 0:
        res_in_seconds = str(int_seconds) + res_stripped
        return res_in_seconds

def calculate_average(array):
    """
    Calculates the average of a given array.
    Takes   : An array of a given length
    Returns : The average of the items in the array
    """

    # Initialize empty variable
    result = 0
    for item in array:
        result += float(item)
    final_result = result/len(array)
    return final_result

def parser(path):
    """
    Reads all the log files in the provided path and parses the time measurement results accordingly.
    Takes   : Relative pat to the log files
    Returns : Several arrays with parsed results
    """
   
    # Initialize empty arrays
    total_arr_10 = []
    docker_arr_10 = []
    orchestration_arr_10 = []
    total_arr_100 = []
    docker_arr_100 = []
    orchestration_arr_100 = []
    total_arr_200 = []
    docker_arr_200 = []
    orchestration_arr_200 = []

    # Search for log files and parse the results
    for entry in os.listdir(path):
        if entry.endswith('.log'):
            if '_10_' in entry:
                with open(path + '/' + entry, 'r') as f_10:
                    data = f_10.readlines()
                    stripped_data = data[-3:]
                    for e,item in enumerate(stripped_data):
                        result_10 = item.replace('\n','')
                        before_comma_10 = result_10[-12:]
                        result_10 = return_seconds(before_comma_10)
                        if e == 0:
                            total_arr_10.append(result_10)
                        elif e == 1:
                            docker_arr_10.append(result_10)
                        elif e == 2:
                            orchestration_arr_10.append(result_10)
            elif '_100_' in entry:
                with open(path + '/' + entry, 'r') as f_100:
                    data = f_100.readlines()
                    stripped_data = data[-3:]
                    for e,item in enumerate(stripped_data):
                        result_100 = item.replace('\n','')
                        before_comma_100 = result_100[-12:]
                        result_100 = return_seconds(before_comma_100)
                        if e == 0:
                            total_arr_100.append(result_100)
                        elif e == 1:
                            docker_arr_100.append(result_100)
                        elif e == 2:
                             orchestration_arr_100.append(result_100)
            elif '_200_' in entry:
                with open(path + '/' + entry, 'r') as f_200:
                    data = f_200.readlines()
                    stripped_data = data[-3:]
                    for e,item in enumerate(stripped_data):
                        result_200 = item.replace('\n','')
                        before_comma_200 = result_200[-12:]
                        result_200 = return_seconds(before_comma_200)                        
                        if e == 0:
                            total_arr_200.append(result_200)
                        elif e == 1:
                            docker_arr_200.append(result_200)
                        elif e == 2:
                            orchestration_arr_200.append(result_200)

    return total_arr_10, docker_arr_10, orchestration_arr_10, total_arr_100, docker_arr_100, orchestration_arr_100, total_arr_200, docker_arr_200, orchestration_arr_200

if __name__ == "__main__":
    path = get_args()
    
    total_arr_10, docker_arr_10, orchestration_arr_10, total_arr_100, docker_arr_100, orchestration_arr_100, total_arr_200, docker_arr_200, orchestration_arr_200 = parser(path)

    print("Totals ---------- 10: ", total_arr_10)
    print("Docker ---------- 10: ", docker_arr_10)
    print("Orchestration --- 10: ", orchestration_arr_10)
    print("Totals --------- 100: ", total_arr_100)
    print("Docker --------- 100: ", docker_arr_100)
    print("Orchestration -- 100: ", orchestration_arr_100)
    print("Totals --------- 200: ", total_arr_200)
    print("Docker --------- 200: ", docker_arr_200)
    print("Orchestration -- 200: ", orchestration_arr_200,'\n')

    avg_total_arr_10 = calculate_average(total_arr_10)
    avg_docker_arr_10 = calculate_average(docker_arr_10)
    avg_orchestration_arr_10 = calculate_average(orchestration_arr_10)
    avg_total_arr_100 = calculate_average(total_arr_100)
    avg_docker_arr_100 = calculate_average(docker_arr_100)
    avg_orchestration_arr_100 = calculate_average(orchestration_arr_100)
    avg_total_arr_200 = calculate_average(total_arr_200)
    avg_docker_arr_200 = calculate_average(docker_arr_200)
    avg_orchestration_arr_200 = calculate_average(orchestration_arr_200)

    print("Average Total ----------- 10: ", avg_total_arr_10)
    print("Average Docker ---------- 10: ", avg_docker_arr_10)
    print("Average Orchestration --- 10: ", avg_orchestration_arr_10)
    print("Average Total ---------- 100: ", avg_total_arr_100)
    print("Average Docker --------- 100: ", avg_docker_arr_100)
    print("Average Orchestration -- 100: ", avg_orchestration_arr_100)
    print("Average Total ---------- 200: ", avg_total_arr_200)
    print("Average Total ---------- 200: ", avg_docker_arr_200)
    print("Average Total ---------- 200: ", avg_orchestration_arr_200)
