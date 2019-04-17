#SSH connection for school project
#Halmstad Högskola
#2019
#Tim Oskarsson and Johan Knutsson
#SSH connect with paramiko
#HejHej
import paramiko
import time
import getpass
import os
import colorama 
from colorama import Fore, Style 
from confTemplates import *

#Creds
servIP = "192.168.1.1"#input("IP: ")
usrname = "user"#input("Username: ")
passwd = "cisco123"#getpass.getpass("Password: ")#input("Password: ")

#SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Auto add keys
ssh.connect(servIP, port=22, username=usrname, password=passwd) #Connection formating
print(Fore.GREEN + "Connection made to ", servIP)

#Make shell
#Show the login splash/banner
sshshell = ssh.invoke_shell()
splash = sshshell.recv(65535)
time.sleep(1) #Sleep to account for latency 
print(splash.decode())

#Basic pre-loop configs
sshshell.send('enable\n') #Enable router
sshshell.send('terminal length 0\n') #Infinte terminal length
sshshell.send('conf t\n')
print(Fore.GREEN + "Terminal enabled")
print(Fore.GREEN + "Terminal length 0")
print(Fore.GREEN + "Config mode")

#Dictionary binds configs to numbers
config_list = {
	'1': basic_config,
	'2': service_security,
}


#Command loop
while True:
	#Interface
	print()
	print(Fore.YELLOW +"#######################################################") 
	print(Fore.GREEN +"Pick a thing: Q or 'quit' to exit") 
	print(Fore.CYAN +"1: Basic Settings 2: Service Security")
	print(Fore.YELLOW +"#######################################################")	
	
	#User command
	cmand = input("#: ")
	if cmand == 'quit' or cmand == 'q':
		ssh.close()
		break
	config_list[cmand]()
		
	#Decode and print outputs
	output = sshshell.recv(65535)
	printout = output.decode(encoding='UTF-8')
	print(printout)

	#Save output to file
	print_file = output.decode(encoding='UTF-8')
	file_save = open('output.txt', 'a')
	file_save.write(print_file)
