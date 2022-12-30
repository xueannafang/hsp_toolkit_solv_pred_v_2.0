import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io


def generate_candidate_list(default_solv_cand_js):
    """
    Generate solvent candidate list. Ask users to determine whether they want to use default option or manually edit the list.
    """
    print("Step 1. Generate solvent candidate list: \n You can select to use the default list [1] or manually input the CAS No. [2] \n Press [v] to check the default candidate list. \n Press [q] to quit. \n")

    default_solv_candidate_js = default_solv_cand_js
    default_solv_candidate_cas_list = []
    default_solv_candidate_name_list = []

    for i, entry in enumerate(default_solv_candidate_js):
        default_solv_candidate_cas_list.append(entry['CAS'])
        default_solv_candidate_name_list.append(entry['Solvent'])

    to_continue = True

    while to_continue:

        valid_how_to_select_candidate_list = ['1', '2', 'default', 'manual', 'quit', 'd', 'm', 'v', 'q']
        candidate_cas_list = []

        how_to_select_candidate = str(input("Please select the method to construct solvent candidate list: \n [1] - default \n [2] - manual \n [v] - visualise default solvent list \n [q] - quit \n" )).lower()

        if not sp_vld_chk.is_option_valid(valid_how_to_select_candidate_list, how_to_select_candidate):
            sp_vld_chk.invalid_input()

        elif how_to_select_candidate in ['1', 'default', 'd']:
            candidate_cas_list = default_solv_candidate_cas_list
            print('You have selected to use the default solvent candidate list.')
            to_continue = False

        elif how_to_select_candidate in ['2', 'manual', 'm']:
            print("Please submit CAS No. of solvents to be considered as candidates. Add one solvent at one time. Press [enter] to continue.")
            usr_solv_candidate_cas_list = sp_io.input_cas()
            candidate_cas_list = usr_solv_candidate_cas_list
            to_continue = False
            #print(usr_solv_candidate_cas_list)
        
        elif how_to_select_candidate in ['v']:
            print('The default solvent candidates include the following solvents: \n')
            for cddt in default_solv_cand_js:
                print(cddt)

        elif how_to_select_candidate in ['q', 'quit']:
            if len(candidate_cas_list) >= 1:
                to_continue = False
            else:
                print('You have not selected any solvent candidate. \n [ctrl + c] to force quit.')

    #print('You have selected the following solvents as candidates: ')
    #print(candidate_cas_list)
    
    print('Solvent candidate list has been generated successfully.')
    return candidate_cas_list
    