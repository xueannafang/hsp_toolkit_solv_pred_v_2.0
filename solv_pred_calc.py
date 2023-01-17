import numpy as np
from scipy.linalg import pinv
import itertools
import solv_pred_fetch_info as sp_ftch_info
import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io

def mtrx_s_bf_comb(cand_cas_list: list, db_list: list) -> list:
    """return the standard hsp matrix s before combination (with all candidates), and corresponding full db idx list and cas list involved.

    Args:
        cand_cas_list (list): cas of all the candidates.
        db_list (list): full db info list [key_i, all values of key_i].

    Returns:
        list: [s_bf_comb, [all_db_idx_list, all_db_cas_list]].
        s_bf_comb: total matrix s with all candidates (4 x all cand, the first three rows are d, p, h, respectively; the last row is 1).



    """
    
    total_cand = len(cand_cas_list) # total candidate number

    s_bf_comb = np.ones((4, total_cand)) # initialise full matrix s

    cand_all_info = sp_ftch_info.fetch_idx_cas_hsp(cand_cas_list, db_list) # fetch all hsp and cas, db_idx info [[idx_i, cas_i, [d_i, p_i, h_i]]] for all candidates 

    all_db_idx_list = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'idx') # fetch db idx for all candidates and store in one list

    all_db_cas_list = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'cas') # fetch cas for all candidates and store in one list

    # fetch sub hsp and store in one list

    all_d = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'd')
    all_p = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'p')
    all_h = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'h')

    s_bf_comb[0] = all_d # first row of matrix s_bf_comb
    s_bf_comb[1] = all_p # second row
    s_bf_comb[2] = all_h # third row

    return [s_bf_comb, [all_db_idx_list, all_db_cas_list]]

def gen_idx(list_length: int) -> list:
    """return a list of idx converted from a list with a given length.

    Args:
        list_length (int): length of list to generate idx.

    Returns:
        list: idx.
    """
    
    i = 0

    n_idx_list = []
    for i in range(0, list_length):

        n_idx_list.append(i)

    return n_idx_list


def comb_idx(len_list: int, n: int) -> list:
    """return list of all combinations idx.

    Args:
        len_list (int): total candidate number.
        n (int): number of solvents in each combination.

    Returns:
        list: all n-solvent combinations of idx in current candidate list.
    """

    idx_list = gen_idx(len_list) # list of idx.

    all_comb_idx_list = []

    for comb in itertools.combinations(idx_list, n):

        all_comb_idx_list.append(list(comb)) # n-solvent combination in the form of idx in the candidate list.
    
    return all_comb_idx_list

def itrt_cand(cand_cas_list: list, db_list: list, n: int) -> tuple[list, list]:
    """return a list of transposed standard HSP matrix S with all posible n solvent combinations and a corresponding matrix lsit of cas.

    Args:
        cand_cas_list (list): cas of all the candidates.
        db_list (list): full db info list [key_i, all values of key_i].
        n (int): number of solvents in each comb.

    Returns:
        tuple[list, list]: [all_comb_mat_s_arr_t, all_comb_mat_cas].

        The first component is a list of all possible combinations in the form of the transpose of standard HSP matrix S. Each matrix S (transposed) is a n x 4 matrix, with the first three columns in the order of d, p, h; the final column is 1.

        The second is the corresponding list of cas matrix.
    """

    mat_s_bf_comb = mtrx_s_bf_comb(cand_cas_list, db_list)[0] # a full mat s involving all candidates hsp info, 4 by total candidate number

    mat_s_bf_comb_arr_t = np.array(mat_s_bf_comb).transpose() # get ready to store column info. convert mat_s_bf_comb to np.array and transpose it into total_cand by 4 matrix.

    db_idx_bf_comb_list = mtrx_s_bf_comb(cand_cas_list, db_list)[1][0] # db_idx of all candidates.

    db_cas_bf_comb_list = mtrx_s_bf_comb(cand_cas_list, db_list)[1][1] # cas of all candidates.

    all_comb_idx_list = comb_idx(len(db_idx_bf_comb_list), n) # all combinations of idx [comb_i = [idx_1, idx_2, ..., idx_n]]

    all_comb_mat_s_arr_t = []
    all_comb_mat_cas = []


    for comb_idx_grp in all_comb_idx_list: # iterate through all the possible combinations

        comb_for_s_arr_t = []
        comb_for_cas = []

        # in each combination

        for i in range(0, n):
            
            idx = comb_idx_grp[i] # idx in the current combination
            comb_for_s_arr_t.append(mat_s_bf_comb_arr_t[idx]) # append the ith row of total mat s (transposed)
            comb_for_cas.append(db_cas_bf_comb_list[idx]) # append corresponding cas.
        
        all_comb_mat_s_arr_t.append(comb_for_s_arr_t) # append combined matrix info to total list
        all_comb_mat_cas.append(comb_for_cas) # append combined cas info to total list
    
    return all_comb_mat_s_arr_t, all_comb_mat_cas


