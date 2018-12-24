#!/usr/bin/env python3

import os
import sys
import datetime
import argparse
import subprocess

def get_args():
    """
    Function : Gets arguments from the command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("replicas", type=str, help="Specifies the number of replicas")
    parser.add_argument("application", help="Specifies the application name")
    parser.add_argument("yaml", help="Relative path + yaml filename (e.g. ../nginx_yaml/nginx-deployment-10.yml)")
    parser.add_argument("outfile", help="Absolute path + filename (e.g. /var/log/dstat/nginx-deployment-10.csv)")
    args = parser.parse_args()
    return args.replicas, args.application, args.yaml, args.outfile

def current_time():
    """
    Function : Returns the current time
    """
    current = datetime.datetime.now()
    return current

def shutdown(application):
    """
    Function : Used to shut down any running application instances
    Takes    : Application name
    Returns  : Timestamp after shutdown command
    """
    os.system("kubectl delete deployment.apps/{}".format(application))
    os.system("kubectl delete pods --selector=app={}".format(application))
    after_shutdown = current_time()
    return after_shutdown

def deploy(yaml):
    """
    Function : Deploys application instances and returns timestamp after deployment command
    Takes    : Relative path to YAML file with instructions
    Returns  : Timestamp after deploy command
    """
    before_deploy_command = current_time()
    os.system("kubectl create -f {}".format(yaml))
    after_deploy_command = current_time()
    return after_deploy_command

def start_resource_monitor(server_definition,outfile):
    """
    Function : Starts resource monitring
    Takes    : List of server:port combination, output file name 
    """
    for server,port in server_definition.items():
#        print("Server: ", server)
#        print("Port  : ", port)
        
        os.system("ssh -i /root/.ssh/remote/id_ed25519 root@{0} -p {1} 'dstat -cdmnyg --disk-util --disk-tps --output {2} < /dev/null > /dev/null 2>&1 &'".format(server,port,outfile))

def stop_resource_monitor(server_definition):
    """
    Function : Gathers PID's for dstat processes on servers and kills those processes
    Takes    : List of server:port combinations
    """
    first = '{print "kill " $1}'
    for server,port in server_definition.items():
        pid = subprocess.check_output("ssh -i /root/.ssh/remote/id_ed25519 root@{0} -p {1} ps -axf | grep dstat | grep -v grep | awk '{2}'".format(server,port,first), shell=True)
        
        pid_decoded = pid.decode("utf-8")
        pid_str = str(pid_decoded)
        
#        print("Pid", pid_str)

        pid_splitted = pid_str.split("\n")
        del pid_splitted[-1]
#        print("Pid splitted", pid_splitted)

        if server == "145.100.104.110":
            del pid_splitted[0]
        else:
            pass

        for item in pid_splitted:
            command = ''
            if server != "145.100.104.110":
                command = "ssh -i /root/.ssh/remote/id_ed25519 root@{0} -p {1} ".format(server,port) 
            #print(command + "{0}".format(item))

            os.system(command + "{0}".format(item))

#            os.system("ssh -i /root/.ssh/remote/id_ed25519 root@{0} -p {1} {2}".format(item))
#            print(server)
#            print(item)

def monitor_replicas(amount,application):
    """
    Function : Monitors the amount of application instances in 'running' state
    Takes    : Amount of application instances to check for, application instance name
    """
    before_monitor = current_time()
    while True:
        output = subprocess.check_output("kubectl get pods --selector=app={} --field-selector=status.phase=Running | tail -n +2 | wc -l".format(application), shell=True)
        
        output_decoded = output.decode("utf-8").strip('\n')
        output_int = int(output_decoded)

#        print(output_int)

        if output_int == 0:
            zero_containers_timestamp = current_time()
#            print(zero_containers_timestamp)
        if output_int > 0:
            one_container_timestamp = current_time()
#            print(one_container_timestamp)

        if output_int == int(amount):
#            print("Match", current_time())
            return zero_containers_timestamp, one_container_timestamp

if __name__ == "__main__":

    # Define server variables:
    server_definition = {
                            "145.100.104.111":"22286",
                            "145.100.104.110":"22",
                            "145.100.104.51":"22",
                            "145.100.104.50":"22",
                        }
    
    # Parse arguments
    replicas,application,yaml,outfile = get_args()

    # [t0] Start time measurements
    t0 = current_time()
    print("[t0] Main Start                 : ", t0)

    # [t1] Delete the deployment and all running copies
    t1 = shutdown(application)
    print("[t1] After Shutdown             : ", t1)

    # [t2] Execute deployment > Saves: actual time after executing the command
    t2 = deploy(yaml)
    print("[t2] After Command Exec         : ", t2)

    # Start monitoring resources on all servers
    start_resource_monitor(server_definition,outfile)

    # [t4][t5] Monitor ammount of deployments > Saves: timestamps of zero and one container(s) active
    t3,t4 = monitor_replicas(replicas,application)
    print("[t3] Last Clock Cycle           : ", t3)
    print("[t4] First Application Instance : ", t4)

    # Stop monitoring resources on all servers
    stop_resource_monitor(server_definition)
    
    # [t5] Stop time measurements
    t5 = current_time()                
    print("[t5] All applications Running   : ", t5)

    # [t5-t2] Orchestration + Docker Delay
    total_delay = t5 - t2
    print("Total Delay                     : ", total_delay)

    # [t5-t3] Docker Delay
    docker_delay = t5 - t3
    print("Docker Delay                    : ", docker_delay)

    # [t3-t2] Orchestration Delay
    orchestration_delay = t3 - t2
    print("Orchestration Delay             : ", orchestration_delay)
