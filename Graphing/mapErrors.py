import sys, getopt
import csv
import matplotlib.pylab as pl
import numpy as np

def main(argv):
    csvresfilename = ''
    try:
            opts, args = getopt.getopt(argv, "hi", ["input="])
    except getopt.GetoptError:
            print 'Usage: python mapErrors.py --input <results>.csv'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python mapErrors.py --input <results>.csv'
            sys.exit()
        if opt in ("-i", "--input"):
            csvresfilename = arg
    assert(csvresfilename != '')

    lastFrame=0
    firstFrame=0xFFFFFFFF
    with open(csvresfilename, 'rb') as csvfile:
        csvValues = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvValues:
            firstFrame
            if firstFrame > int(row[0]):
                firstFrame = int(row[0])
            lastFrame    = int(row[0])

    Derrors = np.zeros((101,((lastFrame+1) - firstFrame)), dtype='int32')
    Cerrors = np.zeros((101,((lastFrame+1) - firstFrame)), dtype='int32')


    with open(csvresfilename, 'rb') as csvfile:
        csvValues = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvValues:
            Frame = int(row[0]) - firstFrame
            Word = int(row[1])
            if row[3] != 'True':
#                Derrors[Word, Frame] = Derrors[Word, Frame] + 1
                Derrors[Word, Frame] = 1
            else:
#                Cerrors[Word, Frame] = Cerrors[Word, Frame] + 1
                Cerrors[Word, Frame] = 1

    pl.matshow(Derrors, fignum=100, cmap=pl.cm.Blues)
    pl.matshow(Cerrors, fignum=100, cmap=pl.cm.Reds, alpha=0.45)
    pl.show()

if __name__ == "__main__":
    main(sys.argv[1:])

