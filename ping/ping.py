import os
import subprocess
import socket

serverlist = []
active = []
down = []

#replace file.txt with domain list text file
with open("file.txt") as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

for line in lines:
    try:
        #convert domain name to IP for later longitude and latitude calculation, its also more convinient for grep
        ipaddr = socket.gethostbyname(line)
        serverlist.append(ipaddr)
    #catch the socket error, as some domains in the dataset will fail to ping
    except socket.gaierror:
        continue


        
for ip in serverlist:
    #ping 3 packets
    response = os.system("ping -c 3 " + ip)
    print("****")
    if response == 0:
        active.append(ip)
    else:
        down.append(ip)

for ip in active:
    #for easier grep
    print(ip, "is active")
