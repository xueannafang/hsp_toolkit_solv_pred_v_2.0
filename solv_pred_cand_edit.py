"""
solv_pred_cand_edit inlcudes user iteractive functions to edit current candidate cas list
"""

import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io
import solv_pred_reg_txt as sp_rtxt

def remove_cas() -> list:
    """return a user-specified cas list to be removed.
    
    Returns:
        list: user-specified cas to be removed.

    """
    to_continue_rm_cas = True

    cas_to_remove = []

    # generate cas_to_remove list

    while to_continue_rm_cas:

        print("Do you want to remove any solvent? \n")
        remove_check = sp_io.continue_check()

        if remove_check == 1:

            cas_to_remove_usr = sp_io.input_cas()

        elif remove_check == 0:

            cas_to_remove_usr = []
            
            print('Continue? ')
            to_continue_rm_cas = sp_vld_chk.finish_check()

        else:

            cas_to_remove_usr = []
            sp_vld_chk.invalid_input()
        
        cas_to_remove += cas_to_remove_usr

    # check if the cas_to_remove list is empty

    if len(cas_to_remove) != 0:

        print('The following solvents will be removed: ')
        print(cas_to_remove)
    
    else:

        print('No solvent will be removed.')
    
    return cas_to_remove


def add_cas() -> list:
    """Return list of additional user-specified candidate cas before submission.

    Returns:
        list: additional cas to be included.
    """

    to_continue_add_cas = True

    cas_to_add = []

    while to_continue_add_cas:

        print("Do you want to add any solvent? \n")
        add_check = sp_io.continue_check()

        if add_check == 1:

            cas_to_add_usr = sp_io.input_cas()
            to_continue_add_cas = False

        elif add_check == 0:

            cas_to_add_usr = []
            print('Continue?')

            to_continue_add_cas = sp_vld_chk.finish_check()

        else:
            sp_vld_chk.invalid_input()
        
        cas_to_add += cas_to_add_usr

    
    if len(cas_to_add) != 0:

        print('The following solvents will be added: ')
        print(cas_to_add)
    
    else:
        
        print('No solvent will be added.')
    
    return cas_to_add


def edit_cand_cas_option(current_cand_cas_list: list, operation: str) -> list:
    """Return confirmed candidate list before final submission.

    Args:
        current_cand_cas_list (list): current candidates cas
        operation (str): 'a' - add, 'rm' - remove, 'q' - quit, 'n' - not continue, 'v' - view current list

    Returns:
        list: edited candidate cas
    """

    to_continue_ed_cas_opt = True

    crt_cand_cas_list = sp_vld_chk.rm_repeat(current_cand_cas_list)

    while to_continue_ed_cas_opt:
        
        if operation == 'n': # submit

            to_continue_ed_cas_opt = False

        elif operation == 'a': # add

            cas_to_add_list = add_cas()

            crt_cand_cas_list += cas_to_add_list
            crt_cand_cas_list = sp_vld_chk.rm_repeat(crt_cand_cas_list)

            print('Continue?')
            to_continue_ed_cas_opt = sp_vld_chk.finish_check()

            print('Current candidate list: ')
            print(crt_cand_cas_list)
        
        elif operation == 'rm': # remove
            
            cas_to_rm_list = remove_cas()

            crt_cand_cas_list = sp_vld_chk.rm_repeat(crt_cand_cas_list)

            after_filt = sp_vld_chk.can_be_removed_check(cas_to_rm_list, crt_cand_cas_list)

            crt_cand_cas_list = sp_vld_chk.rm_repeat(after_filt)

            if len(crt_cand_cas_list) == 0:

                print('Warning: No solvent candidate has been selected. Please add solvents.') # if the candidate has been emptied.

            print('Continue?')
            to_continue_ed_cas_opt = sp_vld_chk.finish_check()
        
        elif operation == 'v': # view current

            print('Current candidate list:')
            print(crt_cand_cas_list)

            print('Continue?')
            to_continue_ed_cas_opt = sp_vld_chk.finish_check()
        
        elif operation == 'q': # quit

            print('Confirm to quit SolvPred?')
            to_finish_ed_cand = sp_vld_chk.finish_check()

            if to_finish_ed_cand is True:

                exit()
        
        elif operation == 's': # submit

            print('Continue?')
            to_continue_ed_cas_opt = sp_vld_chk.finish_check()
        
    return crt_cand_cas_list

def edit_cand_list(current_cand_cas_list: list) -> list:
    """return user updated candidate list

    Args:
        current_cand_cas_list (list): current candidate list

    Returns:
        list: user-updated candidated list
    """

    to_continue_ed_cas_lst = True

    final_cand_list = sp_vld_chk.rm_repeat(current_cand_cas_list) # remove repeated cas entries from the candidate list

    while to_continue_ed_cas_lst:

        print('Submit?')
        submit_check = sp_io.continue_check() # submission check

        if submit_check == 1: # submit

            print('The following solvents will be considered as candidates: ')
            print(final_cand_list)

            to_continue_ed_cas_lst = False
            
        elif submit_check == 0:

            valid_how_to_edit_cand_list = ['a', 'rm', 'v', 's', 'q', 'add', 'remove', 'visualise', 'submit', 'quit'] # valid options to edit current candidate list

            how_to_edit_cand = sp_rtxt.rm_spc(str(input("Please select one of the following options: \n[a] - add CAS \n[rm] - remove CAS \n[v] - visualise current candidate list\n[s] - submit\n[q] - quit\n" ))).lower() # ask users how do they want to modify the current candidate list

            if not sp_vld_chk.is_option_valid(valid_how_to_edit_cand_list, how_to_edit_cand):

                sp_vld_chk.invalid_input()
                edit_operation = 'n'
            
            elif how_to_edit_cand in ['a', 'add']:

                edit_operation = 'a'
            
            elif how_to_edit_cand in ['rm', 'remove']:

                edit_operation = 'rm'
            
            elif how_to_edit_cand in ['v', 'visualise']:

                edit_operation = 'v'
            
            elif how_to_edit_cand in ['s', 'submit']:

                edit_operation = 's'
            
            elif how_to_edit_cand in ['q', 'quit']:

                edit_operation = 'q'

            final_cand_list = edit_cand_cas_option(current_cand_cas_list, edit_operation)

        else:

            sp_vld_chk.invalid_input()
    
    return final_cand_list






