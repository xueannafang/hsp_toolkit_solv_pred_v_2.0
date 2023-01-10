import solv_pred_io as sp_io
import solv_pred_fetch_info as sp_ftch_info

db_readable_opt_dict = {

        'miscibility' : 'ims_idx',
        'bp' : 'bp',
        'idx' : 'No.',
        'cas' : 'CAS',
        'solvent' : 'Name',
        'mw' : 'Mole_vol',
        'viscosity' : 'viscosity',
        'temperature of viscosity' : 'vis_temp',
        'heat_of_evaporation' : 'heat_of_vap',
        'temperature_of_heat_of_evaporation' : 'hov_temp',
        'structure' : 'SMILES'

    }

def ctn_adv_filt():
    """
    check if the user wants to continue the advanced filtration.
    """

    print("Continue advanced filtration? \n")
    usr_ctn_adv_filt_idx = sp_io.continue_check()

    return usr_ctn_adv_filt_idx


def gen_filt_opt(filt_opt):
    """
    convert filt_opt to key name in db_info_dict
    in this version the filt_opt is ['miscibility', 'bp']
    needs to be converted to 'ims_idx' and 'bp'
    """

    db_dict_readable_filt_opt_list = []

    for opt in filt_opt:
        db_dict_readable_opt = db_readable_opt_dict[str(opt)]
        db_dict_readable_filt_opt_list.append(db_dict_readable_opt)
    
    return db_dict_readable_filt_opt_list


def adv_filt(vld_log_list, filt_opt, db_info_dict, target_temp):
    """
    filt_opt is a list of solvent properties involved in the database
    in this version (v2.0) filt_opt is miscibility and bp - will be converted to ims_idx list and bp list

    a mis_chk and bp_chk bool value will be included for each combinations

    for bp filt part:
        solvents with bp belowing the target temp will trigger a warning message and return a False value for bp_chk
    """
    db_opt_list = gen_filt_opt(filt_opt)

    chk_name_list = []

    for db_opt in db_opt_list:
        chk_name = str(db_opt) + '_chk'
        chk_name_list.append(chk_name)
    
    # chk_name_list = ['ims_idx_chk', 'bp_chk']

    expand_info_list = sucs_result_expand(vld_log_list, db_info_dict, db_opt_list)

    # sp_io.calc_log_list2txt(expand_info_list, '_exp_info_')





def sucs_result_expand(vld_log_list, db_info_dict, to_fetch_property):
    """
    expand the sucs results from calculation log
    to_fetch_property is a list matching the filt_opt in adv_filt
    """

    expand_vld_info_dict = []

    for each_comb in vld_log_list:

        cas_comb_list = each_comb['cas_comb']
        vld_info_dict = sp_ftch_info.fetch_info_from_cas_list(cas_comb_list, to_fetch_property, db_info_dict) # need to fetch ['No.', 'Name', 'bp', 'ims_idx']
        expand_vld_info_dict.append(vld_info_dict)
    
    return expand_vld_info_dict



    
