import sys, getopt
import os
import time

#Runs the experiment on each chunk. If the board crashes the chunk is allocated as a problem chunk
#for a later extensive slower evaluation where the problem bits are isolated and recorded.
#The results for all successful chunks are stored in the ./results directory.

def main(argv):
    totalsocs = ''
    bitstream = ''
    try:
            opts, args = getopt.getopt(argv, "hn:b", ["number=", "bit="])
    except getopt.GetoptError:
            print 'Usage: python evaluateChunks.py --number <Number of SoCs in the drawer> --bit <bitstream file>'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python evaluateChunks.py --number <Number of SoCs in the drawer> --bit <bitstream file>'
            sys.exit()
        if opt in ("-n", "--number"):
            totalsocs = arg
        if opt in ("-b", "--bit"):
            bitstream = arg
    assert(totalsocs != '')
    assert(bitstream != '')

    success=True
    N = int(totalsocs)
    for i in range(0,N):
	ping_cmd = 'timeout 0.5 ping -c 1 -i 0.3 soc' + str(i) + ' > /dev/null 2>&1' 
	if os.system(ping_cmd) != 0:
		success = False
		print 'soc' + str(i) + '  is offline'
	else:
		print 'soc' + str(i) + '  is online'

    if success==False:
	print 'Error: not all the boards are in a stable condition'
	return

    print 'Clearing the bitstreams from all the SoCs' +'\t\t'+str(time.ctime()) 
    for i in range(0,N):
         print '		Clearing the test bitstream in soc' + str(i) +'\t\t'+str(time.ctime())
         clear_bit_cmd = 'ssh root@soc' + str(i) + ' \'rm -f ./*.bin\''
         os.system(clear_bit_cmd) 
    print 'Completed clearing the previous testbits.' +'\t\t'+str(time.ctime())

    print 'Tranfer the test bitstream to all socs' +'\t\t'+str(time.ctime())
    for i in range(0,N):
         print '		Transfering test bitstream to soc' + str(i) +'\t\t'+str(time.ctime())
         transfer_testbit_cmd = 'scp ' + bitstream  +' root@soc'+str(i)+':~/'
         os.system(transfer_testbit_cmd)
    print 'Transfer of testbits is completed.' +'\t\t'+str(time.ctime())

    #grab the first N(number of socs) chunks from the chunks directory
    input_chunks = os.listdir('./Chunks')
    print 'Allocating Chunks to SoCs' +'\t\t'+str(time.ctime()) 
    chunk_slice = input_chunks[:N]	
    
    while(len(chunk_slice) > 0):
        input_chunks = os.listdir('./Chunks')
        print 'Allocating Chunks to SoCs' +'\t\t'+str(time.ctime()) 
        chunk_slice = input_chunks[:N]	

        if len(chunk_slice) == 0:
            print 'All Chunks have been processed, or moved to the problemChunks directory.' +'\t\t'+str(time.ctime())
            return
       
        chunkAllocation = [] 
        current_soc = 0
        for c in chunk_slice:	
            print '		Allocation chunk ' + c + ' to soc' + str(current_soc) +'\t\t'+str(time.ctime()) 
            chunk_element = (c, current_soc)
            chunkAllocation.append(chunk_element)
            print '		Clearing previous chunk from soc' + str(current_soc) +'\t\t'+str(time.ctime())
            clear_chunk_cmd = 'ssh root@soc'+str(current_soc)+' \'rm -f x*\''
            os.system(clear_chunk_cmd)
            print '		Transfering new chunk ' + c + 'to soc' + str(current_soc) +'\t\t'+str(time.ctime())
            chunk_transfer_cmd = 'scp ./Chunks/'+c+' root@soc'+str(current_soc)+':~/'	
            os.system(chunk_transfer_cmd)
            current_soc = current_soc + 1

        chunk_completed_sig_dir = '/home/'+os.environ['USER']+'/.completed_chunks'
        print 'Clear the chunk completed directory ' + chunk_completed_sig_dir +'\t\t'+str(time.ctime())
        chunk_completed_clearing_cmd = 'rm -r -f ' + chunk_completed_sig_dir
        os.system(chunk_completed_clearing_cmd)
        make_chunk_completed_sig_cmd = 'mkdir ' + chunk_completed_sig_dir
        os.system(make_chunk_completed_sig_cmd)
        print 'Clearing of the local chunk completed directory completed.' +'\t\t'+str(time.ctime())

        print 'Generating individual soc experiment scripts' +'\t\t'+str(time.ctime())
        current_soc = 0
        for c in chunk_slice:
            generate_exp_script_cmd_line1 = 'echo \"python ./StitchUp/zynq/seuInjection/scripts/injectErrors.py --la '+c+' --bit '+ bitstream +' >> '+c+'.csv \" > soc'+str(current_soc)+'_injErr.sh'
            generate_exp_script_cmd_line2 = 'echo \"scp '+c+'.csv '+os.environ['USER']+'@ee-socDrawer.ee.ic.ac.uk:'+chunk_completed_sig_dir+'/'+c+'\" >> soc'+str(current_soc)+'_injErr.sh'
            generate_exp_script_cmd_line3 = 'echo \"rm '+c+' '+c+'.csv \" >> soc'+str(current_soc)+'_injErr.sh'
            os.system(generate_exp_script_cmd_line1)
            os.system(generate_exp_script_cmd_line2)
            os.system(generate_exp_script_cmd_line3)
            current_soc = current_soc + 1

        print 'Transfering all experiment scripts to the corresponding soc' +'\t\t'+str(time.ctime())
        current_soc = 0
        for c in chunk_slice:
            expr_script_transfer_cmd = 'scp soc'+str(current_soc)+'_injErr.sh root@soc'+str(current_soc)+':~/'
            os.system(expr_script_transfer_cmd)
            print '		Changing expr script permissions on soc'+str(current_soc) +'\t\t'+str(time.ctime())
            executable_permission_cmd = 'ssh root@soc'+str(current_soc)+' \'chmod u+x soc'+str(current_soc)+'_injErr.sh\''
            os.system(executable_permission_cmd)
            cleanup_local_scripts_cmd = 'rm soc'+str(current_soc)+'_injErr.sh'
            os.system(cleanup_local_scripts_cmd)
            current_soc = current_soc + 1	

        print 'Launching all the allocated jobs.' +'\t\t'+str(time.ctime())
        current_soc = 0
        for c in chunk_slice:
            print '		Chunk ' +c+' launched on soc'+str(current_soc) +'\t\t'+str(time.ctime())
            launch_injection_cmd = 'ssh root@soc'+str(current_soc)+' \'screen -d -m ./soc'+str(current_soc)+'_injErr.sh\''
            os.system(launch_injection_cmd)
            current_soc = current_soc + 1

        print 'Chunks are being evaluated.' +'\t\t'+str(time.ctime())
        completed_socs = []
        dead_socs = []
        while len(chunkAllocation) > 0:
        	completed_chunks = os.listdir(chunk_completed_sig_dir)	  
        	for i in chunkAllocation:
        	    if i[0] in completed_chunks:
        	        print '  Chunk ' + i[0] + ' on soc' + str(i[1]) + ' has completed.' +'\t\t'+str(time.ctime())	
        	        move_completed_chunk_cmd = 'mv '+chunk_completed_sig_dir+'/'+i[0] + ' ./completedChunks/'
        	        remove_completed_chunk_cmd = 'rm ./Chunks/'+i[0]
        	        os.system(move_completed_chunk_cmd)
			os.system(remove_completed_chunk_cmd)
        	        completed_socs.append(i[0]) 
        	    ping_cmd = 'timeout 0.5 ping -c 1 -i 0.3 soc' + str(i[1]) + ' > /dev/null 2>&1' 
        	    if os.system(ping_cmd) != 0:
        	        print '  soc' + str(i[1]) + '  is offline: Chunk ' +i[0]+' is a problem chunk.' +'\t\t'+str(time.ctime())
        	        move_problem_chunk_cmd = 'mv ./Chunks/'+i[0]+' ./problemChunks' 		
        	        os.system(move_problem_chunk_cmd)
        	        dead_socs.append(i[0]) 

        	chunkAllocation = [i for i in chunkAllocation if not(i[0] in completed_socs or i[0] in dead_socs)]

	print 'There should be ' + str(len(dead_socs)) + ' socs that need power cycling.' +'\t\t'+str(time.ctime())
	if len(dead_socs) > 0:
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
                        	print 'soc' + str(i) + '  is offline' +'\t\t'+str(time.ctime())
                	else:
                        	print 'soc' + str(i) + '  is online' +'\t\t'+str(time.ctime())

    	print "All SoCs are stable and ready." +'\t\t'+str(time.ctime())
		    

if __name__ == "__main__":
    main(sys.argv[1:])

