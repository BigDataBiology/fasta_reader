import argparse

from diskhash import StructHash


__author__ = 'glazek'

description = '''Script for indexing a fasta file using diskhash.

If the output file path is not defined, the index will be stored in <input_file>.dhi

Produced index has gene/contig names as keys and a pair of integers as value. 
The first integer is the start position of the sequence in the source file, 
the second one encodes the length of the sequence and a flag indicating 
if the sequence is stored in multiple lines or not (as the youngest bit).    
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
    """
    Check the maximal key length in a fasta file.
    :param input_file: path to fasta file
    :return: length of longest sequence identifier
    """
    max_line = 0
    with open(input_file, 'r') as fasta:
        for line in fasta:
            line = line.split()[0]  # only the first token is the identifier
            if line.startswith('>') and (len(line) - 1) > max_line:
                max_line = len(line) - 1  # without '>'
    return max_line


def create_index(input_file, output_file, key_length):
    """
    Create diskhash index for a fasta file.
    For each sequence the offset, length (in bases) and a flag indicating
    if the sequence is stored in multiple lines or not.
    The flag is encoded together with length (as the youngest bit).

    :param input_file: path to the fasta file to index
    :param output_file: path to the index
    :param key_length: Maximal length of index key (in this case: sequence identifier)
    :return:
    """
    print("Creating diskhash index for {input_file}.\n\n"
          "Index will be stored in {output_file}.\nKey length set to {key_length}.".format(**locals()))
    tb = StructHash(output_file, key_length, '2l', 'w')

    with open(input_file, 'r') as fasta:
        line = fasta.readline()
        header = None
        position_start = 0
        seq_len = 0
        multiline = None
        while line:
            if line.startswith('>'):
                if header: tb.insert(header, position_start, (seq_len << 1) + multiline)
                header = line.split()[0].lstrip('>')
                position_start = fasta.tell()
                multiline = None
                seq_len = 0
            else:
                multiline = multiline is not None
                seq_len += len(line.strip())
            line = fasta.readline()
    print("Index creation finished!")


def main():
    args = parse_args()
    ifile = args.input_file
    ofile = args.output_file if args.output_file else ifile + '.dhi'
    key_length = check_max_header_len(input_file=ifile) + 1
    create_index(input_file=ifile, output_file=ofile, key_length=key_length)


if __name__ == '__main__':
    main()
