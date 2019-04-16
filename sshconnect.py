#SSH connection for school project
#Halmstad Högskola
#2019
#Tim Oskarsson and Johan Knutsson
#SSH connect with paramiko

import paramiko
import time
import getpass
import os

#Creds
servIP = "192.168.1.1"#input("IP: ")
usrname = "user"#input("Username: ")
passwd = "cisco123"#getpass.getpass("Password: ")#input("Password: ")

#SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Auto add keys
ssh.connect(servIP, port=22, username=usrname, password=passwd) #Connection formating

#Make shell
#Show the login splash/banner
sshshell = ssh.invoke_shell()
splash = sshshell.recv(65535)
time.sleep(1) #Sleep to account for latency 
print(splash.decode())

sshshell.send('enable\n') #Enable router
sshshell.send('terminal length 0\n') #Infinte terminal length
sshshell.send('conf t\n')

def basic_config():
		sshshell.send('no ip domain-lookup\n')
		sshshell.send('service password-encryption\n')
		#Banner
		banner = input("Banner: ")
		bannerformat = ("banner motd #" + banner + "#\n")
		sshshell.send(bannerformat)
		#Line con
		sshshell.send('line con 0\n')
		sshshell.send('logging synchronous\n')

		sshshell.send('exit\n')
		time.sleep(1) #Wait for buffer

def service_security():
		sshshell.send('no cdp run\n')
		sshshell.send('no ip bootp server\n')
		sshshell.send('no ip arp proxy\n')
		sshshell.send('no ip http server\n')
		sshshell.send('no ip icmp redirect\n')
		sshshell.send('exit\n')
		time.sleep(1)

#Dictionary binds configs to numbers
config_list = {
	'1': basic_config,
	'2': service_security,
}
#Command loop
while True:
	#Interface
	print()
	print("#######################################################") 
	print("Pick a thing: Q or 'quit' for quit") 
	print("1: Basic Settings 2: Service Security")
	print("#######################################################")	
	
	#User command
	cmand = input("Command: ")
	if cmand == 'quit' or cmand == 'q':
		ssh.close()
		break
	config_list[cmand]()
	
	#Send commands, This is old. 
	#sshshell.send(cmand) #Our command
	#sshshell.send('\n')#New line

	
	#Decode and print outputs
	output = sshshell.recv(65535)
	printout = output.decode(encoding='UTF-8')
	print(printout)

	#Save output to file
	print_file = output.decode(encoding='UTF-8')
	file_save = open('output.txt', 'a')
	file_save.write(print_file)

	
