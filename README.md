# Diskhash indexed fasta reader

Little package for indexing fasta files with diskhash and using fasta files indexed in this way.

## Use examples

### Indexing fasta file

To create a diskhash based index for a fasta file use the index_fasta command line tool:

```bash
index_fasta my_fasta.fna -o my_index.dhi
```

### Using indexed fasta file

Sequences from diskhash indexed fasta file can be accessed using *IndexedFastaReader*: 

```python
from fasta_reader import IndexedFastaReader

ifr = IndexedFastaReader(fasta_file='my_fasta.fna', index_file='my_index.dhi')

# check length of sequence
ifr.get_length('my_seq_id1')
# get the sequence
ifr.get('my_seq_id1')
# check number of sequences
ifr.index.size()
```

## Dependencies

[diskhash](https://github.com/luispedro/diskhash) package is required. Code was tested with version 0.2.
When installed with setup.py, the package will be installed from pypi. 
