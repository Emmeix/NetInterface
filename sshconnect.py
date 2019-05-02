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
from tqdm import tqdm

#Time and timestamps
tl = time.localtime()
timeStamp=time.strftime("%a %H:%M:%S \n", tl)

def int_table():
	sshshell.send("do show ip int br\n")
	print(Fore.MAGENTA +"Fetching table...")
	print(Style.RESET_ALL)
	for i in tqdm(range(30)):
		time.sleep(.1)
def r_table():
	sshshell.send("do show ip route | begin Gateway\n")

def run_conf():
	sshshell.send("do show run\n")
	for i in tqdm(range(30)):
		time.sleep(.1)

def ip_prot():
	sshshell.send("do show ip prot\n")

def sh_vlan():
	sshshell.send("do show vlan br\n")

def sh_trunk():
	sshshell.send("do show int trunk\n")

def sh_eth():
	sshshell.send("do show etherchannel br\n")	

def ospf_neigh():
	sshshell.send("do show ip ospf neigh\n")

def arp_table():
	sshshell.send("do show arp\n")

def sh_user():
	sshshell.send("do show users\n")

def sh_dhcp():
	sshshell.send("do show dhcp server\n")
	sshshell.send("do show dhcp lease\n")

def sh_ntp():
	sshshell.send("do show ntp status\n")
	sshshell.send("do show ntp asso\n")
	time.sleep(.2)
	output = sshshell.recv(65535)
	printout = output.decode(encoding='UTF-8')
	print(printout)

def hostnames():
	hostn = input("What hostname for the device do you wish to set? ")
	hostformat = "hostname " + hostn + "\n"
	sshshell.send(hostformat)
	time.sleep(.3)

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
				sshshell.send("do show ip int br\n")
				print(Fore.MAGENTA+"Fetching table..")
				print(Style.RESET_ALL)
				for i in tqdm(range(60)):
					time.sleep(.1)
	
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)
				while True:
					interfaceQ = input("Enter the interface, (q) to quit: ")
					if interfaceQ == "q":
						break
					else:
						interfaceA = "interface " + interfaceQ + "\n"
						sshshell.send(interfaceA)

						ipQ = input("Enter IP address with a proper netmask: ")
						ipA = 'ip address ' + ipQ + "\n"
						sshshell.send(ipA)
						sshshell.send("no sh\n")
						sshshell.send("exit\n")
						time.sleep(1)
						output = sshshell.recv(65535)
						printout = output.decode(encoding='UTF-8')
						print(printout)
						
						print_file = output.decode(encoding='UTF-8')
						file_save = open('output.txt', 'a+')
						file_save.write('\n' + timeStamp + print_file + '\n')
		
		hname = input("Set hostname? Y/N ")
		if hname == "y":
			hostn = input("What hostname for the device do you wish to set? ")
			hnameformat = "hostname " + hostn + "\n"
			sshshell.send(hnameformat)
			time.sleep(.3)

			output = sshshell.recv(65535)
			printout = output.decode(encoding='UTF-8')
			print(printout)
					
			print_file = output.decode(encoding='UTF-8')
			file_save = open('output.txt', 'a+')
			file_save.write('\n' + timeStamp + print_file + '\n')
		else:
			return

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
						time.sleep(.2)
						print(intout)
						sshshell.send(str(intout))
						sshshell.send('\n')
						sshshell.send('switchport port-security\n')
						sshshell.send('switchport port-security mac-address sticky\n')
						sshshell.send('switchport port-security maximum 2\n')					    							
						sshshell.send('switchport mode access\n')
						sshshell.send('shut\n')
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
		print(Style.RESET_ALL)
		sshshell.send('no cdp run\n')
		sshshell.send('no ip bootp server\n')
		sshshell.send('no ip arp proxy\n')
		sshshell.send('no ip http server\n')
		sshshell.send('no ip icmp redirect\n')
		sshshell.send('do show ip int br\n')
		time.sleep(1) #Wait for buffer


