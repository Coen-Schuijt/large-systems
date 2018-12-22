#!/usr/bin/env python3

import os
import sys
import datetime
import subprocess

def get_args():
    try:
        replicas = sys.argv[1]
        str_replicas = str(replicas)

        application = sys.argv[2]
        yaml = sys.argv[3]

        outfile = sys.argv[4]
        return str_replicas, application, yaml, outfile
    except:
        print("Wrong arguments. Usage:\n./spinup-deployment-delay.py rep app yml out\nrep = Amount of replicas\napp = Application name\nyml = Relative path to yaml file\nout = Absolute path + filename (e.g. /root/performance_measurements_7.csv)")
        sys.exit(1)

def current_time():
    current = datetime.datetime.now()
    return current

def shutdown(application):
    os.system("kubectl delete deployment.apps/{}".format(application))
    os.system("kubectl delete pods --selector=app={}".format(application))
    after_shutdown = current_time()
    return after_shutdown

def deploy(yaml):
    before_deploy_command = current_time()
    os.system("kubectl create -f {}".format(yaml))
    after_deploy_command = current_time()
    return after_deploy_command

def start_resource_monitor(server_definition,outfile):
    for server,port in server_definition.items():
#        print("Server: ", server)
#        print("Port  : ", port)
        
        os.system("ssh -i /root/.ssh/remote/id_ed25519 root@{0} -p {1} 'dstat -cdmnyg --disk-util --disk-tps --output {2} < /dev/null > /dev/null 2>&1 &'".format(server,port,outfile))

def stop_resource_monitor(server_definition):
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
