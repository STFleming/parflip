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
            print 'Usage: python evaluateProblemChunks.py --number <Number of SoCs in the drawer> --bit <bitstream file>'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python evaluateProblemChunks.py --number <Number of SoCs in the drawer> --bit <bitstream file>'
            sys.exit()
        if opt in ("-n", "--number"):
            totalsocs = arg
        if opt in ("-b", "--bit"):
            bitstream = arg
    assert(totalsocs != '')
    assert(bitstream != '')

    basecase = False
    rerun_cmd = 'python ~/socDrawer/ExperimentManagement/kmeans_evaluateChunks.py --number '+totalsocs+' --bit '+bitstream

    while(basecase == False):
	basecase = True
        input_chunks = os.listdir('./problemChunks')
        for chunk in input_chunks:
            if (sum(1 for line in open('./problemChunks/'+chunk)) > 1):
                basecase = False
                chunk_split_cmd = 'split --additional-suffix=_'+chunk+'p -nl/2 ./problemChunks/'+chunk 
                os.system(chunk_split_cmd)
                chunk_cleanup_cmd = 'rm ./problemChunks/'+chunk
                os.system(chunk_cleanup_cmd)
                print 'Chunk '+chunk+' has been split and cleaned up.'
        if (basecase == False):
            os.system('mv *p ./Chunks/')
            print 'Problem Chunk Splitting Complteted, evaluating the new chunks.'
            os.system(rerun_cmd)

    print 'Final run on chunks with single elements.'
    os.system('mv ./problemChunks/* ./Chunks/')
    os.system(rerun_cmd)
    print 'All persistent problem chunks have been identified.'
		    

if __name__ == "__main__":
    main(sys.argv[1:])

