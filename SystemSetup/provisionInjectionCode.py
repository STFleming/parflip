import sys, getopt
import os
import time

#gets the latest github version of the injection code and transfers it to each of the 
#socs in the cluster#socs in the cluster

def main(argv):
    totalsocs = ''
    try:
            opts, args = getopt.getopt(argv, "hn", ["number="])
    except getopt.GetoptError:
            print 'Usage: python provisionInjectionCode.py --number <Number of SoCs in the drawer>'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python provisionInjectionCode.py --number <Number of SoCs in the drawer>'
            sys.exit()
        if opt in ("-n", "--number"):
            totalsocs = arg
    assert(totalsocs != '')

    success=True

    os.system('rm -r -f ./StitchUp')

    N = int(totalsocs)
    for i in range(0,N):
	ping_cmd = 'timeout 0.5 ping -c 1 -i 0.3 soc' + str(i) + ' > /dev/null 2>&1' 
	if os.system(ping_cmd) != 0:
		success = False
		print 'soc' + str(i) + '  is offline'
	else:
		print 'soc' + str(i) + '  is online'

    if success == False:
	print 'All the SoCs must be online to proceed, otherwise they might have inconsistent state.'
	return

    print 'Getting latest version from github.'
    os.system('git clone git@github.com:STFleming/StitchUp.git')

    print 'Removing previous versions on each SoC.' 
    for s in range(0,N):
	print '		Cleaning previous version on soc' + str(s)
	cleanup_cmd = 'ssh root@soc' + str(s) + ' \'rm -f -r ./StitchUp\''
	os.system(cleanup_cmd)
   
    print 'Transferring current copy of the base code to each of the SoCs'
    for s in range(0,N):
	print '		Setting up soc' + str(s)
	transfer_cmd = 'scp -r ./StitchUp root@soc' + str(s) + ':~/'
	os.system(transfer_cmd)
    os.system('rm -r -f ./StitchUp')
    print 'Transfer completed, all SoCs should have the latest version of the injection code.' 

#    print 'Transferring working sources.list for apt-get'
#    for s in range(0,N):
#	print '		Fixing apt-get for soc'+ str(s)
#	copy_sources_cmd = 'scp ./sources.list root@soc'+str(s)+':/etc/apt'
#	os.system(copy_sources_cmd)
#	apt_install_cmds = 'ssh root@soc'+str(s)+' \'apt-get -y upgrade; apt-get -y update --fix-missing; apt-get -y install make; apt-get -y install gcc; apt-get -y install screen\''
#	os.system(apt_install_cmds)
	

    print 'Building Local error injection code on each SoC'
    for s in range(0,N):
	print '		Building error injection code on soc'+str(s)
	make_bin_dir_cmd = 'ssh root@soc'+str(s)+' \'mkdir ./StitchUp/zynq/seuInjection/sw_driver/bin \''
	os.system(make_bin_dir_cmd)
	build_cmd = 'ssh root@soc'+str(s)+' \'cd ./StitchUp/zynq/seuInjection/sw_driver; make;\''
	os.system(build_cmd)
	print '		Error injection code for soc'+str(s)+' has been completed'

if __name__ == "__main__":
    main(sys.argv[1:])

