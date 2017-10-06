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
        :return: sequence length (in bases) or None if identifier not found
        """

        coordinates = self.lookup(sequence_id)
        if not coordinates:
            return None
        return coordinates[1]
