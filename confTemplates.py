#Template file

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
		time.sleep(1) #Wait for buffer

def switch_interfaceConf():
        switchPrompt = input("Wich interfaces do you want to shut down? F0/1-24 & G0/0-1 is available")
        switchINT = ('interface range') +  switchPrompt
        print("The interfaces shutting down is: " + switchPrompt)
        
        sshshell.send(switchINT)
        sshshell.send('shutdown\n')
        sshshell.send('exit\n')
        time.sleep(1) #Wait to buffer

def switch_interfaceConf():
            switchSec = input("Wich interface do you want to secure? ")
            switchCom = ('interface ') + switchSec
            sshshell.send(switchCom)
            sshshell.send('\n')
            sshshell.send('switchport mode access\n')
            sshshell.send('switchport port-security\n')
            sshshell.send('exit\n')
            switchMAC = input("Set MAC security to sticky Y/N? ")
            if switchMAC == "y":
                sshshell.send('switchport port-security\n')
                sshshell.send('switchport port-security mac-address sticky\n')
                sshshell.send('switchport port-security maximum 2\n')
            if switchMAC == "n":
                return

def switch_interfaceSHUT():
                switchPrompt = input("Wich interfaces do you want to shut down? F0/1-24 & G0/1-2 is available: ")
                switchINT = ('interface range ') +  switchPrompt
                print("The interfaces shutting down is: " + switchPrompt)        
                sshshell.send('\n')
                sshshell.send(switchINT)
                sshshell.send('\n')
                sshshell.send('shutdown\n')
                time.sleep(1) #Wait to buffer


def interface_IPconf():
			interfaceQ = input("Enter the interface you want to configure: ")
			interfaceA = ('interface') + " " + interfaceQ
			print(interfaceA)
			#sshshell.send(interfaceA)
			#time.sleep(.5)

			ipQ = input("Enter wanted IP address with a proper netmask: ")
			ipA = 'ip address ' + ipQ
			print(ipA)
			#sshshell.send(ipA)
			#time.sleep(.5)


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
            
            #sshshell.send('\n')
            #sshshell.send('username ' + aaaU + ' algorithm-type scrypt secret ' + aaaP)
            time-sleep(.5)
            print(printout)
            #print("username " + aaaU + " algorithm-type scrypt secret " + aaaP)
        else:
            return
        
            
        print("aaa new model")
        print("aaa authentication login default group radius none")
        #sshshell.send('aaa new model\n')
        #sshshell.send('aaa authentication login default group radius none\n')
        print("###Do not forget to validate Radius configurations before proceeding###")
        
        radiusU = input("Please enter the name of Radius server to enter Radius-config, used for this device only: ")
        #print("radius server " + radiusU)
        radiusUformat = "radius server " + radiusU + "\n"
        sshshell.send(radiusUformat)

        #sshshell.send('radius server ' + radiusU + '\n')
        #time-sleep(0.3)
        print(printout)

        radiusS = input("Please enter IP address of the Radius server: ")
        print("address ipv4 " + radiusS + " " + "auth-port 1812 acct-port 1813")
        radiusSformat = "address ipv4 " + radiusS + " " + "auth-port 1812 acct-port 1813\n"
        sshshell.send(radiusSformat)
        
        #sshshell.send('address ipv4 ' + radiusS + 'auth-port 1812 acct-port 1813' + '\n')
        time.sleep(0.3)
        print(printout)

        radiusK = input("Please enter the Key/password for the radius server: ")
        radiusKformat = "key " + radiusK
        sshshell.send(radiusKformat)
        #sshshell.send('key ' + radiusK + '\n')
        print("key " + radiusK)
        time.sleep(0.3)
        print(printout)




def IProute():
		print()
		print(Fore.YELLOW +"#######################################################") 
		print(Fore.GREEN +"Pick a option for setting route: Q or 'quit' to exit") 
		print(Fore.CYAN +"1: Static 2: Default static")
		print(Fore.YELLOW +"#######################################################")	
		print(Style.RESET_ALL)
		
		#output = sshshell.recv(65535)
		#printout = output.decode(encoding='UTF-8')
		
		
		while True:
			#print(printout +'\n')
			routeNav = input("1 or 2?: ")
			if routeNav == 'quit' or routeNav == 'q':
				quit()		
			if routeNav == "1":
				routeS = input("Enter wanted destination address for static route with proper netmask: ")
				routeI = input("Enter exit inteface: ")
				print("ip route " + routeS + " " + routeI)
				routeSIformat = "ip route " + routeS + " " + routeI + "\n"
				sshshell.send(routeSIformat)
				#sshshell.send('ip route ' + routeS + " " + routeI '\n')
				#time.sleep(1)

				#sshshell.send("\n")
				time.sleep(.5)
				print(printout)
				break
			if routeNav == "2":
				routeS2 = input("Enter exit interface for default static route: ")
				print("ip route 0.0.0.0 0.0.0.0" + " " + routeS2)
				routeS2format = "ip route 0.0.0.0 0.0.0.0 " + routeS2 + "\n"
				sshshell.send(routeS2format)
				#sshshell.send('ip route 0.0.0.0 0.0.0.0' + " " + routeS2 + '\n')
				time.sleep(.5)
				print(printout)
				break
			else:
				break

			#output = sshshell.recv(65535)
			#printout = output.decode(encoding='UTF-8')