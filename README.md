# orthofinder_extractor
A Python3 script that parses the `Orthogroups.tsv` output file created by [Orthofinder](https://github.com/davidemms/OrthoFinder) and extracts species specific orthogroups (orthogroups that only appear in a single species tested).


# Prerequisits
- Python3
- Orthogroups.tsv (created by Orthofinder in the `Orthogroups` result directory)
- Fasta files containing protein sequences which were used to run Orthofinder


# Usage

usage: 
```
extract_species_specific_orthogroups.py [-h] [-p PREFIX [PREFIX ...]] [-i INPUT] [-o OUTPUT] [-f FASTA]

-p: a list of protein prefixes used in the fasta files to distinguish species
-i: path to the Orthogroups.tsv file
-o: path to store extracted Orthogroups
-f: path to a directory containing the fasta files
```

## Usage example 1
Expects `Orthogroups.tsv` and all FASTA files to be in the same directory.  
FASTA files look like this:  

file1.fasta:
```
>Alen_Al4_ctg00.g1.t1
MPTGDKLIEIKYSDAVHKFSNWWIE...
...
```
file2.fasta:
```
>Arab_Me14_ctg00_-_Arab_Me14_ctg00.g1.t1
MLHQLDRIVIDECHVLLELTQDWRP...
...
```
Command:
```
extract_species_specific_orthogroups.py -p Alen Arab
```
This will parse your `Orthogroups.tsv` and look for orthogroups that only contain proteins starting with `Alen` or `Arab` and then use the provided fasta files to extract those orthogroups into separate fasta files for each orthogroups.

## Usage example 2
- provide path to `Orthogroups.tsv`
- provide path to FASTA files
- provide path to output directory

```
extract_species_specific_orthogroups.py -p Alen Arab -i /path/to/Orthogroups.tsv -f /path/to/directory/containing/fastas/ -o /path/to/output/directory/
```
- uses `Alen` and `Arab` as prefixes to look for in the `Orthogroups.tsv` file
- uses the `Orthogroups.tsv` file located at `/path/to/Orthogroups.tsv`
- uses FASTA files in `/path/to/directory/containing/fastas/`
- saves output files to `/path/to/output/directory`
