# Diskhash indexed fasta reader

Little package for indexing fasta files with diskhash and using fasta files indexed in this way.

## Use examples

### Indexing fasta file

To create a diskhash based index for a fasta file use the `index_fasta` command line tool:

```bash
index_fasta GMGC10.10.fna
```

### Using indexed fasta file (command line)

Use the `fasta_reader` command line tool passing as a first argument the
previously-indexed FASTA file and then a list of sequences to retrieve

```bash
fasta_reader GMGC10.10.fna GMGC10.027_772_348.UNKNOWN GMGC10.014_522_894.UNKNOWN
```

Will produce

```
>GMGC10.027_772_348.UNKNOWN
ATGTATGACTGCGGGCACTACCTGCCAGAGCCGTTCCCGGATGAACTGGCGGATGAATTCAGAATGTTCTTTCTCTTGAATCGCCACGGGTTTAACAGACACCTCCGAGTCATTTAA
>GMGC10.014_522_894.UNKNOWN
ATGAATATATCGGAAATTGAAAAAATCGCAGCAAAGGAAATATTATTATGGGTTAAAGAGAGGATATTTCAGAAAAATGCCCTCCCGTTCAAGGGGAAGGCGAGGAATTACAGATAG
```

Note that if the sequence is not found, then no output is produced


### Using indexed fasta file (from Python)

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
