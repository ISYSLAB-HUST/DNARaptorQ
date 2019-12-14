def int_to_sixteen(symbol_id):

    bin_data = '{0:08b}'.format(symbol_id)
    # convert to a long string of binary values, only have low 8 bit of the symbol_ID

    symbol_id_16 = '0' * (4-len(hex(int(bin_data, 2)))) + str(hex(int(bin_data, 2)))[2:]

    return symbol_id_16  # return symbol_ID in 2 bit Hexadecimal


def sixteen_to_dna(symbol_id_16):

    codon = {'0': 'GCT', '1': 'TGT', '2': 'GAT', '3': 'GAA',
             '4': 'CAT', '5': 'ATG', '6': 'AAT', '7': 'CAA',
             '8': 'TAT', '9': 'TGG', 'a': 'GTT', 'b': 'AGA',
             'c': 'CCT', 'd': 'GGA', 'e': 'AAG', 'f': 'ACT'}
    # This diction corresponds to genetic code preference in Arabidopsis thaliana


    dna_symbol_id = ''

    for i in symbol_id_16:
    
        dna_symbol_id += codon[i]

    return dna_symbol_id  # return symbol ID coding in DNA








def int_to_dna(symbol_id):  # This function can directly translate symbol ID into DNA

    codon = {'0': 'GCT', '1': 'TGT', '2': 'GAT', '3': 'GAA',
             '4': 'CAT', '5': 'ATG', '6': 'AAT', '7': 'CAA',
             '8': 'TAT', '9': 'TGG', 'a': 'GTT', 'b': 'AGA',
             'c': 'CCT', 'd': 'GGA', 'e': 'AAG', 'f': 'ACT'}
    # This diction corresponds to genetic code preference in Arabidopsis thaliana

    symbol_id_16 = '0' * (4-len(hex(symbol_id)))+str(hex(symbol_id))[2:]

    #This step can be optimization. 4 corresponds to len of the DNA  code

    dna_symbol_id = ''

    for i in symbol_id_16:  # Translate symbol ID into DNA by dictionary

        dna_symbol_id += codon[i]

    return dna_symbol_id               # return symbol ID coding in 6 np DNA


