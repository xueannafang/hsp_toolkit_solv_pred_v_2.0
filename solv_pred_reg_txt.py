cas_valid_symbol_list = ['0','1','2','3','4','5','6','7','8','9','-'] # '0123456789-'

def rm_spc(with_spc):
    """
    remove redundant spaces
    """
    no_space = with_spc.replace(' ', '')

    return no_space

def separate_multi_entry(multi_entry, separate_symbol = ";"):
    """
    separate cells with more than one elements, e.g., immiscible solvent index, synonyms
    """

    multi_entry_list = multi_entry.split(separate_symbol)
    
    return multi_entry_list
