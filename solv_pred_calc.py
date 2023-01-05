import numpy as np
from scipy.linalg import pinv
import itertools

def mtrx_s_bf_comb(cand_list, db_list):
    """
    construct the standard hsp matrix before combination
    """
    total_cand = len(cand_list)
    init_s_bf_comb = np.ones((4, total_cand))
     

