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
		ipconf = input("Set ip addresses? Y/N ")
		if ipconf == "y":
				while True:
					interfaceQ = input("Enter the interface you want to configure (q) to quit: ")
					if interfaceQ == "q":
						break
					else:
						interfaceA = "interface " + interfaceQ
						print(interfaceA)

						ipQ = input("Enter wanted IP address with a proper netmask: ")
						ipA = 'ip address ' + ipQ
						print(ipA)

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
						sshshell.send('switchport port-security\n')
						sshshell.send('switchport port-security mac-address sticky\n')
						sshshell.send('switchport port-security maximum 2\n')					    							
						sshshell.send('switchport mode access\n')
						sshshell.send('shut\n')
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
		print(Style.RESET_ALL)
		sshshell.send('no cdp run\n')
		sshshell.send('no ip bootp server\n')
		sshshell.send('no ip arp proxy\n')
		sshshell.send('no ip http server\n')
		sshshell.send('no ip icmp redirect\n')
		sshshell.send('do show ip int br\n')
		time.sleep(1) #Wait for buffer

def ospf_setup():
		

		print('\n')
		open(".parsefile", 'w').close() #clear parsefile

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

def AAA():
		output = sshshell.recv(65535)
		printout = output.decode(encoding='UTF-8')
		print("###Setup for AAA with radius authentication###")
		aaaQ = input("Add username /w encrypted password, Y/N? ")
		if aaaQ == 'y' or aaaQ == 'Y':
			aaaU = input("Please enter username: ")
			aaaP = input("Please enter password, it will be encrypted using Type 9 hasing algorithm: ")
			aaaUPformat = "username " + aaaU + " algorithm-type scrypt secret " + aaaP + "\n"
			sshshell.send(aaaUPformat)
			timesleep(.5)
			print(printout)
		else:
			return
        
            
		print("aaa new model")
		print("aaa authentication login default group radius none")
		print("###Do not forget to validate Radius configurations before proceeding###")
		radiusU = input("Please enter the name of Radius server to enter Radius-config, used for this device only: ")
		radiusUformat = "radius server " + radiusU + "\n"
		sshshell.send(radiusUformat)
		print(printout)

		radiusS = input("Please enter IP address of the Radius server: ")
		print("address ipv4 " + radiusS + " " + "auth-port 1812 acct-port 1813")
		radiusSformat = "address ipv4 " + radiusS + " " + "auth-port 1812 acct-port 1813\n"
		sshshell.send(radiusSformat)
		        
		time.sleep(0.3)
		print(printout)

		radiusK = input("Please enter the Key/password for the radius server: ")
		radiusKformat = "key " + radiusK
		sshshell.send(radiusKformat)
		print("key " + radiusK)
		time.sleep(0.3)
		print(printout)

def IProute():
		output = sshshell.recv(65535)
		printout = output.decode(encoding='UTF-8')
		
		print()
		print(Fore.YELLOW +"#######################################################") 
		print(Fore.GREEN +"Pick a option for setting route: Q or 'quit' to exit") 
		print(Fore.CYAN +"1: Static 2: Default static")
		print(Fore.YELLOW +"#######################################################")	
		print(Style.RESET_ALL)	
		while True:
			routeNav = input("1 or 2?: ")
			if routeNav == 'quit' or routeNav == 'q':
				quit()		
			if routeNav == "1":
				routeS = input("Enter wanted destination address for static route with proper netmask: ")
				routeI = input("Enter exit inteface: ")
				routeSIformat = "ip route " + routeS + " " + routeI + "\n"
				sshshell.send(routeSIformat)
				time.sleep(.5)
				break
			if routeNav == "2":
				time.sleep(1)
				routeS2 = input("Enter exit interface for default static route: ")
				routeS2format = "ip route 0.0.0.0 0.0.0.0 " + routeS2 + "\n"
				sshshell.send(routeS2format)
				time.sleep(.5)
				break
			else:
				break

			output = sshshell.recv(65535)
			printout = output.decode(encoding='UTF-8')

def int_IPconf():
		while True:
			interfaceQ = input("Enter the interface you want to configure (q) to quit: ")
			if interfaceQ == "q":
				break
			else:
				interfaceA = "interface " + interfaceQ
				print(interfaceA)
				ipQ = input("Enter wanted IP address with a proper netmask: ")
				ipA = 'ip address ' + ipQ
				print(ipA)

#Creds
servIP = "192.168.1.2"#input("IP: ")
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
printout = splash.decode(encoding='UTF-8')
time.sleep(1) #Sleep to account for latency 

#Basic pre-loop configs
sshshell.send('enable\n') #Enable router
sshshell.send('terminal length 0\n') #Infinte terminal length
sshshell.send('conf t\n')
time.sleep(1)

print(Fore.YELLOW + "#####################")
print(Fore.YELLOW + "# " + Fore.GREEN +"Terminal enabled" + Fore.YELLOW +"  #")
print(Fore.YELLOW + "# " + Fore.GREEN + "Terminal length 0" + Fore.YELLOW + " #")
print(Fore.YELLOW + "# " + Fore.GREEN + "Config mode" + Fore.YELLOW +"       #")
print(Fore.YELLOW + "#####################")
print(Style.RESET_ALL)
print(printout)

#Dictionary binds configs to numbers
config_list = {
	'1': basic_config,
	'2': service_security,
	'3': ospf_setup,
	'4': AAA,
	'5': IProute,
	'6': int_IPconf,
}


#Command loop
while True:
	#Interface
	print()
	print(Fore.YELLOW +"#######################################################") 
	print(Fore.GREEN +"Pick a thing: Q or 'quit' to exit") 
	print(Fore.CYAN +"1: Basic Settings 2: Port/Service Security 3: OSPF")
	print(Fore.CYAN +"4: AAA            5: Routing               6: IP config")
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