def ospf_setup():
		
		sshshell.send("\n")
		time.sleep(1)
		open(".parsefile", 'w').close() #clear parsefile

		output = sshshell.recv(2000000)
		printout = output.decode(encoding='UTF-8')
		print(printout)
		print_file = output.decode(encoding='UTF-8')
		file_save = open('output.txt', 'a+')
		file_save.write('\n' + timeStamp + print_file + '\n')

		ospfAS = input("OSPF AS number: ")
		ospfformat = ("router ospf " + ospfAS + '\n')
		sshshell.send(ospfformat)
		time.sleep(.3)
		output = sshshell.recv(65535)
		printout = output.decode(encoding='UTF-8')
		print(printout)
		
		
		while True:
			print()
			print(Fore.YELLOW +"#######################################################") 
			print(Fore.GREEN +"Pick a thing: Q or 'quit' to exit") 
			print(Fore.CYAN +"1: Interface Table         2: Routing Table")
			print(Fore.CYAN +"3: OSPF show commands      4: Set OSPF neighbor")
			print(Fore.CYAN +"5: Set Default origination 6: Set Router ID")
			print(Fore.CYAN +"7: Set stub area           8: Network Statements")
			print(Fore.YELLOW +"#######################################################")	
			print(Style.RESET_ALL)

			ospfNav = input("OSPF# ")
			if ospfNav == 'quit' or ospfNav == 'q':
				break		
			if ospfNav == "1":
				sshshell.send("do show ip int br\n")
				time.sleep(.3)
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)
			if ospfNav == "2":
				sshshell.send("do show ip route | begin Gateway\n")

				time.sleep(.3)
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)
			if ospfNav == "3":
				sshshell.send("do show ospf neigh\n")
				sshshell.send("do show ospf database\n")
				time.sleep(.5)
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)
			if ospfNav == "4":
				sshshell.send('do show ip route | begin Gateway\n')
				
				time.sleep(.3)				
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)
				
				ospfneigh = input("Enter IP of OSPF neighbor: ")
				ospfPrio = input("Enter priority of neighbor [0-255](Default: 1): ")
				ospfSEND1 = 'neighbor ' + ospfneigh + ' priority ' + ospfPrio + "\n"
				sshshell.send(ospfSEND1)

				time.sleep(.3)				
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)
			if ospfNav == "5":
				ospfQ = input("Set to always advertise default route? (Y/N) " )
				if ospfQ == "y":
					sshshell.send('default-information originate always\n')
					time.sleep(.3)

					output = sshshell.recv(65535)
					printout = output.decode(encoding='UTF-8')
					print(printout)
				if ospfQ == "n":
					sshshell.send('default-information originate\n')
					time.sleep(.2)
					output = sshshell.recv(65535)
					printout = output.decode(encoding='UTF-8')
					print(printout)
			if ospfNav == "6":
				ospfID = input("Please choose your router ID in IPv4 format: ")
				ospfSEND2 = 'router-id ' + ospfID + "\n"
				sshshell.send(ospfSEND2)

				time.sleep(.3)				
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)
			if ospfNav == "7":
				ospfSTUB = input("Please enter OSPF area number to become Stub-area: ")
				ospfSEND3 = 'area ' + ospfSTUB + ' stub no-summary' + '\n'
				sshshell.send(ospfSEND3)
				time.sleep(.3)				
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)
			if ospfNav == "8":
				sshshell.send('do show ip route | begin Gateway\n')
				time.sleep(.3)
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)

				ospfNET = input("Enter network ip: ")
				ospfMASK = input("Enter wildcard mask: ")
				ospfAREA = input("Enter area number: ")
				ospfSEND = "network " + ospfNET + " " + ospfMASK + " area " + ospfAREA + "\n"
				sshshell.send(ospfSEND)
				time.sleep(.3)
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)

			
def AAA():
		
		print("###Setup for AAA with radius authentication###")
		print("\n")
		aaaQ = input("Add username /w encrypted password, Y/N? ")
		if aaaQ == 'y' or aaaQ == 'Y':
			aaaU = input("Please enter username: ")
			aaaP = input("Please enter password, it will be encrypted using Type 9 hasing algorithm: ")
			aaaUPformat = "username " + aaaU + " algorithm-type scrypt secret " + aaaP + "\n"
			sshshell.send(aaaUPformat)
			time.sleep(.5)
			output = sshshell.recv(65535)
			printout = output.decode(encoding='UTF-8')
			print(printout)
		else:
			return
        
            
		print("aaa new model")
		print("aaa authentication login default group radius none")
		print("###Do not forget to validate Radius configurations before proceeding###")
		print("\n")
		radiusU = input("Please enter the name of Radius server to enter Radius-config, used for this device only: ")
		radiusUformat = "radius server " + radiusU + "\n"
		sshshell.send(radiusUformat)
		output = sshshell.recv(65535)
		printout = output.decode(encoding='UTF-8')
		print(printout)

		radiusS = input("Please enter IP address of the Radius server: ")
		print("address ipv4 " + radiusS + " " + "auth-port 1812 acct-port 1813")
		radiusSformat = "address ipv4 " + radiusS + " " + "auth-port 1812 acct-port 1813\n"
		sshshell.send(radiusSformat)		        
		time.sleep(0.3)
		output = sshshell.recv(65535)
		printout = output.decode(encoding='UTF-8')
		print(printout)


		radiusK = input("Please enter the Key/password for the radius server: ")
		radiusKformat = "key " + radiusK
		sshshell.send(radiusKformat)
		print("key " + radiusK)
		time.sleep(0.3)
		output = sshshell.recv(65535)
		printout = output.decode(encoding='UTF-8')
		print(printout)

