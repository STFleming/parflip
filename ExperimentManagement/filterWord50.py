
import sys, getopt
import csv
import numpy as np

def main(argv):
    input_filename = ''
    output_filename = ''
    remove = 1
    try:
            opts, args = getopt.getopt(argv, "hoir", ["output=", "input=", "remove="])
    except getopt.GetoptError:
            print 'Usage: python filterWord50.py --input <linearaddr> --output <word50file> --remove <0|1> 0 extracts only word 50, 1 extracts everything but word 50 '
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python filterWord50.py --input <linearaddr> --output <word50file> --remove <0|1> 0 extracts only word 50, 1 extracts everything but word 50 '
            sys.exit()
        if opt in ("-i", "--input"):
            input_filename = arg
        if opt in ("-o", "--output"):
            output_filename = arg
        if opt in ("-r", "--remove"):
            remove = int(arg) 
    assert(input_filename != '')
    assert(output_filename != '')

    FRAME_MASK = 0b11111111111111111000000000000
    WORD_MASK =  0b00000000000000000111111100000
    BIT_MASK =   0b00000000000000000000000011111

    out = open(output_filename, "w")
    with open(input_filename) as f:
        lines = f.readlines();    
    
    #int_lines = [int(i) for i in lines]
    int_lines = [ ]
    for i in lines:
        try:
            if int(i) >= 10000000:
                int_lines.append(int(i))
        except ValueError:
            print "newline?"
        

    for linearaddr in int_lines:
        Frame = (linearaddr & FRAME_MASK) >> 12 
        word = (linearaddr & WORD_MASK) >> 5	
        if remove == 1:
            if word != 50:
                out.write(str(linearaddr) + '\n')	
        else:
            if word == 50:
                out.write(str(linearaddr) + '\n')	
	

if __name__ == "__main__":
    main(sys.argv[1:])

