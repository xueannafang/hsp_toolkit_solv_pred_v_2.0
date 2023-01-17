"""
solv_pred_adv_filt contains functions involved in advanced filtration step.
"""

import solv_pred_io as sp_io
import solv_pred_fetch_info as sp_ftch_info
import solv_pred_valid_check as sp_vld_chk

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

def ctn_adv_filt() -> int:
    """return continue idx reflecting whether the user wants to continue the advanced filtration.

    Returns:
        int: 1 for to continue. 0 for not.
    """

    print("Continue advanced filtration? \n")
    usr_ctn_adv_filt_idx = sp_io.continue_check()

    return usr_ctn_adv_filt_idx


def gen_filt_opt(filt_opt: list) -> list:
    """return name that fits the db dict based on the filt_opt list.  

    Args:
        filt_opt (list): in this version it is ['miscibility', 'bp'] in addition to standard terms ['idx', 'solvent'] - needs to be converted to 'ims_idx' and 'bp'.

    Returns:
        list: corresponding keys readable by the db dict.
    """

    db_dict_readable_filt_opt_list = []

    for opt in filt_opt:

        db_dict_readable_opt = db_readable_opt_dict[str(opt)]
        db_dict_readable_filt_opt_list.append(db_dict_readable_opt)
    
    return db_dict_readable_filt_opt_list


def adv_filt(vld_log_list: list, filt_opt: list, db_info_dict: dict, target_temp: float, bsc_ip_info_dict: dict):
    """return advanced filtration based on filt_opt (in this version bp and miscibility is checked). a mis_chk and bp_chk bool value will be included for each combinations.
    solvents with bp belowing the target temp will return a False value for bp_chk.

    Args:
        vld_log_list (list): log of valid calculation info.
        filt_opt (list): options of advanced filtrations to be applied.
        db_info_dict (dict): dict of full db info.
        target_temp (float): target temperature as a reference of bp filtration.
        bsc_ip_info_dict (dict): basic input parameters.
    """
    
    db_opt_list = gen_filt_opt(filt_opt) # convert into db readable options

    expand_info_list = sucs_result_expand(vld_log_list, db_info_dict, db_opt_list) # expand current valid log list with requested properties

    updt_filt_list = expand_info_list

    for opt in db_opt_list:

        if opt == 'bp':

            exp_info_bp_chk_list = []
            
            for each_comb in updt_filt_list:

                each_comb_bp_chk = sp_vld_chk.bp_chk(each_comb, target_temp)
                exp_info_bp_chk_list.append(each_comb_bp_chk)
            
            updt_filt_list = exp_info_bp_chk_list
        
        elif opt == 'ims_idx':

            exp_info_ims_chk_list = []

            for each_comb in updt_filt_list:

                each_comb_ims_chk = sp_vld_chk.ims_chk(each_comb) # check miscibility issue of each combination
                exp_info_ims_chk_list.append(each_comb_ims_chk)
            
            updt_filt_list = exp_info_ims_chk_list
    
    adv_all_log_txt_path = sp_io.calc_log_list2txt(updt_filt_list, '_adv_all_') # full log of advanced filtration

    # sp_io.calc_log_list2js(updt_filt_list, '_adv_')

    adv_all_js_path = sp_io.adv_filt_exp_list2json(updt_filt_list, 'adv_filt_all_')[0] # save full log of advanced filtration results as json file
    
    
    vld_solv_comb_adv_list = []
    
    # filter invalid results from the expanded list that includes validity info

    for i, solv_comb in enumerate(updt_filt_list):

        comb_vld = 1 # idx of whether any entry is invalid

        for solv_dict in solv_comb:

            if False in solv_dict.values():

                comb_vld = 0 # one or more property check has returned invalid, further filtration required
        
        if comb_vld == 1:

            vld_solv_comb_adv_list.append(solv_comb) # no property is invalid, directly append the result to output list
    
    
    if len(vld_solv_comb_adv_list) == 0:

        print('No results available')

        adv_filt_fail_log_path = sp_io.adv_filt_fail_log(bsc_ip_info_dict, adv_all_js_path, filt_opt)

        print('Please check ' + str(adv_filt_fail_log_path) + ' for full advanced calculation information.\n')

    
    else:

        adv_filt_log_txt_path = sp_io.calc_log_list2txt(vld_solv_comb_adv_list, '_adv_filt_')
        # sp_io.calc_log_list2js(updt_filt_list, '_adv_')

        adv_filt_exp_list, adv_filt_exp_txt_path = adv_filt_expand(vld_log_list, vld_solv_comb_adv_list) # expand and export final log - need to visit back to the vld_log_list to extract the basic info

        # convert adv_filt_exp_list to json and save as adv_filt_exp_json
        adv_js_path, adv_js_list = sp_io.adv_filt_exp_list2json(adv_filt_exp_list, 'adv_filt_exp_info_')
        
        adv_filt_sucs_log_txt_path = sp_io.adv_filt_sucs_log(adv_filt_exp_list, filt_opt, adv_js_path, adv_all_js_path, bsc_ip_info_dict) # save final log

        print('Please check: \n' + str(adv_filt_sucs_log_txt_path) + ' for calculation log.')


