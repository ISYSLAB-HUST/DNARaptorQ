def int_to_sixteen(symbol_ID):    
   
    bin_data = '{:032b}'.format(symbol_ID)                #convert to a long sring of binary values, only have low 8 bit of the symbol_ID

    half_bin_data = bin_data[16:]

    hex_data = '{:04x}'.format(int(half_bin_data , 2))      # 2 to 16 ,and complement 0 

    return hex_data                                        #return symbol_ID in Hexadecimal,str





def int_to_sixteen(symbol_ID):    
   
    bin_data = '{:032b}'.format(symbol_ID)                #convert to a long sring of binary values, only have low 8 bit of the symbol_ID

    half_bin_esi = bin_data[16:]

    sbn=bin_data[:3]

    hex_esi = '{:04x}'.format(int(half_bin_esi , 2))         # 2 to 16 ,and complement 0 

    hex_sbn = '{:02x}'.format(int(sbn , 2))

    return hex_sbn+hex_esi                                    #return sbn,esi in Hexadecimal,str






def sixteen_to_dna(symbol_ID_16):
    
    codon={'0':'GCT','1':'TGT','2':'GAT','3':'GAA',
           '4':'CAT','5':'ATG','6':'AAT','7':'CAA',
           '8':'TAT','9':'TGG','a':'GTT','b':'AGA',
           'c':'CCT','d':'GGA','e':'AAG','f':'ACT'}   # This diction corresponds to genetic code preference in Arabidopsis thaliana

    dna_symbol_ID=''

    for i in str(symbol_ID_16):

        dna_symbol_ID +=codon[i]                        

    return dna_symbol_ID                                 # return symbol ID coding in DNA
