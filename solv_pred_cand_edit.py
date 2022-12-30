import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io

def remove_cas():
    """
    ask user to remove any unwanted solvent cas from the candidate list
    """
    to_continue = True
    cas_to_remove = []

    while to_continue:

        remove_check = input("Do you want to remove any solvent? [y/n] ? ").lower()

        if remove_check in ['y', 'yes']:
            cas_to_remove_usr = sp_io.input_cas()

        elif remove_check in ['n', 'no']:
            cas_to_remove_usr = []
            to_continue = False

        else:
            sp_vld_chk.invalid_input()
        
        cas_to_remove += cas_to_remove_usr

    if cas_to_remove:
        print('The following solvents will be removed: ')
        print(cas_to_remove)


def is_cas_in(input_cas_list, available_cas_list):

    not_in_list = []

    for input_cas in input_cas_list:
        if input_cas not in available_cas_list:
            not_in_list.append(input_cas)

    return not_in_list
            
    pass