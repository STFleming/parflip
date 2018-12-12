import sys, getopt
import re
import math

def main(argv):
    outfile = ''
    stateNum = 0 

    startframe = 0
    endframe = 7950

    try:
            opts, args = getopt.getopt(argv, "ho:s:e", ["output=", "startframe=", "endframe="])
    except getopt.GetoptError:
            print 'Usage: python generateExhaustiveLinearAddr.py --output <output linear addresses> --startframe <start frame> --endframe <end frame>'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python generateExhaustiveLinearAddr.py --output <output linear addresses> --startframe <start frame> --endframe <end frame>'
            sys.exit()
        if opt in ("-o", "--output"):
            outfile = arg
        if opt in ("-s", "--startframe"):
            startframe = int(arg)
        if opt in ("-e", "--endframe"):
            endframe = int(arg)
    assert(outfile != '')

    outf = open(outfile, 'w')

    frameSize = 101 #Size of the frame in 32 bit words
    offset = 109 #Size of the zero padding
    totalFrames = 7950

    address = 0
    for frame in range(startframe,endframe):
        for word in range(49,50):
            for bit in range(0,32):
                address = frame << 12
                address = address | (word << 5)
                address = address | bit 
		#print str(address) + '		f:'+str(frame)+'    w:'+str(word)+'    b:'+str(bit) 
                outf.write(str(address) + '\n')

    outf.close()

if __name__ == "__main__":
            main(sys.argv[1:])
