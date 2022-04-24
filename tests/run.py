import subprocess
from os import path

QUERIES = [
'GMGC10.046_019_582.RPMJ',
'GMGC12.046_019_582.RPMJ', # Will fail
'GMGC10.038_643_172.UNKNOWN',
'FAIL',
]


if not path.exists('GMGC10.100.fna.xz'):
    subprocess.check_call(['xz', 'GMGC10.100.fna.xz'])
subprocess.check_call(['index_fasta', 'GMGC10.100.fna.xz'])
for q in QUERIES:
    fna = 'GMGC10.100.fna.xz'
    assert \
        subprocess.check_output(['fasta_reader', fna, q]) \
            == \
        subprocess.check_output(['python', 'naive.py', fna, q])
subprocess.check_call(['unxz', 'GMGC10.100.fna.xz'])
for q in QUERIES:
    fna = 'GMGC10.100.fna'
    assert \
        subprocess.check_output(['fasta_reader', fna, q]) \
            == \
        subprocess.check_output(['python', 'naive.py', fna, q])
subprocess.check_call(['xz', 'GMGC10.100.fna'])
