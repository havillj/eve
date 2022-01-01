# EVE

## Installation

## Dependencies

### Python modules

EVE is written in Python 3 (version 3.6 or later) and requires the following nonstandard modules:
- biopython
- dna_features_viewer
- intervaltree
- lxml
- matplotlib
- numpy
- pysam

They should be easy to install using `pip` (or `pip3`).  For example:

```
pip3 install biopython
```

### Samtools

Samtools can be found at http://www.htslib.org.

Once installed, assign the path to `samtools` to the variable `SAMTOOLS_EXEC` in `config.py`.  For example:

```
SAMTOOLS_EXEC = '/usr/bin/samtools'
```

### SPAdes

The SPAdes assembler is available at https://cab.spbu.ru/software/spades/.

Once installed, assign the path to `spades.py` to the variable `SPADES_EXEC` in `config.py`.  For example:

```
SPADES_EXEC = '/usr/local/bin/spades.py'
```

### BLAST

BLAST can be downloaded from https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download.

Once installed, assign the path to the `blastn` executable to the variable `BLAST_EXEC` in `config.py`.  For example:

```
BLAST_EXEC = '/usr/local/bin/blastn'
```

## Set up

### Directories

The following three directories should be specified in `config.py`:

```
ROOT_DIR = '/Volumes/Data/'              # root directory where all data files related to EVE will be located
SPECIMENS_DIR = ROOT_DIR + 'specimens/'  # path for original specimen BAM files
RESULTS_DIR = ROOT_DIR + 'results/'      # path for all results
```

