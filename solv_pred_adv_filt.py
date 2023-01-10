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

    expand_info_list = sucs_result_expand(vld_log_list, db_info_dict, db_opt_list)

    # sp_io.calc_log_list2txt(expand_info_list, '_exp_info_')

    # for comb_dict_list in expand_info_list:
    #     pass

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
                each_comb_ims_chk = sp_vld_chk.ims_chk(each_comb)
                exp_info_ims_chk_list.append(each_comb_ims_chk)
            
            updt_filt_list = exp_info_ims_chk_list
    
    adv_all_log_txt_path = sp_io.calc_log_list2txt(updt_filt_list, '_adv_all_')
    # sp_io.calc_log_list2js(updt_filt_list, '_adv_')
    

    
    vld_solv_comb_adv_list = []
    
    for i, solv_comb in enumerate(updt_filt_list):

        comb_vld = 1

        for solv_dict in solv_comb:

            if False in solv_dict.values():
                comb_vld = 0
        
        if comb_vld == 1:

            vld_solv_comb_adv_list.append(solv_comb)
    
    
    if len(vld_solv_comb_adv_list) == 0:

        print('No results available')
        print('Please check ' + str(adv_all_log_txt_path) + ' for full advanced calculation information.\n')
        # run failed adv log
    
    else:

        adv_filt_log_txt_path = sp_io.calc_log_list2txt(vld_solv_comb_adv_list, '_adv_filt_')
        # sp_io.calc_log_list2js(updt_filt_list, '_adv_')
        # print('Please check ' + str(adv_filt_log_txt_path) + ' for full advanced calculation information.\n')

        # expand and export final log - need to visit back to the vld_log_list to extract the basic info

    return adv_filt_log_txt_path
        

def sucs_result_expand(vld_log_list, db_info_dict, to_fetch_property):
    """
    expand the sucs results from calculation log
    to_fetch_property is a list matching the filt_opt in adv_filt
    """

    expand_vld_info_dict = []

    for each_comb in vld_log_list:

        cas_comb_list = each_comb['cas_comb']

        each_comb_idx = each_comb['idx']
        # each_comb_conc = each_comb['conc']
        # each_comb_err = each_comb['err']
        # each_comb_calc_hsp = each_comb['calc_hsp']

        vld_info_dict = sp_ftch_info.fetch_info_from_cas_list(cas_comb_list, to_fetch_property, db_info_dict) # need to fetch ['No.', 'Name', 'bp', 'ims_idx']

        for solv_dict in vld_info_dict:
            solv_dict['ori_idx'] = each_comb_idx

        expand_vld_info_dict.append(vld_info_dict)
    
    return expand_vld_info_dict



    
