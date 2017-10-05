# Diskhash indexed fasta reader


## Examples

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
ifr.get_lenght('my_seq_id1')
# get the sequence
ifr.get('my_seq_id1')
# check number of sequences
ifr.index.size()
```
 