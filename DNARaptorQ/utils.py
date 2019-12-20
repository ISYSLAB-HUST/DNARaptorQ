"""

"""
import numpy as np

DNAtable = "ACGT"
FourTable = "0123"
transForward = str.maketrans(FourTable, DNAtable)
transReverse = str.maketrans(DNAtable, FourTable)


def IntToFour(num):
    """
    int to 0,1,2,3
    Args:
        num (int):
    """
    _repr = np.binary_repr(num)
    _trans = []
    for item in range(0, len(_repr), 2):
        _trans.append(str(int(_repr[item:item + 2], 2)))
    return "".join(_trans)


def BinToDNA(numlist):
    """

    Args:
        numlist: list

    Returns:
        str
    """
    dna_list = []
    for num in numlist:
        DNA.append(IntToFour(num).translate(transForward))
    return "".join(dna_list)


def DNAToBin(dna_str):
    """
    DNA translate bytes: ACGT---00011011
    Args:
        dna_str: DNA str

    Returns:
        bytes
    """
    num_str = dna_str.translate(transReverse)
    num_list = []
    for item in range(0, len(num_str), 4):
        num = ""
        for a in num_str[item:item + 4]:
            num = num + np.binary_repr(a, 2)
        num_list.append(int(num, 2))
    return bytes(num_list)


codon = {'0': 'GCT', '1': 'TGT', '2': 'GAT', '3': 'GAA',
         '4': 'CAT', '5': 'ATG', '6': 'AAT', '7': 'CAA',
         '8': 'TAT', '9': 'TGG', 'a': 'GTT', 'b': 'AGA',
         'c': 'CCT', 'd': 'GGA', 'e': 'AAG', 'f': 'ACT'}


def reverseDictKeyValue():
    _reverse = {}
    for k, v in codon:
        _reverse[v] = k
    return _reverse


codonTo16 = reverseDictKeyValue()


def int_to_sixteen(symbol_id):
    bin_str = np.binary_repr(symbol_id, 32)
    # translate symbol id to bytes
    # get half of bytes str
    bin_str = bin_str[4:8] + bin_str[20:]
    # convert to a long string of binary values, only have low 8 bit of the symbol_ID
    symbol_id_16 = '0' * (4 - len(hex(int(bin_str, 2)))) + str(hex(int(bin_str, 2)))[2:]
    return symbol_id_16  # return symbol_ID in 2 bit Hexadecimal


def sixteen_to_dna(symbol_id_16):
    # This diction corresponds to genetic code preference in Arabidopsis thaliana
    dna_symbol_id = ''
    for i in symbol_id_16:
        dna_symbol_id += codon[i]
    return dna_symbol_id  # return symbol ID coding in DNA


def symbol_id_to_dna(symbol_id):  # This function can directly translate symbol ID into DNA
    # This diction corresponds to genetic code preference in Arabidopsis thaliana
    symbol_id_16 = '0' * (8 - len(hex(symbol_id))) + str(hex(symbol_id))[2:]
    # This step can be optimization. 4 corresponds to len of the DNA  code
    dna_symbol_id = ''
    for i in symbol_id_16:  # Translate symbol ID into DNA by dictionary
        dna_symbol_id += codon[i]
    return dna_symbol_id  # return symbol ID coding in 6 np DNA


def dna_to_symbol_id(dna_str):
    _16_str = ''
    for item in range(0, len(dna_str), 3):
        for a in dna_str[item:item + 3]:
            _16_str = _16_str + codonTo16[a]
    return int(_16_str, 16)