def IProute():
		
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
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)
				break

			if routeNav == "2":
				time.sleep(1)
				routeS2 = input("Enter exit interface for default static route: ")
				routeS2format = "ip route 0.0.0.0 0.0.0.0 " + routeS2 + "\n"
				sshshell.send(routeS2format)
				time.sleep(.5)
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)
				break
			
			else:
				break

def int_IPconf():
		while True:
			interfaceQ = input("Enter the interface you want to configure (q) to quit: ")
			if interfaceQ == "q":
				return
			else:
				interfaceA = "interface " + interfaceQ
				sshshell.send(interfaceA)
				sshshell.send("\n")
				ipQ = input("Enter wanted IP address with a proper netmask: ")
				ipA = 'ip address ' + ipQ + "\n"
				sshshell.send(ipA)
				sshshell.send("exit\n")
				time.sleep(.3)
				output = sshshell.recv(65535)
				printout = output.decode(encoding='UTF-8')
				print(printout)

def int_SHUT():
	sshshell.send("do show ip int br\n")
	print(Fore.MAGENTA+"Fetching table..")
	print(Style.RESET_ALL)
	for i in tqdm(range(10)):
		time.sleep(.1)
	output = sshshell.recv(65535)
	printout = output.decode(encoding='UTF-8')
	print(printout)
	intchoice = input("Single(1) or multiple interfaces(2)? ")
	if intchoice == "1":
		switchPrompt = input("Enter interface: ")
		switchINT = ('interface ') +  switchPrompt + "\n"
		print("The interface shutting down is: " + switchPrompt + '\n')
		sshshell.send(switchINT)
		sshshell.send('shutdown\n')
		time.sleep(1) #Wait to buffer
	if intchoice == "2":
		switchPrompt = input("Enter range: ")
		switchINT = ('interface range ') +  switchPrompt + "\n"
		print("The interfaces shutting down is: " + switchPrompt + '\n')
		sshshell.send(switchINT)
		sshshell.send('shutdown\n')
		time.sleep(1) #Wait to buffer

def trunk_conf():
	
	sshshell.send("do show ip int br\n")
	print(Fore.MAGENTA+"Fetching table..")
	print(Style.RESET_ALL)
	for i in tqdm(range(10)):
		time.sleep(.1)
	output = sshshell.recv(65535)
	printout = output.decode(encoding='UTF-8')
	print(printout)

	etherc = input("Make etherchannel? Y/N ") 
	if etherc == "y":
		erange = input("Enter interface range: ")
		erangeformat = "int range " + erange + "\n"
		sshshell.send(erangeformat)
		protchoice = input("LACP(1) or PAgP(2) ")
		if protchoice == "1": #LACP config
			sshshell.send("shut\n")
			time.sleep(1)
			groupsel = input("Channel group number: ")
			groupselformat = "channel-group " + groupsel + " mode active\n"
			sshshell.send(groupselformat)
			sshshell.send("no shut\n")
			time.sleep(.5)
			ethertrunk = input("Trunk interfaces? Y/N ")
			if ethertrunk == "y":
				sshshell.send("int po" + groupsel + "\n")
				sshshell.send("switchport mode trunk\n")
				nvlan = input("Native VLAN(number)for trunk: ")
				nvlanformat = "switchport trunk native vlan " + nvlan + "\n"
				sshshell.send(nvlanformat)
				allowv = input('Allowed vlans(separate only with ",": ')
				sshshell.send("switchport trunk allowed vlan " + allowv + "\n")
				time.sleep(.5)
			if ethertrunk == "n":
				
				return
			else:
				return

			output = sshshell.recv(65535)
			printout = output.decode(encoding='UTF-8')
			print(printout)
			print_file = output.decode(encoding='UTF-8')
			file_save = open('output.txt', 'a+')
			file_save.write('\n' + timeStamp + print_file + '\n')

		if protchoice == "2": # PAgP config
			sshshell.send("shut\n")
			sshshell.send("shut\n")
			time.sleep(1)
			groupsel = input("Channel group number: ")
			groupselformat = "channel-group " + groupsel + " mode desirable\n"
			sshshell.send(groupselformat)
			sshshell.send("no shut\n")
			time.sleep(.5)
			sshshell.send("no shut\n")
			ethertrunk = input("Trunk interfaces? Y/N ")
			if ethertrunk == "y":
				sshshell.send("int po" + groupsel + "\n")
				sshshell.send("switchport mode trunk\n")
				nvlan = input("Native VLAN(number)for trunk: ")
				nvlanformat = "switchport trunk native vlan " + nvlan + "\n"
				sshshell.send(nvlanformat)
				allowv = input('Allowed vlans(separate only with ",": ')
				sshshell.send("switchport trunk allowed vlan " + allowv + "\n")
				time.sleep(.5)
			if ethertrunk == "n":
				return
			else:
				return	

			output = sshshell.recv(65535)
			printout = output.decode(encoding='UTF-8')
			print(printout)
			print_file = output.decode(encoding='UTF-8')
			file_save = open('output.txt', 'a+')
			file_save.write('\n' + timeStamp + print_file + '\n')
		
		else:
			return

	else:
		tchoice = input("Single(1) or multiple(2) interfaces? ")
		if tchoice == "1":
			trunki = input("Input single interface for trunk: ")
			trunkiformat = "int " + trunki + "\n"
			sshshell.send(trunkiformat)
			sshshell.send("switchport mode trunk\n")
			nvlan = input("Native VLAN(number)for trunk: ")
			nvlanformat = "switchport trunk native vlan " + nvlan + "\n"
			sshshell.send(nvlanformat)
			allowv = input('Allowed vlans(separate only with ",": ')
			sshshell.send("switchport trunk allowed vlan " + allowv + "\n")
			sshshell.send("no shut\n")
			time.sleep(.5)

			output = sshshell.recv(65535)
			printout = output.decode(encoding='UTF-8')
			print(printout)
			print_file = output.decode(encoding='UTF-8')
			file_save = open('output.txt', 'a+')
			file_save.write('\n' + timeStamp + print_file + '\n')
			return
		
		if tchoice == "2":
			mtrunki = input("Enter interface range: ")
			mtrunkiformat = "int range " + mtrunki + "\n"
			sshshell.send(mtrunkiformat)
			sshshell.send("shut\n")
			sshshell.send("switchport mode trunk\n")
			mnvlan = input("Native VLAN(number) for trunk: ")
			mnvlanformat = "switchport trunk native vlan " + mnvlan + "\n"
			allowv = input('Allowed vlans(separate only with ",": ')
			sshshell.send("switchport trunk allowed vlan " + allowv + "\n")
			sshshell.send(mnvlanformat)
			sshshell.send("no sh\n")
			time.sleep(.5)

			output = sshshell.recv(65535)
			printout = output.decode(encoding='UTF-8')
			print(printout)
			print_file = output.decode(encoding='UTF-8')
			file_save = open('output.txt', 'a+')
			file_save.write('\n' + timeStamp + print_file + '\n')
			return
		else:
			return



