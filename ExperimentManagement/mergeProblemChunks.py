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
            print 'Usage: python mergeProblemChunks.py'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python mergeProblemChunks.py : This function takes no arguments, it needs to be called in the project dir'
            sys.exit()

    #remove the previous danger bits file
    os.system('rm ./results/dangerBits.la')

    print 'Collecting Problems'
    input_problem_bits = os.listdir('./problemChunks') 
    for problem_bit in input_problem_bits:
	problem_bit_merge_cmd = 'cat ./problemChunks/'+problem_bit+' >> ./results/dangerBits.la'
	os.system(problem_bit_merge_cmd)
	print 'Problem Bit: ' +problem_bit+ ' has been merged into the dangerBits file.'
    print 'Merging completed.'

if __name__ == "__main__":
    main(sys.argv[1:])

