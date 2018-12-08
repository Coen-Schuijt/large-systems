#!/usr/bin/env python3

import os
import sys
import datetime
import subprocess

def get_args():
    replicas = sys.argv[1]
    str_replicas = str(replicas)

    application = sys.argv[2]
    yaml = sys.argv[3]

    return str_replicas, application, yaml

def current_time():
    current = datetime.datetime.now()
    return current

def shutdown(application):
    os.system("kubectl delete deployment.apps/{}".format(application))
    os.system("kubectl delete pods --selector=app={}".format(application))

def deploy(yaml):
    before_deploy_command = current_time()
    os.system("kubectl create -f {}".format(yaml))
    after_deploy_command = current_time()

    return after_deploy_command

def monitor(amount,application):

    before_monitor = current_time()
    while True:
        output = subprocess.check_output("kubectl get pods --selector=app={} --field-selector=status.phase=Running | tail -n +2 | wc -l".format(application), shell=True)

        str_output = output.decode("utf-8").strip('\n')
        int_output = int(str_output)

        if int_output == 0:
            zero_containers_timestamp = current_time()
#            print(zero_containers_timestamp)
        if int_output == 1:
            one_container_timestamp = current_time()
#            print(one_container_timestamp)

        if int_output == int(amount):
#            print("Match", current_time())
            return zero_containers_timestamp, one_container_timestamp

if __name__ == "__main__":

    # 1. Parse arguments
    replicas,application,yaml = get_args()

    # 2. Delete the deployment and all running copies
    shutdown(application)
    
    # 3. Start time measurements
#    main_start = current_time()
    
#    print("Main Start    : ", main_start)

    # 4. Execute deployment > Saves: actual time after executing the command
    after_deploy_command = deploy(yaml)
    print(after_deploy_command)

    # 5. Monitor ammount of deployments > Saves: timestamps of zero and one container(s) active
    zero_containers_timestamp,one_container_timestamp = monitor(replicas,application)

    print(zero_containers_timestamp)
    print(one_container_timestamp)

    # 6. Stop time measurements
#    main_after = current_time()                                   

    # 7. Measure startup delay
    difference_zero_to_one = one_container_timestamp - zero_containers_timestamp
    print("Diff zero to one: ", difference_zero_to_one)

    difference_cmd_to_one = one_container_timestamp - after_deploy_command
    print("Diff cmd to one:  ", difference_cmd_to_one)

    final_delay = difference_cmd_to_one - difference_zero_to_one

    # 8. Print delay
    print("Startup Delay :   ", final_delay)
    
