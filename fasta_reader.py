from diskhash import StructHash

__author__ = 'glazek'


class IndexedFastaReader(object):

    def __init__(self, index_file, fasta_file):
        self.index = StructHash(index_file, 0, '2l', 'r')
        self.fasta = open(fasta_file, 'r')

    def lookup(self, gene_id):
        s, em = self.index.lookup(gene_id)
        return s, em >> 1, bool(em%2)

    def get(self, gene_id):
        start, end, multiline = self.lookup(gene_id=gene_id)
        self.fasta.seek(start)
        sequence = self.fasta.read(end - start)
        if multiline:
            sequence = sequence.replace('\n', '')
        return sequence