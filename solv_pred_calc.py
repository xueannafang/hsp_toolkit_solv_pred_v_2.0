import numpy as np
from scipy.linalg import pinv
import itertools
import solv_pred_fetch_info as sp_ftch_info
import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io

def mtrx_s_bf_comb(cand_cas_list, db_list):
    """
    construct the standard hsp matrix before combination
    """
    total_cand = len(cand_cas_list)
    s_bf_comb = np.ones((4, total_cand))
    cand_all_info = sp_ftch_info.fetch_idx_cas_hsp(cand_cas_list, db_list)
    all_db_idx_list = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'idx')
    all_db_cas_list = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'cas')
    all_d = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'd')
    all_p = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'p')
    all_h = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'h')
    s_bf_comb[0] = all_d
    s_bf_comb[1] = all_p
    s_bf_comb[2] = all_h

    return [s_bf_comb, [all_db_idx_list, all_db_cas_list]]

def gen_idx(list_length):
    """
    convert a list with a given length into a list of index
    """
    i = 0
    n_idx_list = []
    for i in range(0, list_length):
        n_idx_list.append(i)

    return n_idx_list


def comb_idx(len_list, n):

    idx_list = gen_idx(len_list)

    all_comb_idx_list = []

    for comb in itertools.combinations(idx_list, n):
        all_comb_idx_list.append(list(comb))
    
    return all_comb_idx_list

def itrt_cand(cand_cas_list, db_list, n):

    mat_s_bf_comb = mtrx_s_bf_comb(cand_cas_list, db_list)[0]
    mat_s_bf_comb_arr_t = np.array(mat_s_bf_comb).transpose() # get ready to store column info

    db_idx_bf_comb_list = mtrx_s_bf_comb(cand_cas_list, db_list)[1][0]
    db_cas_bf_comb_list = mtrx_s_bf_comb(cand_cas_list, db_list)[1][1]

    all_comb_idx_list = comb_idx(len(db_idx_bf_comb_list), n)

    all_comb_mat_s_arr_t = []
    all_comb_mat_cas = []


    for comb_idx_grp in all_comb_idx_list:

        comb_for_s_arr_t = []
        comb_for_cas = []

        for i in range(0, n):
            
            idx = comb_idx_grp[i]
            comb_for_s_arr_t.append(mat_s_bf_comb_arr_t[idx])
            comb_for_cas.append(db_cas_bf_comb_list[idx])
        
        all_comb_mat_s_arr_t.append(comb_for_s_arr_t)
        all_comb_mat_cas.append(comb_for_cas)

    # print(all_comb_mat_s_arr_t)
    # print(np.array(all_comb_mat_s_arr_t[0]).transpose())
    # print(all_comb_mat_cas)
    
    return all_comb_mat_s_arr_t, all_comb_mat_cas


def all_mat_s_arr(all_mat_s_arr_t):
    
    all_mat_s_arr_t_back = []
    
    for arr_t in all_mat_s_arr_t:

        arr_t_back = np.array(arr_t).transpose()
        all_mat_s_arr_t_back.append(arr_t_back)
    
    # print(all_mat_s_arr_t_back)
    return all_mat_s_arr_t_back

def solv_pinv_s(mat_s_arr):
    """
    calculate the left pseudo inverse of matrix s
    """

    pinv_s_arr = pinv(mat_s_arr)

    return pinv_s_arr

def tgt_hsp_vec(tgt_hsp_list):

    flt_tgt_hsp_list = list(np.float_(tgt_hsp_list)) # the original usr input hsps are string type

    flt_tgt_hsp_list.append(1)

    tgt_hsp_vec_with_1 = np.array(flt_tgt_hsp_list)

    return tgt_hsp_vec_with_1


def perturb_mat_d(tgt_hsp_list, rep_ptb_time = 50, var = 0.1):
    """
    apply perturbation on the target hsp
    var is the variance of gaussian random variable serving as the perturbation
    """
    tgt_hsp_with_1 = tgt_hsp_vec(tgt_hsp_list)

    print('Generating perturbated target HSP matrix... ')

    pbt_mat = np.random.randn(rep_ptb_time, 4) * (var, var, var, 0)

    mat_d_bf_t = pbt_mat + tgt_hsp_with_1

    mat_d_t = np.array(mat_d_bf_t).transpose() # mat_d_t is now a 4 x rep_ptb_time matrix

    print('Perturbated target matrix: ')
    print(mat_d_t)

    return mat_d_t


