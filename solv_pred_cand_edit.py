import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io

def remove_cas():
    """
    ask user to remove any unwanted solvent cas from the candidate list
    """
    to_continue = True
    cas_to_remove = []

    while to_continue:

        print("Do you want to remove any solvent? \n")
        remove_check = sp_io.continue_check()

        if remove_check == 1:
            cas_to_remove_usr = sp_io.input_cas()

        elif remove_check == 0:
            cas_to_remove_usr = []
            #to_continue = False

        else:
            sp_vld_chk.invalid_input()
        
        cas_to_remove += cas_to_remove_usr

    
        if len(cas_to_remove) != 0:
            print('The following solvents will be removed: ')
            print(cas_to_remove)
        
        else:
            print('No solvent will be removed.')
        
        print('Continue? ')

        remove_finish = sp_io.continue_check()

        if remove_finish == 1:
            to_continue = False

        elif remove_finish == 0:
            pass

        else:
            sp_vld_chk.invalid_input()
    
    return cas_to_remove

    

        

