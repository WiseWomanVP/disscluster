#  Generate GraphViz from SIM_TEXT output
#
#  WiseWoman @ VroniPlag Wiki
#  April 2014
#
#    1. First convert PDFs into .txt files and have them all in one folder
#
#    2. Then run sim_text on the folder
#
#    sim_text.exe -o output.log -d -p -t 1 -r 7 *.txt
#
#    -o Output to output.log
#    -d use diff format for output
#    -p use percentage format for output
#    -t cutoff percentage is 1
#    -r minimum number of tokens in sequence (run size) is 7
#    use all files ending in .txt
#
#    3. The SIM_TEXT output is:
#    Doktorarbeit(21).txt consists for 19 % of Doktorarbeit(26).txt material
#
#    The GraphViz input needs to be:
#    "Doktorarbeit(21)" -> "Doktorarbeit(26)" [label="19"]
# --------------------
#  Usage:
#  execfile('MakeGraphViz.py')
#  >>> transform ("input.txt", "output.dot")
#  >>> transform ("input.txt", "output.dot", 10)
#
#  or just call
#
#  python MakeGraphViz.py input output [threshhold] 

import sys

def startit():
    anz = len (sys.argv)
    if ((anz < 3) or (anz > 4)) :
        print "Usage: python MakeGraphViz.py input output [threshhold] "
        sys.exit (1)
    if anz is 3:
        transform (sys.argv[1], sys.argv[2])
    if anz is 4:
        transform (sys.argv[1], sys.argv[2], int(sys.argv[3]))


def transform (infile, outfile, threshhold=5):
    input = open(infile, 'r')
    output = open(outfile, 'w')
    header(output)
    for line in input:
        # ignore empty lines
        if not line.strip():
            continue
        # tokenize
        words = line.split()
        # ignore lines like this
        if words[0].startswith('File'):
            continue
        if words[0].startswith('Total:'):
            continue
        # remove the file type in the from file
        tmp= words[0].split('.')
        fromFile = tmp[0]
        # What percentage is identical?
        amount = words[3]
        # ignore line if less than threshhold
        if int(amount) < threshhold:
            continue
        # target
        tmp = words[6].split('.')
        toFile = tmp[0]
        # output the line
        outLine = '"' + fromFile + '" -> "' + toFile + '" [label="' + amount + '"]\n'
        output.write(outLine)
    footer(output)

def header(output):
    output.write('digraph Cluster { \n')
    output.write('graph [ bgcolor=white, resolution=128, fontname=Arial, fontcolor=blue,fontsize=12, nodesep="0.7" ]; \n')
    output.write('node [ fontname=Arial, fontcolor=blue, fontsize=11];\n')
    output.write('edge [ fontname=Helvetica, fontcolor=red, fontsize=11 ];\n\n')


def footer(output):
    output.write('\n overlap=false\n')
    output.write('}\n')


if __name__ == '__main__':
    startit()
