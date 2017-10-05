from diskhash import StructHash

__author__ = 'glazek'


class IndexedFastaReader(object):

    def __init__(self, index_file, fasta_file):
        """
        Reader of fasta file indexed with diskhash index.

        :param index_file: path to index file (diskhash index)
        :param fasta_file: path to fasta file
        """
        self.index = StructHash(index_file, 0, '2l', 'r')
        self.fasta = open(fasta_file, 'r')

    def lookup(self, sequence_id):
        """
        Lookup coordinates in the index file.

        :param sequence_id: sequence identifier
        :return: tuple: start position, length (in bases) and a boolean flag
                 indicating if the sequence includes newline characters.
        """
        s, lm = self.index.lookup(sequence_id)
        return s, lm >> 1, bool(lm%2)

    def get(self, sequence_id):
        """
        Get the sequence corresponding to given sequence identifier.

        Note: if you only need the length of the sequence, use get_length method instead.

        :param sequence_id: sequence identifier
        :return: sequence corresponding to given identifier
        """
        start, length, multiline = self.lookup(sequence_id=sequence_id)
        self.fasta.seek(start)
        if multiline:
            sequence = ''
            while True:
                line = self.fasta.readline().strip()
                if line.startswith('>'):
                    break
                sequence += line
        else:
            sequence = self.fasta.read(length)
        return sequence

    def get_length(self, sequence_id):
        """
        Get the length of the sequence corresponding to given identifier.

        :param sequence_id: sequence identifier
        :return: sequence length (in bases)
        """

        _, l, _ = self.lookup(sequence_id)
        return l