See the [Directory structure](#directory-structure) section below for details on the contents of the `RESULTS_DIR` directory.

### BLAST databases

You will need two BLAST nucleotide databases: 
- one containing the virus sequences for which you wish to search and
- one containing the host reference genome

Assuming your virus sequences are contained in a FASTA file named `virus.fasta`, you can create the database with

```
makeblastdb -in virus.fasta -dbtype nucl -parse_seqids -title "virusdb" -out virusdb
```

Similarly, if your host reference genome is contained in `host.fasta`, you can create the host database with

```
makeblastdb -in host.fasta -dbtype nucl -parse_seqids -title "hostdb" -out hostdb
```

Once these databases exist, assign their names to the variables `VIRUS_DB` and `HOST_DB` in `config.py`:

```
VIRUS_DB = 'virusdb'
HOST_DB = 'aegyptidb'
```

To make diagrams more readable, also edit the variable `CHR_NAMES` in `config.py` so that the accession number of each host chromosome corresponds to the correct chromosome number.  For example, for *Aedes aegypti*:

```
CHR_NAMES = {'NC_035107.1': 'Chr1', 'NC_035108.1': 'Chr2', 'NC_035109.1': 'Chr3'}
```

### Host genome features

To identify repeat sequences and other genomic features near putative viral insertions, EVE needs files in GFF3 format that list these features.  For example, these files for *Aedes aegpyti* can be obtained from http://vectorbase.org ([here](https://vectorbase.org/common/downloads/release-52/AaegyptiLVP_AGWG/gff/data/VectorBase-52_AaegyptiLVP_AGWG.gff) and [here](https://vectorbase.org/common/downloads/Legacy%20VectorBase%20Files/Aedes-aegypti/Aedes-aegypti-LVP_AGWG_REPEATFEATURES_AaegL5.gff3.gz)).  Once downloaded and decompressed, add their names to the variables `BASE_FEATURES_GFF3_FILENAME` and `REPEAT_FEATURES_GFF3_FILENAME` in `config.py`.  For example:

```
GFF3_DIR = ROOT_DIR + 'gff3/'
BASE_FEATURES_GFF3_FILENAME = GFF3_DIR + 'Aedes-aegypti-LVP_AGWG_BASEFEATURES_AaegL5.2.gff3'
REPEAT_FEATURES_GFF3_FILENAME = GFF3_DIR + 'Aedes-aegypti-LVP_AGWG_REPEATFEATURES_AaegL5.gff3'
```

The GFF3 files may identify host chromosomes simply by number.  To translate between these and the chromosomes' accession numbers in the host reference genome, edit the variable `CHR_NUMBERS` in `config.py`.  For example, for *Aedes aegypti*, this would look like:

```
CHR_NUMBERS = {'1': 'NC_035107.1', '2': 'NC_035108.1', '3': 'NC_035109.1', 'MT': 'NC_035159.1'}
```
### Specimen populations

If your specimens come from different populations, you can specify those by editing the `POPULATIONS` dictionary in `config.py`.  The keys are the names of the populations and the values are patterns that appear in the file names of specimens from those populations.  For example, in the following, the region `'USA'` is assigned to any specimen containing either `'USA'` or `'AZ'` in its file name.

```
POPULATIONS = {'Angola': ['Angola'], 
               'Argentina': ['Argentina', 'US_U'], 
               'Australia': ['Australia'], 
               'Brazil': ['Brazil'], 
               'French-Polynesia': ['FrenchPolynesia'],
               'Gabon': ['Gabon'], 
               'Mexico': ['Mexico'], 
               'Philippines': ['Philippines'], 
               'South-Africa': ['South_Africa'], 
               'Thailand': ['Thailand'], 
               'USA': ['USA', 'AZ'], 
               'Vietnam': ['Vietnam']}
```
### Preferred virus accession numbers

Since there are commonly many genomic sequences in a viral database corresponding to the same viral species, EVE only retains hits from one representative of a species in each contig.  You can optionally specify a preferred accession number for each species by editing the `PREFERRED_ACCS` variable in `config.py`.  For example:

```
PREFERRED_ACCS = {'Aedes anphevirus':               ['gb|MH037149.1|'], 
                  'Australian Anopheles totivirus': ['ref|NC_035674.1|'], 
                  'Culex ohlsrhavirus':             ['ref|NC_035132.1|'], 
                  'Phasi Charoen-like phasivirus':  ['ref|NC_038263.1|'], 
                  'Wuhan Mosquito Virus 6':         ['gb|MF176251.1|']}
```

## Parameters

There are several ways to customize the execution of EVE.  These options are described in detail in the comments of [config.py](config.py).

## Usage

```
eve.py
```

```
insertsites.py
```

## Directory structure

In the following directory tree, `N` is used to represent the last in a series, not any particular number.

```
<ROOT_DIR>
├── specimens
│   ├── <SPECIMEN 1>.bam
│   :
│   └── <SPECIMEN N>.bam
│   
└── results
    ├── results.tsv
    ├── specimens
    │   ├── <SPECIMEN 1>
    │   │   ├── <SPECIMEN 1>_unmapped_with_mates.bam
    │   │   ├── diagrams
    │   │   │   ├── <VIRUS_FAMILY 1>
    │   │   │   │   ├── <CONTIG 1>.pdf
    │   │   │   │   :
    │   │   │   │   └── <CONTIG N>.pdf
    │   │   │   :
    │   │   │   └── <VIRUS_FAMILY N>
    │   │   │       ├── 
    │   │   │       :   (as above)
    │   │   │       └── 
    │   │   ├── scaffolds
    │   │   │   ├── blast_scaffolds.csv
    │   │   │   └── scaffolds.fasta
    │   │   ├── sequences
    │   │   │   ├── <SPECIMEN 1>_hits_aligned.fasta
    │   │   │   └── <SPECIMEN 1>_hits_unaligned.fasta
    │   │   ├── xml
    │   │   │   └── <SPECIMEN 1>_hits.xml
    │   │   └── spades
    │   │       ├──
    │   │       :   (SPAdes work files)
    │   │       └── 
    │   :
    │   └── <SPECIMEN N>
    │       ├── 
    │       :   (as above)
    │       └──
    │
    └── viruses
        ├── diagrams
        │   ├── <VIRUS_FAMILY 1>
        │   │   ├── <VIRUS_FAMILY 1 VIRUS 1>_all.pdf
        │   │   :
        │   │   └── <VIRUS_FAMILY 1 VIRUS N>_all.pdf
        │   :
        │   └── <VIRUS_FAMILY N>
        │       ├── 
        │       :   (as above)
        │       └── 
        └── sequences
            ├── <VIRUS_FAMILY 1>
            │   ├── <VIRUS_FAMILY 1>_per_contig_aligned.fasta
            │   ├── <VIRUS_FAMILY 1>_per_contig_unaligned.fasta
            │   ├── <VIRUS_FAMILY 1>_per_specimen_aligned.fasta
            │   ├── <VIRUS_FAMILY 1 VIRUS 1>_per_contig_aligned.fasta
            │   ├── <VIRUS_FAMILY 1 VIRUS 1>_per_contig_unaligned.fasta
            │   ├── <VIRUS_FAMILY 1 VIRUS 1>_per_contig_with_flanks.fasta
            │   ├── <VIRUS_FAMILY 1 VIRUS 1>_per_specimen_aligned.fasta
            │   :
            │   ├── <VIRUS_FAMILY 1 VIRUS N>_per_contig_aligned.fasta
            │   ├── <VIRUS_FAMILY 1 VIRUS N>_per_contig_unaligned.fasta
            │   ├── <VIRUS_FAMILY 1 VIRUS N>_per_contig_with_flanks.fasta
            │   ├── <VIRUS_FAMILY 1 VIRUS N>_per_specimen_aligned.fasta
            │   └── clustered
            │       ├── <VIRUS_FAMILY 1 VIRUS 1>_per_contig_aligned_clustered_k?.fasta
            │       ├── <VIRUS_FAMILY 1 VIRUS 1>_per_contig_aligned_clustered_k?.txt
            │       :
            │       ├── <VIRUS_FAMILY 1 VIRUS N>_per_contig_aligned_clustered_k?.fasta
            │       └── <VIRUS_FAMILY 1 VIRUS N>_per_contig_aligned_clustered_k?.txt
            :
            └── <VIRUS_FAMILY N>
                ├── 
                :   (as above)
                └── 
```
