import sys, getopt
import os
import time

#This script creates the directories for storing the chunks of essential bits
#the problem chunks, and the completed chunks. It then chunks up the essential
#bits into roughly equal sized portions specified with the chunks parameter.


def main(argv):
    linAddrStr = ''
    chunksStr = ''
    try:
            opts, args = getopt.getopt(argv, "h")
    except getopt.GetoptError:
            print 'Usage: python mergeChunks.py'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python createChunks.py : This function takes no arguments, it needs to be called in the project dir'
            sys.exit()
    
    #CleanUp Previous results
    os.system('rm ./results/res.csv')

    print 'Collecting Chunks'
    input_chunks = os.listdir('./problemChunks') 
    for chunk in input_chunks:
	chunk_split_cmd = 'split --additional-suffix=_'+chunk+'p -nl/2 ./problemChunks/'+chunk
	os.system(chunk_split_cmd)
	chunk_cleanup_cmd = 'rm ./problemChunks/'+chunk
	os.system(chunk_cleanup_cmd)
	print 'Chunk: ' +chunk+ ' has been split.'
    os.system('mv *p ./Chunks/')
    print 'Chunk splitting is completed.'

if __name__ == "__main__":
    main(sys.argv[1:])

