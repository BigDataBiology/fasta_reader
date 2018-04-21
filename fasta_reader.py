from diskhash import StructHash

__author__ = 'glazek'


class IndexedFastaReader(object):

    def __init__(self, fasta_file, index_file=None, use_mmap=False):
        """
        Reader of fasta file indexed with diskhash index.

        :param fasta_file: path to fasta file
        :param index_file: path to index file (diskhash index). If None, uses (fasta_file + '.dhi')
        """
        if index_file is None:
            index_file = fasta_file + '.dhi'
        self.index = StructHash(index_file, 0, '2l', 'r')
        self.fasta = open(fasta_file, 'rb')
        self.use_mmap = use_mmap
        if use_mmap:
            import mmap
            self.data = mmap.mmap(self.fasta.fileno(), 0, access=mmap.ACCESS_READ)

    def lookup(self, sequence_id):
        """
        Lookup coordinates in the index file.

        :param sequence_id: sequence identifier
        :return: tuple: start position, length (in bases) and a boolean flag
                 indicating if the sequence includes newline characters.
        """
        try:
            s, lm = self.index.lookup(sequence_id)
            return s, lm >> 1, bool(lm%2)
        except TypeError:
            return None

    def get(self, sequence_id):
        """
        Get the sequence corresponding to given sequence identifier.

        Note: if you only need the length of the sequence, use get_length method instead.

        :param sequence_id: sequence identifier
        :return: sequence corresponding to given identifier or None if identifier not found
        """

        coordinates = self.lookup(sequence_id=sequence_id)
        if not coordinates:
            return None
        start, length, multiline = coordinates
        if self.use_mmap:
            if not multiline:
                return self.data[start:start+length]
            end = self.data.find(b'\n>', start)
            if end == -1:
                seqdata = self.data[start:]
            else:
                seqdata = self.data[start:end]
            seqdata = seqdata.replace(b'\n', b'')
            assert len(seqdata) == length, "Retrieved length should match stored length"
            return seqdata


        self.fasta.seek(start)
        if multiline:
            sequence = []
            while True:
                line = self.fasta.readline().strip()
                if not line or line.startswith(b'>'):
                    break
                sequence.append(line)
            return b''.join(sequence)
        return self.fasta.read(length)

    def get_length(self, sequence_id):
        """
        Get the length of the sequence corresponding to given identifier.

        :param sequence_id: sequence identifier
        :return: sequence length (in bases) or None if identifier not found
        """

        coordinates = self.lookup(sequence_id)
        if not coordinates:
            return None
        return coordinates[1]

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('fasta_file',  metavar='FASTA',
                        help='fasta file')
    parser.add_argument('--index', required=False,
                        help='path to the index file (by default: fasta_file + .dhi',
                        dest='index_file')
    parser.add_argument('query', metavar='QUERY',
			nargs='*',
                        help='Name(s) of sequence(s) to retrieve')
    parser.add_argument('-F',
                        dest='query_file')

    return parser.parse_args()

def main():
    from itertools import chain
    args = parse_args()
    ix = IndexedFastaReader(args.fasta_file, args.index_file)
    qs = [args.query]
    if args.query_file:
        qs.append(open(args.query_file))
    for q in chain.from_iterable(qs):
        q = q.strip()
        s = ix.get(q)
        if s:
            print(">"+q)
            print(s.decode('ascii'))

if __name__ == '__main__':
    main()
