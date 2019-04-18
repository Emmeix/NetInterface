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