def solv_c_from_s_d(mat_s_arr, mat_d_arr):
    """
    solve coefficient matrix c
    """
    mat_c_arr = solv_pinv_s(mat_s_arr) @ mat_d_arr

    # print('mat_c_arr: ')
    # print(mat_c_arr)

    return mat_c_arr


def nparr_vec(np_arr):
    """
    convert operated array to n x 1 vec
    """
    np_arr_list = []
    
    for entry in np_arr:

        np_arr_list.append(entry)
    
    np_arr_vec = np.array([np_arr_list]).transpose()

    return np_arr_vec





def solv_avg_std_sum_c(mat_c_arr):
    """
    solve the repeated time averaged c and corresponding std
    solve the sum of mean
    """
    c_mean_ov_t_arr = np.mean(mat_c_arr, axis = 1)# work out the mean for each row in c
    c_std_ov_t_arr = np.std(mat_c_arr, axis = 1)
    c_tot_of_n = sum(c_mean_ov_t_arr)

    c_mean_t_vec = nparr_vec(c_mean_ov_t_arr)
    c_std_t_vec = nparr_vec(c_std_ov_t_arr)

    # print('c_mean_t_vec: ')
    # print(c_mean_t_vec)
    # print('c_mean_t[0]: ')
    # print(c_mean_ov_t_arr[0])
    # print('c_tot_of_n: ')
    # print(c_tot_of_n)

    return c_mean_t_vec, c_std_t_vec, c_tot_of_n


def solv_e_from_s_c_d(mat_s_arr, mat_d_arr, mat_c_arr):
    """
    calculate the error matrix based on the difference of sc and d
    """
    mat_e_arr = mat_s_arr @ mat_c_arr - mat_d_arr

    e_mean_ov_t_arr = np.mean(mat_e_arr, axis = 1)

    e_std_ov_t_arr = np.std(mat_e_arr, axis = 1)

    e_mean_vec = nparr_vec(e_mean_ov_t_arr)
    e_std_vec = nparr_vec(e_std_ov_t_arr)

    return [e_mean_vec, e_std_vec]


def conc_filt_c(c_mean_vec, tol_conc_check):
    """
    based on the tol_conc validate results, updt redundant solv conc to 0
    """
    conc_filt_c_list = []

    for i, c_mean in enumerate(c_mean_vec):

        # idx_in_c = tol_conc_check[i][0]
        is_conc_vld = tol_conc_check[i][-1]

        if is_conc_vld == True:
            conc_filt_c_list.append(c_mean[0])
        
        else:
            conc_filt_c_list.append(0)
    
    conc_filt_c_mean_vec = np.array([conc_filt_c_list]).transpose()

    return conc_filt_c_mean_vec


def renorm_c(c_mean_vec):
    """
    this mat_c has been updated by replacing entries below tol_conc with 0
    """
    # print('toberenormed c_mean_t: ')
    # print(c_mean_vec)
    
    tot_c = sum(c_mean_vec)[0]
    # print('tot_c: ')
    # print(tot_c)

    norm_c_mean_list = []

    for c_mean in c_mean_vec:
        
        # print('element in c_mean_vec during update:')
        # print(c_mean)

        norm_c_mean = c_mean[0]/tot_c
        norm_c_mean_list.append(norm_c_mean)
    
    
    # print('norm_c_list: ')
    # print(norm_c_mean_list)

    norm_c_mean_vec = np.array([norm_c_mean_list]).transpose()

    # print('norm_c_vec: ')
    # print(norm_c_mean_vec)


    return norm_c_mean_vec


def norm_c_err(norm_c_mean_vec, mat_s, tgt_hsp):
    """
    calculate the final error based on the renormalised c and standard matrix s minus the target hsp
    """

    tgt_hsp_with_1_arr = np.array([tgt_hsp_vec(tgt_hsp)]).transpose()

    norm_c_err_vec = mat_s @ norm_c_mean_vec - tgt_hsp_with_1_arr

    return norm_c_err_vec


