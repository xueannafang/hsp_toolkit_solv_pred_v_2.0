"""
solv_pred_fetch_info includes functions to extract required information from database
"""

import json

def fetch_name(cas: str, db_json: json) -> str:
    """return solvent name of cas

    Args:
        cas (str): cas to be fetched
        db_json (json): database js

    Returns:
        str: solvent name
    """

    for i, entry in enumerate(db_json):
        
        if cas == entry['CAS']:
            solv_name = entry['Name']
            
    return solv_name



def fetch_info_from_cas_list(to_fetch_cas_list, to_fetch_key, db_info_dict):
    """
    fetech the required information from the db_info_dict
    to_fetch argument is a list from the following items: ['No.', 'CAS', 'Name', 'D', 'P', 'H', 'Mole_vol', 'ims_idx', 'bp', 'mw', 'viscosity', 'vis_temp', ''heat_of_vap', 'hov_temp', 'SMILES']
    """
    # to_fetch_cas_idx = []
    all_cas_in_db = db_info_dict['CAS']

    all_key_dict_list = []

    for cas in to_fetch_cas_list:

        tuple_to_dict_list = []

        for i, db_cas in enumerate(all_cas_in_db):

            if db_cas == cas:
                
                tuple_to_dict_list.append(tuple(['CAS', db_info_dict['CAS'][i]]))

                for key in to_fetch_key:

                    tuple_each_key = tuple([key, db_info_dict[key][i]])

                    tuple_to_dict_list.append(tuple_each_key)

                key_dict = dict(tuple_to_dict_list)
        
        all_key_dict_list.append(key_dict)
    
    return all_key_dict_list


def fetch_idx_cas_hsp(to_fetch_cas_list: list, db_info_list: list) -> list:
    """fetch current hsp of a given cas no. from the db info list.

    Args:
        to_fetch_cas_list (list): cas whose info need to be fetched.
        db_info_list (list): db with full info.

    Returns:
        list: [[idx_i, cas_i, [d_i, p_i, h_i]]]
    """
    all_db_cas = db_info_list[1][1]
    all_db_idx = db_info_list[0][1]
    all_db_d = db_info_list[3][1]
    all_db_p = db_info_list[4][1]
    all_db_h = db_info_list[5][1]

    idx_cas_hsp_list = []


    for i, cas in enumerate(to_fetch_cas_list):

        for j, db_cas in enumerate(all_db_cas):

            fetch_all_info = []

            if db_cas == cas:

                fetch_all_info = [all_db_idx[j], all_db_cas[j], [all_db_d[j], all_db_p[j], all_db_h[j]]]
                
                idx_cas_hsp_list.append(fetch_all_info)
        
    return idx_cas_hsp_list


def fetch_sub_hsp(idx_cas_hsp_list: list, to_fetch_opt: str) -> list:
    """return sub-hsp of idx, cas from idx_cas_hsp list.

    Args:
        idx_cas_hsp_list (list): [[idx_i, cas_i, [d_i, p_i, h_i]]].
        to_fetch_opt (str): d, p, h, idx or cas.

    Returns:
        list: [[cas i, required data i]]
    """
    sub_hsp_list = []

    for idx_cas_hsp in idx_cas_hsp_list:

        all_hsp = idx_cas_hsp[2] # first attach cas

        if to_fetch_opt == 'd':

            d = all_hsp[0]
            sub_hsp_list.append(d)
        
        elif to_fetch_opt == 'p':

            p = all_hsp[1]
            sub_hsp_list.append(p)
        
        elif to_fetch_opt == 'h':
            
            h = all_hsp[2]
            sub_hsp_list.append(h)
        
        elif to_fetch_opt == 'cas':

            cas = idx_cas_hsp[1]
            sub_hsp_list.append(cas)
        
        elif to_fetch_opt == 'idx':

            idx = idx_cas_hsp[0]
            sub_hsp_list.append(idx)
    
    return sub_hsp_list




            







