#SSH connection for school project
#Halmstad Högskola
#2019
#Tim Oskarsson and Johan Knutsson
#SSH connect with paramiko

import paramiko
import time
import datetime
import getpass
import os
import colorama 
from colorama import Fore, Style 
from confTemplates import *

#Time and timestamps
tl = time.localtime()
timeStamp=time.strftime("%a %H:%M:%S \n", tl)

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
		time.sleep(1) #Wait for buffer

def service_security():
	
		def int_parse():
				sshshell.send('do show ip int br\n')
				time.sleep(.5)
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				time.sleep(.5)
				
				parse_file = printout
				parse_print = open(".parsefile", 'w')
				parse_print.write(parse_file)
				parse_print.close()
				
				#Open prasefile to read
				parse_read = open(".parsefile", 'r')
				
				#For every line in parsefile look for string, print interface
				intlist = []
				incr = 0
				for line in parse_read:
						if "down" in line:
							intlist.append(line.split(' ', 1)[0])
							intout = ("Interface " + intlist[incr])
							time.sleep(.3)
							print(intout)
							sshshell.send(str(intout))
							sshshell.send('\n')
							#switchMAC = input("Set MAC security to sticky Y/N? ")
							#if switchMAC == "y":
							sshshell.send('switchport port-security\n')
							sshshell.send('switchport port-security mac-address sticky\n')
							sshshell.send('switchport port-security maximum 2\n')
							#if switchMAC == "n":
							#	continue					    							
						    sshshell.send('switchport mode access\n')
							sshshell.send('shut\n')
							#print(printout)
							incr += 1
				return

				print('\n')
				open(".parsefile", 'w').close() #clear parsefile


		print(Fore.MAGENTA + "Interfaces in the Down state will be detected")
		print(Style.RESET_ALL)
		portsec = input("Shut down unused ports? Y/N:  ")
		if portsec == "quit" or portsec == 'q':
			return
		if portsec == "y":
			int_parse()
		else:
			sshshell.send("\n")
			time.sleep(.2)
			
		print(Fore.MAGENTA + "Shuting down processes...")
		sshshell.send('no cdp run\n')
		sshshell.send('no ip bootp server\n')
		sshshell.send('no ip arp proxy\n')
		sshshell.send('no ip http server\n')
		sshshell.send('no ip icmp redirect\n')
		sshshell.send('do show ip int br\n')
		#sshshell.send("exit\n")
		time.sleep(1) #Wait for buffer

def ospf_setup():
		

		print('\n')
		open(".parsefile", 'w').close() #clear parsefile
				
		#print("at files")
		output = sshshell.recv(65535)
		print_file = output.decode(encoding='UTF-8')
		file_save = open('output.txt', 'a+')
		file_save.write('\n' + timeStamp + print_file + '\n')

		ospfAS = input("OSPF AS number: ")
		ospfformat = ("router ospf " + ospfAS)
		sshshell.send(ospfformat)
		sshshell.send('\n')
		time.sleep(.5)

		print()
		print(Fore.YELLOW +"#######################################################") 
		print(Fore.GREEN +"Pick a thing: Q or 'quit' to exit") 
		print(Fore.CYAN +"1: Interface Table 2: Routing Table")
		print(Fore.YELLOW +"#######################################################")	
		print(Style.RESET_ALL)
		
		output = sshshell.recv(65535)
		printout = output.decode(encoding='UTF-8')
		
		
		while True:
			print(printout +'\n')
			ospfNav = input("OSPF# ")
			if ospfNav == 'quit' or ospfNav == 'q':
				quit()		
			if ospfNav == "1":
				sshshell.send("do show ip int br\n")
				time.sleep(.5)
			if ospfNav == "2":
				sshshell.send("do show ip route\n")
				time.sleep(.5)
			
			time.sleep(.5)	
			output = sshshell.recv(65535)
			printout = output.decode(encoding='UTF-8')


#Creds
servIP = "192.168.1.1"#input("IP: ")
usrname = "user"#input("Username: ")
passwd = "cisco123"#getpass.getpass("Password: ")#input("Password: ")

#SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Auto add keys
ssh.connect(servIP, port=22, username=usrname, password=passwd) #Connection formating
print(Fore.MAGENTA + "Connection made to ", servIP)
print(Style.RESET_ALL)

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
print(Fore.YELLOW + "#####################")
print(Fore.YELLOW + "# " + Fore.GREEN +"Terminal enabled" + Fore.YELLOW +"  #")
print(Fore.YELLOW + "# " + Fore.GREEN + "Terminal length 0" + Fore.YELLOW + " #")
print(Fore.YELLOW + "# " + Fore.GREEN + "Config mode" + Fore.YELLOW +"       #")
print(Fore.YELLOW + "#####################")
print(Style.RESET_ALL)

#Dictionary binds configs to numbers
config_list = {
	'1': basic_config,
	'2': service_security,
	'3': ospf_setup,
}


#Command loop
while True:
	
	#Interface
	print()
	print(Fore.YELLOW +"#######################################################") 
	print(Fore.GREEN +"Pick a thing: Q or 'quit' to exit") 
	print(Fore.CYAN +"1: Basic Settings 2: Port/Service Security 3: OSPF")
	print(Fore.YELLOW +"#######################################################")	
	print(Style.RESET_ALL)

	#User command
	cmand = input("#: ")
	if cmand == 'quit' or cmand == 'q':
		sshshell.send('exit\n')
		ssh.close()
		break
	config_list[cmand]()

		
	#Decode and print outputs
	output = sshshell.recv(65535)
	printout = output.decode(encoding='UTF-8')
	print(printout)

	#Save output to file
	print_file = output.decode(encoding='UTF-8')
	file_save = open('output.txt', 'a+')
	file_save.write('\n' + timeStamp + print_file + '\n')
