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
