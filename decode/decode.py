import os
import logging
from utils import *

def load_dna_file(dna_file_path):
    try:
        dna_file_obj = open(dna_file_path, 'r')
    except:
        logging.error("%s file not found", dna_file_path)
    return dna_file_obj

def main():
    dna_file_path = input("please input dna_file_path: ") 
    f = load_dna_file(dna_file_path)

    while(True):
        try:
            dna = f.readline().rstrip('\n')
        except:
            logging.info("Finished reading input file!")
            break

        if(len(dna) == 0):
            logging.info("Finished reading input file!")
            break

        #Check the length of dna fragment 
        if(len(dna) == get_check_length()):
            #convert symbol_id_codon to binary, default symbol_id_size 6nt
            symbol_id_size = 6
            symbol_id_codon = dna[0:symbol_id_size]
            symbol_id = codon_to_bin(symbol_id_codon)

            #convert RSCode to binary, default rscode_size 8nt
            rscode_size = 8
            rsc = dna_to_bin(dna[-rscode_size:])

            #get binary decoded symbol
            symbol_decoded = dna_to_bin(dna[symbol_id_size:-rscode_size])


        





def get_check_length():
    pass