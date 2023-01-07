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

    pinv_s_arr = pinv(mat_s_arr)

    return pinv_s_arr

def tgt_hsp_vec(tgt_hsp_list):

    flt_tgt_hsp_list = list(np.float_(tgt_hsp_list)) # the original usr input hsps are string type

    tgt_hsp_vec_with_1 = flt_tgt_hsp_list.append(1)

    return tgt_hsp_vec_with_1


def perturb_mat_d(tgt_hsp_list, rep_ptb_time = 50, var = 0.1):
    """
    apply perturbation on the target hsp
    var is the variance of gaussian random variable serving as the perturbation
    """
    tgt_hsp_with_1 = tgt_hsp_vec(tgt_hsp_list)

    pbt_mat = np.random.randn(rep_ptb_time, 4) * (var, var, var, 0)

    mat_d_bf_t = pbt_mat + tgt_hsp_with_1

    mat_d_t = np.array(mat_d_bf_t).transpose() # mat_d_t is now a 4 x rep_ptb_time matrix

    return mat_d_t


def solv_c_from_s_d(mat_s_arr, mat_d_arr):
    """
    solve coefficient matrix c
    """
    mat_c_arr = solv_pinv_s(mat_s_arr) @ mat_d_arr

    return mat_c_arr


def solv_avg_std_sum_c(mat_c_arr):
    """
    solve the repeated time averaged c and corresponding std
    solve the sum of mean
    """
    c_mean_ov_t_arr = np.mean(mat_c_arr, axis = 1) # work out the mean for each row in c
    c_std_ov_t_arr = np.std(mat_c_arr, axis = 1)
    c_tot_of_n = sum(c_mean_ov_t_arr)

    return c_mean_ov_t_arr, c_std_ov_t_arr, c_tot_of_n


def solv_e_from_s_c_d(mat_s_arr, mat_d_arr, mat_c_arr):
    """
    calculate the error matrix based on the difference of sc and d
    """
    mat_e_arr = mat_s_arr @ mat_c_arr - mat_d_arr

    e_mean_ov_t_arr = np.mean(mat_e_arr, axis = 1)

    return e_mean_ov_t_arr


def conc_filt_c(c_mean_vec, tol_conc_check):
    """
    based on the tol_conc validate results, updt redundant solv conc to 0
    """
    conc_filt_c_list = []

    for i, c_mean in enumerate(c_mean_vec):

        # idx_in_c = tol_conc_check[i][0]
        is_conc_vld = tol_conc_check[i][1]

        if is_conc_vld == True:
            conc_filt_c_list.append(c_mean)
        
        else:
            conc_filt_c_list.append(0)
    
    conc_filt_c_mean_vec = np.array([conc_filt_c_list]).transpose()

    return conc_filt_c_mean_vec


def renorm_c(c_mean_vec):
    """
    this mat_c has been updated by replacing entries below tol_conc with 0
    """
    tot_c = sum(c_mean_vec)
    norm_c_mean_list = []

    for c_mean in c_mean_vec:
        norm_c_mean = c_mean/tot_c
        norm_c_mean_list.append(norm_c_mean)
    
    norm_c_mean_vec = np.array([norm_c_mean]).transpose()

    return norm_c_mean_vec


def norm_c_err(norm_c_mean_vec, mat_s, tgt_hsp):
    """
    calculate the final error based on the renormalised c and standard matrix s minus the target hsp
    """

    tgt_hsp_with_1_arr = np.array([tgt_hsp_vec(tgt_hsp)]).transpose()

    norm_c_err_vec = mat_s @ norm_c_mean_vec - tgt_hsp_with_1_arr

    return norm_c_err_vec


def calc_vld_all_c():
    # invalid result will not be filtered out immediately, but will be marked with an invld note and filter in the final step





    pass

    

    
































    






    










     