def calc_vld_all_c(cand_cas_list, db_list, n, tgt_hsp_list, tol_err_list, tol_conc):
    # invalid result will not be filtered out immediately, but will be marked with an invld note and filter in the final step

    flt_tol_conc = float(tol_conc)

    all_mat_s_t, all_mat_cas = itrt_cand(cand_cas_list, db_list, n)

    tgt_hsp_with_1_arr = np.array([tgt_hsp_vec(tgt_hsp_list)]).transpose() # tgt hsp list end with 1
    # print(tgt_hsp_with_1_arr)

    mat_d = perturb_mat_d(tgt_hsp_list, rep_ptb_time = 50, var = 0.1) # perturbated target hsp matrix

    calc_log_list = []

    vld_comb_number = 0

    for i in range(0, len(all_mat_s_t)):

        mat_s = np.array(all_mat_s_t[i]).transpose()
        # print('mat_s: ')
        # print(mat_s)

        cas_comb = all_mat_cas[i]

        mat_c = solv_c_from_s_d(mat_s, mat_d)

        # print('mat_c: ')
        # print(mat_c)

        # print('mat_d: ')
        # print(mat_d)
        # # mat_c = np.array(solv_c_from_s_d(mat_s, mat_d)).transpose()
        # # print(mat_c)
        c_mean_t, c_std_t, c_tot = solv_avg_std_sum_c(mat_c)
        
        # print('c_mean_t: ')
        # print(c_mean_t)

        c_stable_chk = sp_vld_chk.is_c_stable(c_std_t, tol_rep_std = 0.1)
        c_vld_chk = sp_vld_chk.is_c_vld(c_mean_t)

        e_mean_t, e_std_t = solv_e_from_s_c_d(mat_s, mat_d, mat_c)
        
        # print(e_mean_t, e_std_t)

        e_vld_chk = sp_vld_chk.is_err_mat_accptbl(e_mean_t, tol_err_list)

        rough_c_e_chk_list = [c_stable_chk, c_vld_chk, e_vld_chk]

        if False in rough_c_e_chk_list:
            err_msg = 'UnstableResult'
            cal_result = [cas_comb, [c_mean_t, c_std_t], [e_mean_t, e_std_t]]
            calc_log_list.append([i, cal_result, err_msg, False])
        
        else:
            norm_c = renorm_c(c_mean_t)
            print('norm_c in main: ')
            print(norm_c)

            conc_tol_check_log = sp_vld_chk.is_conc_above_tol(norm_c, flt_tol_conc)

            low_conc_updt_c = conc_filt_c(norm_c, conc_tol_check_log)

            norm_conc_updt_c = renorm_c(low_conc_updt_c)

            # print('mat_s: ')
            # print(mat_s)
            # print('norm_conc_updt_c: ')
            # print(norm_conc_updt_c)
            # print('tgt_hsp_with_1_arr: ')
            # print(tgt_hsp_with_1_arr)
            
            norm_e = mat_s @ norm_conc_updt_c - tgt_hsp_with_1_arr

            # print('norm_e: ')
            # print(norm_e)

            # print('tol_err_list: ')
            # print(tol_err_list)

            e_hsp_check = sp_vld_chk.is_err_mat_accptbl(norm_e, tol_err_list)

            if e_hsp_check == False:
                err_msg = 'ErrorTooLarge'
                cal_result = [cas_comb, norm_conc_updt_c, norm_e]
                calc_log_list.append([i, cal_result, err_msg, False]) 
                vld_comb_number += 0
               
            else:
                cal_result = [cas_comb, norm_conc_updt_c, norm_e]
                vld_msg = 'Valid'
                calc_log_list.append([i, cal_result, vld_msg, True])
                vld_comb_number += 1
    
    
    vld_comb_chk = sp_vld_chk.is_vld_comb_exist(vld_comb_number) # check if the vld comb is not empty

    if vld_comb_chk == False:

        continue_idx = 0
    
    else:

        continue_idx = 1
    # print('calculation log: ')
    # print(calc_log_list)
    # sp_io.calc_log_list2json(calc_log_list)

    sp_io.calc_log_list2js(calc_log_list)
    

    return continue_idx, calc_log_list


    

    
































    






    










     

