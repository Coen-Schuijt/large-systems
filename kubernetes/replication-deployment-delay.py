#!/usr/bin/env python3

import os
import sys
import datetime
import subprocess

def get_args():
    replicas = sys.argv[1]
    str_replicas = str(replicas)

    application = sys.argv[2]

    return str_replicas, application

def current_time():
    current = datetime.datetime.now()
    return current

def deploy(amount):
    before_deploy = current_time()
    os.system("kubectl scale deployment nginx --replicas={}".format(amount))
    after_deploy = current_time()

    command_execution_time = after_deploy - before_deploy
    return command_execution_time

def monitor(amount,application):

    before_monitor = current_time()
    while True:
        output = subprocess.check_output("kubectl get pods --selector=app={} --field-selector=status.phase=Running | tail -n +2 | wc -l".format(application), shell=True)

        str_output = output.decode("utf-8").strip('\n')
        int_output = int(str_output)

        if int_output == int(amount):
#            print("Match", current_time())
            break

if __name__ == "__main__":
    replicas,application = get_args()

    main_start = current_time()
    print("Main Start    : ", main_start)

    command_execution_time = deploy(replicas)
    
    monitor(replicas,application)
    
    main_after = current_time()
#    print("Main After    : ", main_after)

    difference_main = main_after - main_start
    total = difference_main - command_execution_time

    print("Startup Delay : ", total)
    