#Creds
servIP = input("IP: ")
usrname = input("Username: ")
passwd = getpass.getpass("Password: ")

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
splashp = splash.decode(encoding='UTF-8')
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
print(splashp)
splash = sshshell.recv(65535)
splashp = splash.decode(encoding='UTF-8')
#print(splashp)

#Dictionary binds configs to numbers
config_list = {
	'1': basic_config,
	'2': service_security,
	'3': ospf_setup,
	'4': AAA,
	'5': IProute,
	'6': int_IPconf,
	'7': trunk_conf,
	'8': int_SHUT,
	'i': int_table,
	'r': r_table,
	'c': run_conf,
	'p': ip_prot,
	't': sh_trunk,
	'e': sh_eth,
	'v': sh_vlan,
	'o': ospf_neigh,
	'a': arp_table,
	'u': sh_user,
	'd': sh_dhcp,
	'n': sh_ntp,
	'h': hostnames,

}


#Command loop
while True:
	
	#Interface
	print()
	print(Fore.YELLOW +"####################################################################") 
	print(Fore.GREEN +"Pick a thing: Q or 'quit' to exit") 
	print(Fore.CYAN +"1: Basic Settings     2: Port/Service Security 3: OSPF")
	print(Fore.CYAN +"4: AAA                5: Routing               6: IP config")
	print(Fore.CYAN +"7: Trunks & channels  8: Disable interfaces    H: Hostname")
	print(Fore.CYAN +"I: Interface table    R: Routing table         C: Running-config" )
	print(Fore.CYAN +"P: Routing Protocols  T: Show trunks           E: Show etherchannels")
	print(Fore.CYAN +"V: Show vlans         O: OSPF neighbors        A: Arp table")
	print(Fore.CYAN +"U: Show users         D: Show DHCP             N: Show NTP")
	#print(Fore.CYAN +
	print(Fore.YELLOW +"####################################################################")	
	print(Style.RESET_ALL)

	#User command
	cmand = input("#: ")
	if cmand == 'quit' or cmand == 'q':
		sshshell.send('exit\n')
		ssh.close()
		break
	config_list[cmand]()

		
	#Decode and print outputs
	sshshell.send("\n")
	time.sleep(.1)
	output = sshshell.recv(65535)
	printout = output.decode(encoding='UTF-8')
	print(printout)
	time.sleep(.2)
	#Save output to file
	print_file = output.decode(encoding='UTF-8')
	file_save = open('output.txt', 'a+')
	file_save.write('\n' + timeStamp + print_file + '\n')
