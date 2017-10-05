from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

__author__ = 'glazek'


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fasta_reader',

    version='0.1.0',

    description='Diskhash indexed fasta reader',
    long_description=long_description,

    url='https://git.embl.de/glazek/fasta_reader',

    author='Anna Glazek',
    author_email='anna.glazek@embl.de',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='fasta diskhash index',

    py_modules=["fasta_reader", "index_fasta"],

    install_requires=['diskhash'],

    entry_points={
        'console_scripts': [
            'index_fasta=index_fasta:main',
        ],
    },
)