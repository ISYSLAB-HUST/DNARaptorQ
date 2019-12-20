import numpy as np
import logging

intab = "0123"
outtab = "ACGT"

trantab = str.maketrans(intab, outtab)
revtab = str.maketrans(outtab, intab)

def dna_to_bin(dna_str):
    #convert a string like 'ACTCA' to a binary string like '0001110100'
    num = dna_str.translate(revtab)
    bin_str = ''.join('{0:02b}'.format(int(num[t])) for t in range(0, len(num),1))
    return bin_str

def dna_to_int_array(dna_str):
    #convert a string like ACTCA to an array of ints like [10, 2, 4]
    num = dna_str.translate(revtab)
    s = ''.join('{0:02b}'.format(int(num[t])) for t in range(0, len(num),1))
    int_array = [int(s[t:t+8],2) for t in range(0,len(s), 8)]
    return int_array


def codon_to_bin(symbol_id_codon):
    #convert symbol_id_codon to a binary string, default symbol_id_codon 6nt
    rev_codon = {'GCT': '0000', 'TGT': '0001', 'GAT': '0010', 'GAA': '0011',
                 'CAT': '0100', 'ATG': '0101', 'AAT': '0110', 'CAA': '0111',
                 'TAT': '1000', 'TGG': '1001', 'GTT': '1010', 'AGA': '1011',
                 'CCT': '1100', 'GGA': '1101', 'AAG': '1110', 'ACT': '1111'}
    bin_str = ''
    for t in range(0, len(symbol_id_codon), 3):
        codon = symbol_id_codon[t:t+3]
        if codon in rev_codon:
            bin_str += rev_codon[codon]
        else:
            logging.error("existing error codon!")

    return bin_str



