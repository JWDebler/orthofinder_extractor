#!/usr/bin/env python3

import os
import sys
import re
import csv
import argparse
import glob
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prefix', nargs='+', help='prefix describing the species to extract')
parser.add_argument('-i', '--input', help='path to Orthogroups.tsv file (default = "Orthogroups.tsv" in the current directory)', default = 'Orthogroups.tsv')
parser.add_argument('-o', '--output', help='path to location for output files (default = current directory)')
parser.add_argument('-f', '--fasta', help = 'path to folder containing fasta files containing the protein sequences used to run Orthofinder (defaul = files are in current directory)')
args = parser.parse_args()

if args.input:
    orthogroups_file = Path(args.input)

if args.output:
    output_path = Path(os.path.abspath(args.output))
else:
    output_path = Path(os.path.join(os.getcwd(),'output'))

if args.fasta:
    fasta_files = Path(args.fasta)
else:
    fasta_files = Path(os.getcwd())

fastas = []
for file in fasta_files.glob('*.fasta'):
    fastas.append(file)

if args.prefix:
    prefix = args.prefix
else:
    print('ERROR - please provide at least one protein name prefix')
    sys.exit()

orthogroups = {}
species_specific_orthogroups = {}
proteins = {}

# Create output folder
try:
    os.makedirs(output_path)
except Exception:
    pass

# Overwrite files in output folder if any exist
for file in os.listdir(output_path):
    file_path = os.path.join(output_path, file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

# Read Orthogroups.tsv file
if not os.path.isfile(orthogroups_file):
    print('ERROR - missing:', orthogroups_file)
    sys.exit()

with open(orthogroups_file) as file:
    print('=======================')
    print('Reading Orthogroups.tsv')
    input = csv.reader(file, delimiter='\t')
    next(input, None) #skip header line
    for line in input:
        id = line[0]
        orthogroups[id] = line[1:]

# Parse fasta files
print('Parsing fasta files')
print('=======================')
for fasta in fastas:
    with open(fasta) as file:
        input = file.read().splitlines()
        for line in input:
            if not line.strip(): continue
            if line[0] == '>':
                name = line[1:]
                proteins[name] = ''
            else: 
                proteins[name] += line


#for protein in proteins:
#    



# Check if the orthogroups contain proteins from all the provided prefixes.
# If an orthogroup contains only members of a single prefix then add that 
# protein name to the 'species_specific_orthogroups' dictionary

for element in orthogroups: #element = orthogroup number
    counter = len(prefix)
    for p in prefix: # p = one of the prefixes
        for x in orthogroups[element]: # x = current element of orthogroup
            if p in x: # check if the element contains the prefix
                counter -= 1 # if it does, decrease the counter by 1
    
    if counter == 1: # if counter == 1 after the loop, the orthogroup contains only species specific elements
        for x in orthogroups[element]:
            if x != '': # if the orthogroup does not contain one of the prefixes, it contains empty list elements which we want to ignore
                temp = (x.split(", ")) # if there are several members from the same species, they are separated by a comma and a space
                for t in temp:
                    if element in species_specific_orthogroups:
                        species_specific_orthogroups[element].append(t)
                    else:
                        species_specific_orthogroups[element] = [t]


print('There are',len(species_specific_orthogroups),'species specific orthogroups')
print('Extracting species specific orthogroups to',output_path)
for x in prefix:
    for orthogroupID in species_specific_orthogroups:
    
        for protein in species_specific_orthogroups[orthogroupID]:
            print('>'+protein, '\n'+proteins[protein], file=open(os.path.join(output_path, orthogroupID+'.fasta'),'a'))
