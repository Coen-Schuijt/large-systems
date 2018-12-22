# Large-systems

This repository contains the necessary files and folders for setting up the test environment as part of the Large System course for the OS3 masters (also known as Securty and Network Engineering).


## Usage

The general syntax for running the measurement scripts is as follows:
./measure-deployment-delay-[framework].py [instances] [application name] [dstat output] > [stdout output]

For Kubernetes:
```bash
./kubernetes/measure-deployment-delay-kubernetes.py 10 nginx nginx_yaml/nginx-deployment-10.yml /var/log/dstat/performance_measurements_10_1.csv > /var/log/dstat/performance_measurements_10_1.log
```

For Mesos:
```bash
./mesos/measure-deployment-delay-mesos.py 10 nginx nginx_json/nginx_deployment-10.json /var/log/dstat/performance_measurement_10_1.csv > var/log/dstat/performance_measurements_10_1.log
```

Both scripts rely on the fact that an ed25519 ssh keypair has been created for the server running the script, in the following directory:
```bash
/root/.ssh/remote
```

And the fact that the pulbic key has been added to the '/root/.ssh/autorized_keys' file of any other node.


## Adding a framework

To add a framework, copy the 'kubernetes/measure-deployment-delay-kubernetes.py' file and:
```bash
1. Replace the command to delete deployment and/or running pods @[lines 27-28]
2. Replace the command to deploy new instances based on a file @[line 34]
3. Replace ip address of local node @[line 59] and @[line 66]
4. Replace the command that polls for Running instances @[line 80]
5. Change ip addresses own and slave nodes @[lines 102-105]
```