def all_mat_s_arr(all_mat_s_arr_t):

    all_mat_s_arr_t_back = []
    
    for arr_t in all_mat_s_arr_t:

        arr_t_back = np.array(arr_t).transpose()
        all_mat_s_arr_t_back.append(arr_t_back)
    
    # print(all_mat_s_arr_t_back)
    return all_mat_s_arr_t_back

def solv_pinv_s(mat_s_arr):
    """return the left pseudoinverse of matrix S.

    Args:
        mat_s_arr (np.ndarray): 4 x n standard hsp matrix S.

    Returns:
        np.ndarray: left pseudoinverse of matrix S (in the size of n x 4).
    """

    pinv_s_arr = pinv(mat_s_arr) # solve left pseudoinverse

    return pinv_s_arr

def tgt_hsp_vec(tgt_hsp_list: list):
    """return target hsp vector in the format of array[d, p, h, 1].

    Args:
        tgt_hsp_list (list): [d, p, h]

    Returns:
        np.ndarray: [d, p, h, 1]
    """

    flt_tgt_hsp_list = list(np.float_(tgt_hsp_list)) # convert [str, str, str] to [float, float, float]

    flt_tgt_hsp_list.append(1) # attach the boundary condition 1 to the end of the list

    tgt_hsp_vec_with_1 = np.array(flt_tgt_hsp_list) # convert list to array

    return tgt_hsp_vec_with_1


def perturb_mat_d(tgt_hsp_list: list, rep_ptb_time: int = 50, var: float = 0.1):
    """return GRN perturbated target hsp array, i.e., matrix D. 
    

    Args:
        tgt_hsp_list (list): [d, p, h]
        rep_ptb_time (int, optional): repeated perturbation time. Defaults to 50.
        var (float, optional): a scale factor of the gaussian random variable serving as the perturbation amplitude restriction (-var, var). Defaults to 0.1.

    Returns:
        np.ndarray: a 4 x t mat d after with each target hsp modifed by a GRN.
    """
    
    tgt_hsp_with_1 = tgt_hsp_vec(tgt_hsp_list)

    print('Generating perturbated target HSP matrix... ')

    pbt_mat = np.random.randn(rep_ptb_time, 4) * (var, var, var, 0) # perturbation matrix (t x 4) with GRN ranging from -var to var for the first three columns (which applys to hsp) and no perturbation for the final column (1, the boundary condition)

    mat_d_bf_t = pbt_mat + tgt_hsp_with_1 # broadcast the target hsp vector list by adding it to each row of perturbation matrix, resulting the t x 4 perturbated target matrix (before transpose).

    mat_d_t = np.array(mat_d_bf_t).transpose() # mat_d_t is now a 4 x t matrix

    print('Done.')
    # print(mat_d_t)

    return mat_d_t


def solv_c_from_s_d(mat_s_arr, mat_d_arr):
    """return the coefficient matrix C by calculating the left pseudoinverse of mat S and apply it to mat D.

    Args:
        mat_s_arr (np.ndarray): standard hsp matrix S, 4 x n.
        mat_d_arr (np.ndarray): perturbated target hsp matrix, 4 x t.

    Returns:
        np.ndarray: coefficient or concentration matrix C (in the size of n x t). Row i corresponds to the concentraion of the ith solvent in mat S. Column j is the tth calculation. 
    """
    # print(mat_s_arr)
    # print(type(mat_s_arr))
    mat_c_arr = solv_pinv_s(mat_s_arr) @ mat_d_arr

    return mat_c_arr


def nparr_vec(np_arr):
    """return a n x 1 array from a 1 x n array.

    Args:
        np_arr (np.ndarray): 1 x n.

    Returns:
        np.ndarray: n x 1.
    """
    
    np_arr_list = []
    
    for entry in np_arr:

        np_arr_list.append(entry)
    
    np_arr_vec = np.array([np_arr_list]).transpose()

    return np_arr_vec





