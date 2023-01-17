"""
SolvPred_v2.0
Last update: 17/01/2023
"""

import solv_pred_io as sp_io
import solv_pred_gen_cand as sp_gen_cand
import solv_pred_cand_edit as sp_cand_ed
import solv_pred_valid_check as sp_vld_chk
import solv_pred_fetch_info as sp_ftch_info
import solv_pred_prmtr as sp_prmtr
import solv_pred_calc as sp_clc
import solv_pred_adv_filt as sp_adv_filt


def solv_pred_main(db: str = 'db_solv_pred_v2.json', default_candidate: str = 'default_solv_candidate.json'):
    """run all functions of SolvPred_2.0
    
    Args:
        db (str): _database file name under current working directory_
        default_candidate (str): _default candidate json file name under current working directory_
    
    Returns:
        some logs and jsons... tbc

    """

    # Step 0: Load database and default candidate list.

    sp_io.version_info() # print current version info and time info for running the test.

    print('Loading database and default candidate list...')
    
    db_js = sp_io.load_js(db) # load solvent database
    default_solv_candidate_js = sp_io.load_js(default_candidate) # load default solvent candidate list

    db_full_info_list = sp_io.db_init(db_js) # save all the values for each key into a list of list

    # to check current db_info_list: sp_io.calc_log_list2txt(db_full_info_list, '_db_full_info_list')

    db_cas_list = db_full_info_list[1][1] # extract all the cas in db

    if db_js and default_solv_candidate_js:
        print('Done. \n')
        print('Please follow the instruction to continue: ')
    
    
    #

    # Step_1: Generate candidate list

    # In this step, user can choose to use default candidate list and then remove unwanted solvents or add more (recommended).

    # Alternatively (less recommended), user can create the candidate list by entering the cas no. of desired solvents.

    # For the "manual" method, users need to bear in mind that the minimum number of solvents must larger than 2 and there will be more likely to fail the prediction if the region connected by the selected solvents does not cover the target hsp, though SolvPred v2.0 has included the filteration of this case.

    #
    
    usr_gen_cand_list = sp_gen_cand.generate_candidate_list(default_solv_candidate_js) # return candidate list

    usr_gen_cas_to_remove = sp_cand_ed.remove_cas() # collect a list of cas to be removed, especially when default db is applied

    print('Checking if any solvent is not on the candidate list...')

    after_usr_filt_cand_list = sp_vld_chk.can_be_removed_check(usr_gen_cas_to_remove, usr_gen_cand_list) # check and remove the requested cas from current candidate list

    print('Done. \n Checking if any solvent is not in the database...')

    not_in_db_cas = sp_vld_chk.is_cas_in(after_usr_filt_cand_list, db_cas_list) # collect invalid cas that are not in db

    after_db_filt_cand_list = sp_vld_chk.not_in_db_filt(after_usr_filt_cand_list, not_in_db_cas) # check and remove not_db_cas from current candidate list
    
    print('Done.')
    
    edited_cand_list = sp_cand_ed.edit_cand_list(after_db_filt_cand_list) # confirm the final usr-edited candidate list before submission 

    not_in_db_cas_final = sp_vld_chk.is_cas_in(edited_cand_list, db_cas_list)

    final_db_cas_filt = sp_vld_chk.not_in_db_filt(edited_cand_list, not_in_db_cas_final)

    print('Candidate list has been successfully generated:')

    final_db_name_filt = []

    for cas in final_db_cas_filt:

        matched_name = sp_ftch_info.fetch_name(cas, db_js) # fetch solvent name from db based on cas
        final_db_name_filt.append(matched_name)
    
    print(final_db_name_filt) # print the name of all the candidates


    #
    # Step 2: Specify basic calculation parameters.

    # user need to first specify the temperature - default temperature is 25 degree c.
    # The database will be updated by applying temperature correction for the three HSP.

    # user then need to specify the following parameters:

    # n - maximum number of solvents involved in each combination. default n = 2. recommend to use 2 or 3.

    # tol_err_d, p, h - tolerance of error of the calculated HSP based on the predicted combinations.
    # - Errors higher than these values will be filtered.

    # tol_conc - threshold of lowest acceptable concentration of each solvent component.
    # - Solvents with predicted concentration below this value will be filtered.

    # target_d, p, h - the target HSP to be achieved.
    # - This target must be included in the region connected by all the solvent candidates in the Hansen space.
    # - This version will automatically check if this requirement is met or not.

    #

    print('=========================\n\nStep 2: Specify parameters. \n Please follow the instruction to specify the \n - Maximum number of solvents (n) to be included in each combination (default = 2); \n - Highest acceptable error of HSP (tol_err) of the predicted combination (default = 0.5); \n - Lowest acceptable concentration (tol_conc) of each predicted solvent component (default = 0.01). \n - Target HSP (target D, P, H). \n Temperature (default = 25 degree C). \n')

    temp_updt_db, is_temp_updt, tgt_temp = sp_prmtr.specify_temp(db_full_info_list) # temperature correction based on user request
    
    all_parameters = sp_prmtr.get_parameter(final_db_cas_filt, temp_updt_db)
    print('Parameter selection done.\n')
    #print(all_parameters)

    n = int(all_parameters[0])

    target_hsp_list = all_parameters[1] # in the order of d, p, h
    tol_err_list = all_parameters[2] # in the order of tol_err_d, tol_err_p, tol_err_h
    tol_conc = all_parameters[3]

    cand_cas_for_calc_list = all_parameters[4] # valid candidate cas for next step calculation

    # 
    # Step 3

    # Main calculation cell

    # Iterate through all the combinations of n-nary solvent systems
    # Construct standard HSP matrix based on n-candidate combination
    # Construct target HSP matrix with statistical perturbation
    # Statistical validation - rough filtration - concentration renormalisation - fine filtration
    # 


    ctn_idx, calc_log_js_list, calc_log_js_path = sp_clc.calc_vld_all_c(cand_cas_for_calc_list, temp_updt_db, n, target_hsp_list, tol_err_list, tol_conc)

    vld_result_list = sp_clc.sucs_result_filt(calc_log_js_list) # filter and only keep valid results

    db_info_dict = sp_io.db_info_list2dict(temp_updt_db) # convert db_info_list to a dictionary

    if ctn_idx == 0:

        print('No available results.\n Please check ' + calc_log_js_path + ' for full calculation details.\n')
        print('Please consider to increase the number of candidates or error tolerance.\n ')

        fail_log_txt_path = sp_io.fail_calc_log(tgt_temp, n, target_hsp_list, tol_err_list, tol_conc, cand_cas_for_calc_list, final_db_name_filt, calc_log_js_path) # output failed log txt file log_failed.

        print('Please check ' + fail_log_txt_path + ' for calculation log. \n')

        # add one more final log summarising other calculation details

        exit()
    
    else:

        sucs_log_path = sp_io.sucs_calc_log(tgt_temp, n, target_hsp_list, tol_err_list, tol_conc, cand_cas_for_calc_list, final_db_name_filt, calc_log_js_path, vld_result_list, db_info_dict) # output successful log txt file log_success.
    
    # 
    # Step 4
    
    # advanced filtration

    # optional filtrations based on 
    # miscibility check
    # bp check

    # first save a log without optional filtration step.

    # let user determine if they want to do final filtration.

    # filter all the false results, in the remaining terms

    # fetch the original idx
    
    # - if the temperarture has been modified before:
    
    # this step will pop up a warning saying these check are based on room temperature. 

    # - bp check will highlight some solvent whose bp is below the required temperature.

    # - if any value is -1 or None, label it as data unavailbale, manual check required.

    # -miscibility check: this version (2.0) is only based on data available on pubchem.
    
    # -Note that the limitation of miscibility check include
    
    # 1) many solvents do not have experimentally suggested immiscible solvents, or the description is ambiguous, e.g., very poor, poor, etc. Solvents that was mentioned with those "poor" solubility features are all classified as "immscible" at r.t.
    
    # 2) The term "immiscible" itself can be arguable. This property is ideally to be quantified by a continuous solubility variable, but at this stage, this data is very limited.

    # 3) Some data do not include test temperature.


    # 

    ctn_idx = 1

    print('=========================\nStep 4: Advanced filtration (optional) \n This step will further include the consideration of solvent properties according to the condition set up. \n In this version, miscibility and boiling point will be evaluated. \n Data are based on PubChem. \n Please note, there could be some limitation of this function due to data availability. Check README for more discussion. \n')

    ctn_idx = sp_adv_filt.ctn_adv_filt() # check if user wants to process advanced filteration or not.

    adv_filt_opt_list = ['idx', 'solvent', 'miscibility', 'bp'] # items except idx and solvent are advanced options to be filtered and checked.

    if ctn_idx == 0:
        
        # user does not want to do the filtration.

        print('Please check ' + sucs_log_path + ' for calculation log.')

        # file name and path of the sucs log
        exit()
    
    else:

        basic_input_prmtr_dict = {

        'Target D /MPa^(1/2)' : target_hsp_list[0],
        'Target P /MPa^(1/2)' : target_hsp_list[1],
        'Target H /MPa^(1/2)' : target_hsp_list[2],
        'Temperature /degree c' : tgt_temp,
        'Number of candidates in each combination (n)' : n,
        'Tolerance of error for D /MPa^(1/2)' : tol_err_list[0],
        'Tolerance of error for P /MPa^(1/2)' : tol_err_list[1],
        'Tolerance of error for H /MPa^(1/2)' : tol_err_list[2],
        'Lowest concentration limit' : tol_conc,
        'Candidate cas' : cand_cas_for_calc_list,
        'Candidate solvents' : final_db_name_filt,
    
        } # Full input parameters into a dict. 'Full calculation log path' : calc_log_js_path will not be included in the sucs_adv_filt_log

                    
        sp_adv_filt.adv_filt(vld_result_list, adv_filt_opt_list, db_info_dict, tgt_temp, basic_input_prmtr_dict) # advanced filtration




solv_pred_main()