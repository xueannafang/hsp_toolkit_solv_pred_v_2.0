#key func: fetch required information from the database (json)

def fetch_name(cas, db_json):

    for i, entry in enumerate(db_json):
        if cas == entry['CAS']:
            solv_name = entry['Name']
            
    return solv_name


def fetch_idx_cas_hsp(to_fetch_cas_list, db_info_list):
    """
    fetch current hsp of a given cas no. from the db info list
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
                #print(fetch_all_info)
                idx_cas_hsp_list.append(fetch_all_info)
        
        #print(idx_cas_hsp_list)
    
    return idx_cas_hsp_list


def fetch_sub_hsp(idx_cas_hsp_list, to_fetch_opt):
    """
    fetch sub-hsp from idx_cas_hsp list
    to_fetch_opt = d, p, h, cas, idx
    """
    sub_hsp_list = []

    for idx_cas_hsp in idx_cas_hsp_list:
        all_hsp = idx_cas_hsp[2]

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




            






