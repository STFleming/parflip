import sys, getopt
import os
import time

def main(argv):
    totalsocs = ''
    try:
            opts, args = getopt.getopt(argv, "hn", ["number="])
    except getopt.GetoptError:
            print 'Usage: python restartDrawer.py --number <Number of SoCs in the drawer>'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python restartDrawer.py --number <Number of SoCs in the drawer>'
            sys.exit()
        if opt in ("-n", "--number"):
            totalsocs = arg
    assert(totalsocs != '')

    N = int(totalsocs)
    success = False

    while(success == False):
	    success = True
	    os.system('echo "1" > /dev/ttyUSB0')
	    os.system('echo "0" > /dev/ttyUSB0')
	
	    time.sleep(30)
	
	    for i in range(0,N):
		ping_cmd = 'timeout 0.5 ping -c 1 -i 0.3 soc' + str(i) + ' > /dev/null 2>&1' 
		if os.system(ping_cmd) != 0:
			success = False
			print 'soc' + str(i) + '  is offline'
		else:
			print 'soc' + str(i) + '  is online'

    print "All SoCs are stable and ready."
if __name__ == "__main__":
    main(sys.argv[1:])