def adv_filt_expand(vld_log_list: list, vld_solv_comb_adv_list: list) -> tuple[list, str]:
    """return [info_expanded list, path of expanded info log]. From the adv_filtered list, using ori_idx to extract conc, err, calc_hsp info from the vld_log_list.

    Args:
        vld_log_list (list): full valid calculation log before adv filtration.
        vld_solv_comb_adv_list (list): valid combination based on adv filtration.

    Returns:
        tuple[list, str]: [expanded info after adv filtration, path of adv_exp log].
    """
    

    adv_filt_expand_list = []

    for solv_comb_adv_filt in vld_solv_comb_adv_list:

        updt_solv_comb_list = []

        for i, solv in enumerate(solv_comb_adv_filt):

            updt_solv_dict = solv

            idx_in_all_vld = solv['ori_idx']

            for solv_comb_all_vld in vld_log_list:

                if solv_comb_all_vld['idx'] == idx_in_all_vld:

                    conc_i = solv_comb_all_vld['conc'][i][0]

                    updt_solv_dict['conc'] = conc_i

                    calc_d = solv_comb_all_vld['calc_hsp'][0][0]

                    calc_p = solv_comb_all_vld['calc_hsp'][1][0]

                    calc_h = solv_comb_all_vld['calc_hsp'][2][0]

                    err_d = solv_comb_all_vld['err'][0][0]

                    err_p = solv_comb_all_vld['err'][1][0]

                    err_h = solv_comb_all_vld['err'][2][0]

                    updt_solv_dict['calc_d'] = calc_d
                    updt_solv_dict['calc_p'] = calc_p
                    updt_solv_dict['calc_h'] = calc_h
                    updt_solv_dict['err_d'] = err_d
                    updt_solv_dict['err_p'] = err_p
                    updt_solv_dict['err_h'] = err_h
        
            updt_solv_comb_list.append(updt_solv_dict) # update solvent comb info
    
        adv_filt_expand_list.append(updt_solv_comb_list) # attach to the expanded list

    
    adv_filt_exp_txt_path = sp_io.calc_log_list2txt(adv_filt_expand_list, '_adv_exp_') # save log
    
    return adv_filt_expand_list, adv_filt_exp_txt_path



def sucs_result_expand(vld_log_list: list, db_info_dict: dict, to_fetch_property: list) -> list:
    """return list of dict involving requested properties expanded from the valid results in calculation log.

    Args:
        vld_log_list (list): [{'idx' : idx_i in all calc details, 'cas_comb' : [cas_1, cas_2, .., cas_n], 'conc' : [[conc_1], [conc_2], ...,  [conc_n], 'err' : [[e_d], [e_p], [e_h], [e_I = 1]], 'calc_hsp' : [[calc_d], [calc_p], [calc_h], [1]], 'quality' : 'Valid', 'validity' : 'True'}]
        db_info_dict (dict): {key_i: all_values of key i in db}
        to_fetch_property (list): keys in db to be fetched.

    Returns:
        list: with attached to_fetch_key : fetched value in the current list.
    """
    

    expand_vld_info_dict = []

    for each_comb in vld_log_list:

        cas_comb_list = each_comb['cas_comb']

        each_comb_idx = each_comb['idx']

        vld_info_dict = sp_ftch_info.fetch_info_from_cas_list(cas_comb_list, to_fetch_property, db_info_dict) #  [{'CAS' : cas_i, 'to_be_fetched_key_j' : value_j}]

        for solv_dict in vld_info_dict:

            solv_dict['ori_idx'] = each_comb_idx # attach idx in the full calc log as ori_idx in the expanded info

        expand_vld_info_dict.append(vld_info_dict)
    
    return expand_vld_info_dict



    
