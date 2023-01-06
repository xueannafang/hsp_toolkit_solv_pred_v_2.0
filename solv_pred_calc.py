import numpy as np
from scipy.linalg import pinv
import itertools
import solv_pred_fetch_info as sp_ftch_info

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

    pinv_s_arr = np.linalg.pinv(mat_s_arr)

    return pinv_s_arr

def perturb_mat_d(tgt_hsp_list, rep_ptb_time = 50, var = 0.1):
    """
    apply perturbation on the target hsp
    var is the variance of gaussian random variable serving as the perturbation
    """
    # init_mat_d = np.zeros((4, rep_ptb_time))

    flt_tgt_hsp_list = list(np.float_(tgt_hsp_list)) # the original usr input hsps are string type

    tgt_hsp_vec_with_1 = flt_tgt_hsp_list.append(1)

    # tgt_hsp_vec = np.array([tgt_hsp_vec_with_1]).transpose()
    
    pbt_mat = np.random.randn(rep_ptb_time, 4) * (var, var, var, 0)

    mat_d_bf_t = pbt_mat + tgt_hsp_vec_with_1

    mat_d_t = np.array(mat_d_bf_t).transpose() # mat_d_t is now a 4 x rep_ptb_time matrix

    return mat_d_t


def solv_c_from_s_d(mat_s_arr, mat_d_arr):
    """
    solve coefficient matrix c
    """
    mat_c_arr = solv_pinv_s(mat_s_arr) @ mat_d_arr

    return mat_c_arr


def stat_check_c(mat_c_arr, tol_rep_std = 0.1):
    """
    for as-calculated matrix c:
        check if the standard deviation along all the perturbation is below tol_rep_std (default = 0.1)
        check if the total concentration is above 105% or below 95%
    """

    c_mean_ov_t_arr = np.mean(mat_c_arr, axis = 1) # work out the mean for each row in c
    c_std_ov_t_arr = np.std(mat_c_arr, axis = 1)
    c_tot_of_n = sum(c_mean_ov_t_arr)

    stat_check_c = True

    if c_std_ov_t_arr > tol_rep_std or c_tot_of_n > 1.05 or c_tot_of_n < 0.95:
        stat_check_c = False
    
    return stat_check_c

    

    
































    






    










     

