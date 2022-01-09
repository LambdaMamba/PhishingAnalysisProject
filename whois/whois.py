import os
import subprocess

#replace file.txt with domain list text file
fd = open("file.txt", "r")
serverlist = []
while True:
    line = fd.readline()
    if not line:
        break
    serverlist.append(line)

        
for ip in serverlist:
    response = os.system("whois " + ip)
