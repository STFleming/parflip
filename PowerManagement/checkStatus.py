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
    for i in range(0,N):
	ping_cmd = 'timeout 0.5 ping -c 1 -i 0.3 soc' + str(i) + ' > /dev/null 2>&1' 
	if os.system(ping_cmd) != 0:
		success = False
		print 'soc' + str(i) + '  is'+ "\033[0;31m" + ' offline'+"\033[0m"
	else:
		print 'soc' + str(i) + '  is'+ "\033[0;32m" +'  online'+"\033[0m"

if __name__ == "__main__":
    main(sys.argv[1:])

