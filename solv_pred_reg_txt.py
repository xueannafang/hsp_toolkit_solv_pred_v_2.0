"""

solv_pred_reg_txt formatting specific input into required structures.

"""

from datetime import datetime

cas_valid_symbol_list = ['0','1','2','3','4','5','6','7','8','9','-'] # valid characters, symbols or numbers that are supposed to appear in usr input cas

def rm_spc(with_spc: str) -> str:
    """Return string without spaces.

    Args:
        with_spc (str): input string that may contain redundant space.
    
    Returns:
        str: no_space
    """
    no_space = with_spc.replace(' ', '')

    return no_space

def separate_multi_entry(multi_entry: str, separate_symbol: str = ";") -> list:
    """return separated text based on separate symbol.

    Args:
        multi_entry (str): multi-entry info, e.g., immiscible solvent index, synonyms, etc.
        separate_symbol (str, optional): symbol to separate. Defaults to ";".

    Returns:
        list: separated info list.
    """
    

    multi_entry_list = multi_entry.split(separate_symbol)
    
    return multi_entry_list


def date_time_form(now: datetime.datetime) -> str:
    """return formatted time as part of the file name.

    Args:
        now (datetime.datetime): current time

    Returns:
        _type_: _description_
    """
    
    dd = str(now.day)
    mm = str(now.month)
    yyyy = str(now.year)
    t_hh = str(now.hour)
    t_mm = str(now.minute)
    t_ss = str(now.second)

    if len(dd) == 1:
        dd = '0' + dd
    
    if len(mm) == 1:
        mm = '0' + mm
    
    if len(t_hh) == 1:
        t_hh = '0' + t_hh
    
    if len(t_mm) == 1:
        t_mm = '0' + t_mm
    
    if len(t_ss) == 1:
        t_ss = '0' + t_ss
    
    time_comb = mm + dd + yyyy + t_hh + t_mm + t_ss

    return time_comb
