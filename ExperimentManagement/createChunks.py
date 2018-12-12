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
            opts, args = getopt.getopt(argv, "ha:c", ["la=", "chunks="])
    except getopt.GetoptError:
            print 'Usage: python createChunks.py --la <Linear addresses for the target circuit> --chunks <Number of Chunks>'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python createChunks.py --la <Linear addresses for the target circuit> --chunks <Number of Chunks>'
            sys.exit()
        if opt in ("-a", "--la"):
            linAddrStr = arg
        if opt in ("-c", "--chunks"):
            chunksStr = arg
    assert(linAddrStr != '')
    assert(chunksStr != '')

    success=True
    
    #Cleanup any leftover chunk directories
    os.system('rm -r -f ./Chunks')
    os.system('rm -r -f ./problemChunks')
    os.system('rm -r -f ./completedChunks')
    os.system('rm -r -f ./results')

    #Create the directories
    os.system('mkdir ./Chunks')
    os.system('mkdir ./problemChunks')
    os.system('mkdir ./completedChunks')
    os.system('mkdir ./results')

    print 'Chunking up the linear addresses'
    chunk_cmd = 'split -nl/' + chunksStr + ' ' + linAddrStr
    os.system(chunk_cmd)
    os.system('mv x* ./Chunks')
    print 'Completed chunking of linear addresses.'

if __name__ == "__main__":
    main(sys.argv[1:])

