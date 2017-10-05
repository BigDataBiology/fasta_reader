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

    def lookup(self, gene_id):
        """
        Lookup coordinates in the index file.

        :param gene_id: sequence identifier
        :return: tuple: start position, end position and a boolean flag
                 indicating if the sequence includes newline characters.
        """
        s, em = self.index.lookup(gene_id)
        return s, em >> 1, bool(em%2)

    def get(self, gene_id):
        """
        Get the sequence of given contig/gene.

        :param gene_id: sequence identifier
        :return: sequence corresponding to given identifier
        """
        start, end, multiline = self.lookup(gene_id=gene_id)
        self.fasta.seek(start)
        sequence = self.fasta.read(end - start)
        if multiline:
            sequence = sequence.replace('\n', '')
        return sequence
