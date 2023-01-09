import solv_pred_io as sp_io
import solv_pred_fetch_info as sp_ftch_info

def ctn_adv_filt():
    """
    check if the user wants to continue the advanced filtration.
    """

    print("Continue advanced filtration? \n")
    usr_ctn_adv_filt_idx = sp_io.continue_check()

    return usr_ctn_adv_filt_idx

def adv_filt(sucs_calc_result, filt_opt = ['misc', 'bp']):
    pass




def sucs_result_expand(vld_log_list, db_info_list):
    """
    expand the sucs results from calculation log
    """
    pass

    fmt_log_list = []

    for each_comb in vld_log_list:

        cas_comb_list = each_comb['cas']
        name_comb_list = sp_ftch_info.fetch_name_from_cas_list(cas_comb_list, db_info_list)
        idx_comb_list = sp_ftch_info.fetch_idx_from_cas_list(cas_comb_list, db_info_list)

    
