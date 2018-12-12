import sys, getopt
import csv
import matplotlib.pylab as pl
import numpy as np

def main(argv):
    dangerbits_filename = ''
    try:
            opts, args = getopt.getopt(argv, "hi:f", ["input=", "frame="])
    except getopt.GetoptError:
            print 'Usage: python mapDangerBits.py --input <dangerbits>.la --frame <frame you want to plot>'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python mapDangerBits.py --input <dangerbits>.la --frame <frame you want to plot>'
            sys.exit()
        if opt in ("-i", "--input"):
            dangerbits_filename = arg
        if opt in ("-f", "--frame"):
            frame = int(arg)
    assert(dangerbits_filename != '')

    dangerbits = np.zeros((32,101), dtype='int32')
    FRAME_MASK = 0b11111111111111111000000000000
    WORD_MASK =  0b00000000000000000111111100000
    BIT_MASK =   0b00000000000000000000000011111

    with open(dangerbits_filename) as f:
        lines = f.readlines();    
    int_lines = [int(i) for i in lines]

    for linearaddr in int_lines:
        curr_Frame = (linearaddr & FRAME_MASK) >> 12 
        if curr_Frame==frame:
            word = (linearaddr & WORD_MASK) >> 5	
	    print word
            bit = (linearaddr & BIT_MASK)
	    print bit
	    dangerbits[bit,word] = 1;
            print "\n"
	
    pl.matshow(dangerbits, fignum=100, cmap=pl.cm.Reds, aspect='auto')
    pl.show()

    #pl.matshow(Derrors, fignum=100, cmap=pl.cm.Blues)
    #pl.matshow(Cerrors, fignum=100, cmap=pl.cm.Reds, alpha=0.45)
    #pl.show()

if __name__ == "__main__":
    main(sys.argv[1:])