def solv_avg_std_sum_c(mat_c_arr: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """reutrn the average and std of the concentration matrix C over t and the total concentration of t-averaged c over n.

    Args:
        mat_c_arr (np.ndarray): n x t matrix C.

    Returns:
        tuple[np.ndarray, np.ndarray, float]: [n x 1 (average over t), n x 1 (std over t), sum of c_mean_t (total concentration)].
    """
    
    c_mean_ov_t_arr = np.mean(mat_c_arr, axis = 1)# work out the mean for each row in c over t; the resulting format will be a 1d array with n elements.
    c_std_ov_t_arr = np.std(mat_c_arr, axis = 1)# standard deviation of each row in c over t; the resulting format will be a 1d array with n elements.
    c_tot_of_n = sum(c_mean_ov_t_arr) # sum of all column of c_mean_ov_t_arr to get the total concentration for this combination

    c_mean_t_vec = nparr_vec(c_mean_ov_t_arr) # 1 x n to n x 1
    c_std_t_vec = nparr_vec(c_std_ov_t_arr) # 1 x n to n x 1

    return c_mean_t_vec, c_std_t_vec, c_tot_of_n


def solv_e_from_s_c_d(mat_s_arr: np.ndarray, mat_d_arr: np.ndarray, mat_c_arr: np.ndarray) -> list:
    """return the error matrix based on s@c-d.

    Args:
        mat_s_arr (np.ndarray): matrix S, 4 x n.
        mat_d_arr (np.ndarray): matrix D, 4 x t.
        mat_c_arr (np.ndarray): matrix C, n x t.

    Returns:
        list: [t-averaged error matrix (nd.nparray, n x 1), std of error matrix over t (nd.nparray, n x 1)]
    """
    
    mat_e_arr = mat_s_arr @ mat_c_arr - mat_d_arr

    e_mean_ov_t_arr = np.mean(mat_e_arr, axis = 1) # average over t

    e_std_ov_t_arr = np.std(mat_e_arr, axis = 1) # std over t

    e_mean_vec = nparr_vec(e_mean_ov_t_arr) # 1 x n to n x 1 

    e_std_vec = nparr_vec(e_std_ov_t_arr) # 1 x n to n x 1

    return [e_mean_vec, e_std_vec]


def conc_filt_c(c_mean_vec: np.ndarray, tol_conc_check: list) -> np.ndarray:
    """return updated mat c based on the tol_conc validate results, updt redundant solv conc to 0.

    Args:
        c_mean_vec (np.ndarray): original n x 1 matrix C.
        tol_conc_check (list): concentration check log in the format of [[solv_idx i, validity (bool)]].

    Returns:
        np.ndarray: update matrix C by setting the concentration of redundant solvents as 0.
    """
    
    conc_filt_c_list = []

    for i, c_mean in enumerate(c_mean_vec):

        is_conc_vld = tol_conc_check[i][-1] # validity check

        if is_conc_vld is True:

            conc_filt_c_list.append(c_mean[0]) # append valid solvent
        
        else:

            conc_filt_c_list.append(0) # update conc of redundant solvent entry as 0
    
    conc_filt_c_mean_vec = np.array([conc_filt_c_list]).transpose() # 1 x n to n x 1

    return conc_filt_c_mean_vec


def renorm_c(c_mean_vec: np.ndarray) -> np.ndarray:
    """return updated mat c by normalising total concentration to 1.

    Args:
        c_mean_vec (np.ndarray): original t-averaged mat c. total concentration may slighlty deviate from 1.

    Returns:
        np.ndarray: mat c whose sum over each element is 1.
    """
    
    tot_c = sum(c_mean_vec)[0] # current total concentration over all elements in mat c

    norm_c_mean_list = []

    for c_mean in c_mean_vec:

        norm_c_mean = c_mean[0]/tot_c
        norm_c_mean_list.append(norm_c_mean)

    norm_c_mean_vec = np.array([norm_c_mean_list]).transpose() # 1 x n to n x 1

    return norm_c_mean_vec


def norm_c_err(norm_c_mean_vec, mat_s, tgt_hsp):
    """
    calculate the final error based on the renormalised c and standard matrix s minus the target hsp
    """

    tgt_hsp_with_1_arr = np.array([tgt_hsp_vec(tgt_hsp)]).transpose()

    norm_c_err_vec = mat_s @ norm_c_mean_vec - tgt_hsp_with_1_arr

    return norm_c_err_vec


def calc_vld_all_c(cand_cas_list: list, db_list: list, n: int, tgt_hsp_list: list, tol_err_list: list, tol_conc: float) -> tuple[int, list, str]:
    """return continue_idx, calc_log_js_list, full_calc_log_js_path.

    Args:
        cand_cas_list (list): cas list of all candidates.
        db_list (list): full db info list in the format of [key i, all_values of i].
        n (int): number of solvents in each comb.
        tgt_hsp_list (list): target hsp [d, p, h].
        tol_err_list (list): error [d, p, h].
        tol_conc (float): lowest acceptable concentration.

    Returns:
        tuple[int, list, str]: continue_idx (0 if no results available), cal_log_js_list (full calculation log to be converted to json output), full_calc_log_js_path (the path of json log).
    """
    
    # note that invalid result will not be filtered out immediately, but will be marked with an invld note and filter in the final step

    flt_tol_conc = float(tol_conc)

    all_mat_s_t, all_mat_cas = itrt_cand(cand_cas_list, db_list, n) 

    tgt_hsp_with_1_arr = np.array([tgt_hsp_vec(tgt_hsp_list)]).transpose() # tgt hsp list end with 1

    mat_d = perturb_mat_d(tgt_hsp_list, rep_ptb_time = 50, var = 0.1) # generate perturbated target hsp matrix

    calc_log_list = []

    vld_comb_number = 0


    for i, s_comb in enumerate(all_mat_s_t):

        mat_s = np.array(s_comb).transpose() # mat_s is now a 4 x n matrix
        print(mat_s)
        cas_comb = all_mat_cas[i]

        mat_c = solv_c_from_s_d(mat_s, mat_d) # mat c is a n x t matrix 

        c_mean_t, c_std_t, c_tot = solv_avg_std_sum_c(mat_c) # statistic info

        c_stable_chk = sp_vld_chk.is_c_stable(c_std_t, tol_rep_std = 0.1) # check if c_std_t is within acceptable std

        c_vld_chk = sp_vld_chk.is_c_vld(c_mean_t) # phsycial meaning and stability check

        e_mean_t, e_std_t = solv_e_from_s_c_d(mat_s, mat_d, mat_c) # solve error statistic info

        e_vld_chk = sp_vld_chk.is_err_mat_accptbl(e_mean_t, tol_err_list) # validate if error is within acceptable region

        rough_c_e_chk_list = [c_stable_chk, c_vld_chk, e_vld_chk] # collect three validity info - any invalid means this group is unstable

        calc_hsp_rough = mat_s @ c_mean_t # rough calculated hsp based on mat S and t-averaged mat C

        if False in rough_c_e_chk_list:

            err_msg = 'UnstableResult'

            cal_result = [cas_comb, [c_mean_t, c_std_t], [e_mean_t, e_std_t], calc_hsp_rough]

            calc_log_list.append([i, cal_result, err_msg, False])
        
        else:

            norm_c = renorm_c(c_mean_t) # updt matrix C by normalising the total concentration to 1

            conc_tol_check_log = sp_vld_chk.is_conc_above_tol(norm_c, flt_tol_conc)

            low_conc_updt_c = conc_filt_c(norm_c, conc_tol_check_log) # update low conc solvent into 0

            norm_conc_updt_c = renorm_c(low_conc_updt_c) # renormalise
            
            calc_hsp_norm_c = mat_s @ norm_conc_updt_c # calculated HSP based on renormalised mat C

            norm_e = calc_hsp_norm_c - tgt_hsp_with_1_arr # absolute error between calculated and target HSP (no perturbation)

            e_hsp_check = sp_vld_chk.is_err_mat_accptbl(norm_e, tol_err_list) # error check again

            if e_hsp_check is False:

                err_msg = 'ErrorTooLarge'
                cal_result = [cas_comb, norm_conc_updt_c, norm_e, calc_hsp_norm_c]

                calc_log_list.append([i, cal_result, err_msg, False]) # the last term is the validity of this combination

                vld_comb_number += 0
               
            else:

                cal_result = [cas_comb, norm_conc_updt_c, norm_e, calc_hsp_norm_c]

                vld_msg = 'Valid'

                calc_log_list.append([i, cal_result, vld_msg, True])

                vld_comb_number += 1
    
    
    vld_comb_chk = sp_vld_chk.is_vld_comb_exist(vld_comb_number) # check if the vld comb is not empty

    if vld_comb_chk is False:

        continue_idx = 0 # will not continue the future step
    
    else:

        continue_idx = 1

    full_calc_log_js_path, calc_log_js_list = sp_io.calc_log_list2js(calc_log_list) # write json of full calculation data before advanced filtration

    sp_io.calc_log_list2txt(calc_log_list, '_all_') # write log of full calculation details before advanced filtration
    

    return continue_idx, calc_log_js_list, full_calc_log_js_path


def sucs_result_filt(calc_log_js_list: list) -> list:
    """return successful-only results (i.e., validity is True).

    Args:
        calc_log_js_list (list): full calculation info in a json list.

    Returns:
        list: successful calculation info.
    """
    
    vld_log_list = []

    for each_comb in calc_log_js_list:

        if each_comb['validity'] == 'True':

            vld_log_list.append(each_comb)
        
    sp_io.calc_log_list2txt(vld_log_list, '_vld_')

    return vld_log_list

