"""
solv_pred_gen_cand includes a simple ui for user to determine how to select the solvent candidates
"""

import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io
import solv_pred_reg_txt as sp_rtxt
import json


def generate_candidate_list(default_solv_cand_js: json) -> list:
    """Return a user-generated solvent candidate list. Ask users to determine whether they want to use default option or manually edit the list. The default can be viewed at the first stage. It is recommended to use default list then edit it later.

    Args:
        default_solv_cand_js (json): default candidate list in js
    
    Returns:
        list: user-generated list

    """
    print("=========================\nStep 1: Generate solvent candidate list: \n You can select to use the default list (recommend) or manually input the CAS No. for each solvent.\n")

    # separately prepare cas and name list of solvent candidates by iterating through default_solv_cand_js
    
    default_solv_candidate_js = default_solv_cand_js
    default_solv_candidate_cas_list = []
    default_solv_candidate_name_list = []

    for i, entry in enumerate(default_solv_candidate_js):

        default_solv_candidate_cas_list.append(entry['CAS']) # cas info
        default_solv_candidate_name_list.append(entry['Solvent']) # name info

    # start user interaction
    
    to_continue_gen_cand_lst = True

    while to_continue_gen_cand_lst:

        valid_how_to_select_candidate_list = ['1', '2', 'default', 'manual', 'quit', 'd', 'm', 'v', 'q'] # valid possible user input
        
        candidate_cas_list = []

        how_to_select_candidate = sp_rtxt.rm_spc(str(input("Please select the method to construct solvent candidate list: \n [d] - default (recommend - the default list can still be edited in the following steps) \n [m] - manual \n [v] - visualise default solvent list \n [q] - quit \n" ))).lower() # ask user to select from the following options and regulate the input by removing space and lowering letters

        if not sp_vld_chk.is_option_valid(valid_how_to_select_candidate_list, how_to_select_candidate):

            sp_vld_chk.invalid_input() # in the case when user input an unexpected value or symbol, continue the loop and ask the user to enter the valid option

        elif how_to_select_candidate in ['1', 'default', 'd']:

            candidate_cas_list = default_solv_candidate_cas_list # apply default candidate list
            print('You have selected to use the default solvent candidate list.')
            to_continue_gen_cand_lst = False # break the ui loop


        elif how_to_select_candidate in ['2', 'manual', 'm']:
            
            print("Please submit CAS No. of solvents to be considered as candidates. Add one solvent at one time. Press [enter] to continue.")
            usr_solv_candidate_cas_list = sp_io.input_cas() # ask user to input cas manually
            candidate_cas_list = usr_solv_candidate_cas_list # collect user personalised cas list
            to_continue_gen_cand_lst = False
            #print(usr_solv_candidate_cas_list)
        
        elif how_to_select_candidate in ['v']:

            print('The default solvent candidates include the following solvents: \n')

            for cddt in default_solv_cand_js:

                print(cddt) # iterate through the default candidate list and print to user for a view

        elif how_to_select_candidate in ['q', 'quit']:

            print('Confirm to quit?')

            to_finish_sel_cand = sp_vld_chk.finish_check()

            if to_finish_sel_cand != True:

                exit()

    
    print('Solvent candidate list has been generated successfully.')

    return candidate_cas_list
    