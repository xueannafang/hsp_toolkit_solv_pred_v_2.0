import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io


def generate_candidate_list(default_solv_cand_js):
    """
    Generate solvent candidate list. Ask users to determine whether they want to use default option or manually edit the list.
    """
    print("Generate solvent candidate list: \n You can select to use the default list [1] or manually input the CAS No. [2] \n The default candidate list include the following solvents: ")

    default_solv_candidate_js = default_solv_cand_js
    default_solv_candidate_cas_list = []
    default_solv_candidate_name_list = []

    for i, entry in enumerate(default_solv_candidate_js):
        default_solv_candidate_cas_list.append(entry['CAS'])
        default_solv_candidate_name_list.append(entry['Solvent'])
        
    print(default_solv_candidate_js)

    to_continue = True

    while to_continue:

        valid_how_to_select_candidate_list = ['1', '2', 'default', 'manual', 'd', 'm']
        candidate_cas_list = []
        how_to_select_candidate = str(input("Please select the method to construct solvent candidate list. [1-default/2-manual]: " )).lower()

        if not sp_vld_chk.is_option_valid(valid_how_to_select_candidate_list, how_to_select_candidate):
            sp_vld_chk.invalid_input()

        elif how_to_select_candidate in ['1', 'default', 'd']:
            candidate_cas_list = default_solv_candidate_cas_list
            to_continue = False

        elif how_to_select_candidate in ['2', 'manual', 'm']:
            print("Please submit CAS No. of solvents to be considered as candidates. Add one solvent at one time. Press enter to finish.")
            usr_solv_candidate_cas_list = sp_io.input_cas()
            candidate_cas_list = usr_solv_candidate_cas_list
            to_continue = False
            #print(usr_solv_candidate_cas_list)

    print('You have selected the following solvents as candidates: ')
    print(candidate_cas_list)
    
    