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
        
        sshshell.send('switchINT\n')
        sshshell.send('shutdown\n')
        sshshell.send('exit\n')
        time.sleep(1) #Wait to buffer


