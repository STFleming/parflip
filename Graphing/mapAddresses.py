import sys, getopt
import csv
import matplotlib.pylab as pl
import numpy as np

def main(argv):
    addrfilename = ''
    try:
            opts, args = getopt.getopt(argv, "hi", ["input="])
    except getopt.GetoptError:
            print 'Usage: python mapAddresses.py --input <addr>.la'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python mapAddresses.py --input <addr>.la'
            sys.exit()
        if opt in ("-i", "--input"):
            addrfilename = arg
    assert(addrfilename != '')

    lastFrame = 7950
    firstFrame = 0;
    FRAME_MASK = 0b11111111111111111000000000000
    WORD_MASK =  0b00000000000000000111111100000
    BIT_MASK =   0b00000000000000000000000011111

    word_occupied = np.zeros((7950,101), dtype='int32')

    with open(addrfilename) as f:
        lines = f.readlines();
    int_lines = [int(i) for i in lines]

    for linearaddr in int_lines:
        Frame = (linearaddr & FRAME_MASK) >> 12
        word = (linearaddr & WORD_MASK) >> 5
        bit = (linearaddr & BIT_MASK)
        word_occupied[Frame, word] = 1;

    pl.matshow(word_occupied, fignum=100, cmap=pl.cm.Blues, aspect='auto')
    pl.show()



if __name__ == "__main__":
    main(sys.argv[1:])

