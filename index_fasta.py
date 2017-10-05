import argparse

from diskhash import StructHash


__author__ = 'glazek'

description = '''Script for indexing a fasta file using diskhash.

If the output file path is not defined, the index will be stored in <input_file>.dhi

Produced index has gene/contig names as keys and a pair of integers as value. 
The first integer is the start position of the sequence in the source file, 
the second one encodes the end position and a flag    
'''


def parse_args():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description=description)

    parser.add_argument('input_file',  metavar='FASTA',
                        help='fasta file to index')
    parser.add_argument('-o', '--output', required=False,
                        help='path to the output index file',
                        dest='output_file')

    return parser.parse_args()


def check_max_header_len(input_file):
    max_line = 0
    with open(input_file, 'r') as fasta:
        for line in fasta:
            line = line.split()[0]
            if line.startswith('>') and (len(line) - 1) > max_line:
                max_line = len(line) - 1  # without '>' and '\n'
    return max_line + 1


def create_index(input_file, output_file, header_len=15):
    print(header_len)
    tb = StructHash(output_file, header_len, '2l', 'w')

    with open(input_file, 'r') as fasta:
        line = fasta.readline()
        header = None
        position_start = 0
        position_end = fasta.tell()
        multiline = None
        while line:
            if line.startswith('>'):
                if header: tb.insert(header, position_start, (position_end << 1) + multiline)
                header = line.split()[0].lstrip('>')
                position_start = fasta.tell()
                multiline = None
            elif multiline is None:
                multiline = False
            else:
                multiline = True
            position_end = fasta.tell()
            line = fasta.readline()


if __name__ == '__main__':
    args = parse_args()
    ifile = args.input_file
    ofile = args.output_file if 'output_file' in args else ifile + '.dhi'
    create_index(input_file=ifile, output_file=ofile, header_len=check_max_header_len(input_file=ifile))
