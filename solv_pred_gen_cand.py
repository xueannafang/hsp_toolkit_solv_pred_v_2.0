import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io
import solv_pred_reg_txt as sp_rtxt


def generate_candidate_list(default_solv_cand_js):
    """
    Generate solvent candidate list. Ask users to determine whether they want to use default option or manually edit the list.
    """
    print("=========================\nStep 1: Generate solvent candidate list: \n You can select to use the default list (recommend) or manually input the CAS No. \n")

    default_solv_candidate_js = default_solv_cand_js
    default_solv_candidate_cas_list = []
    default_solv_candidate_name_list = []

    for i, entry in enumerate(default_solv_candidate_js):
        default_solv_candidate_cas_list.append(entry['CAS'])
        default_solv_candidate_name_list.append(entry['Solvent'])

    to_continue_gen_cand_lst = True

    while to_continue_gen_cand_lst:

        valid_how_to_select_candidate_list = ['1', '2', 'default', 'manual', 'quit', 'd', 'm', 'v', 'q']
        candidate_cas_list = []

        how_to_select_candidate = sp_rtxt.rm_spc(str(input("Please select the method to construct solvent candidate list: \n [1] - default (recommend - the default list can still be edited in the following steps) \n [2] - manual \n [v] - visualise default solvent list \n [q] - quit \n" ))).lower()

        if not sp_vld_chk.is_option_valid(valid_how_to_select_candidate_list, how_to_select_candidate):
            sp_vld_chk.invalid_input()

        elif how_to_select_candidate in ['1', 'default', 'd']:
            candidate_cas_list = default_solv_candidate_cas_list
            print('You have selected to use the default solvent candidate list.')
            to_continue_gen_cand_lst = False

        elif how_to_select_candidate in ['2', 'manual', 'm']:
            print("Please submit CAS No. of solvents to be considered as candidates. Add one solvent at one time. Press [enter] to continue.")
            usr_solv_candidate_cas_list = sp_io.input_cas()
            candidate_cas_list = usr_solv_candidate_cas_list
            to_continue_gen_cand_lst = False
            #print(usr_solv_candidate_cas_list)
        
        elif how_to_select_candidate in ['v']:
            print('The default solvent candidates include the following solvents: \n')
            for cddt in default_solv_cand_js:
                print(cddt)

        elif how_to_select_candidate in ['q', 'quit']:
            print('Confirm to quit?')
            to_finish_sel_cand = sp_vld_chk.finish_check()
            if to_finish_sel_cand != True:
                exit()
                
    #print('You have selected the following solvents as candidates: ')
    #print(candidate_cas_list)
    
    print('Solvent candidate list has been generated successfully.')
    return candidate_cas_list
    