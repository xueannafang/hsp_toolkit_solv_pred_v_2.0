import solv_pred_io as sp_io

def ctn_adv_filt():
    """
    check if the user wants to continue the advanced filtration.
    """

    print("Continue advanced filtration? \n")
    usr_ctn_adv_filt_idx = sp_io.continue_check()

    return usr_ctn_adv_filt_idx

def adv_filt(sucs_calc_result, filt_opt = ['misc', 'bp']):
    pass

    
