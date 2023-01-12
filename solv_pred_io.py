import os
import json
from datetime import datetime
from datetime import date
import numpy as np

import solv_pred_valid_check as sp_vld_chk
import solv_pred_reg_txt as sp_rtxt
import solv_pred_fetch_info as sp_ftch_info

today = date.today()
now = datetime.now()

def load_js(js_file: str) -> json:
    """_Return loaded json_

    Args:
        js_file (str): _json file name under cwd
    
    Returns:
        json
    """
    current_path = os.getcwd()
    full_js_path = current_path + "\\" + str(js_file)

    with open(full_js_path) as f:
        js = json.load(f)

    #print(db_js[1]["CAS"])

    return js

def input_cas():
    """
    construct solvent candidate list from user input
    check the format of cas no is valid
    """

    usr_cas_list = []
    i = 0
    to_continue = True

    while to_continue:

        usr_input_cas = input("Please enter the CAS No. of solvent candidate " + str(i+1) + " : ")
        #print(usr_input_cas)
        usr_input_cas_no_spc = sp_rtxt.rm_spc(usr_input_cas)
        #print(usr_input_cas_no_spc)

        if not usr_input_cas:

            print('Have all the solvent candidates been added?')
            finish_check = continue_check()

            if finish_check== 1:
                to_continue = False

            elif finish_check == 0:
                pass
                # not_finish = ' '
                # while not_finish != '':
                #     not_finish = input("Press enter to continue adding the next solvent. [enter]")

            else:
                sp_vld_chk.invalid_input()
        
        else:
            if not sp_vld_chk.is_cas_form_valid(usr_input_cas):
                print("Wrong CAS No. format")
                sp_vld_chk.invalid_input()
            else:
                usr_cas_list.append(usr_input_cas_no_spc)
                i += 1
    
    #print(usr_cas_list)
    return usr_cas_list


def db_info_list2dict(db_info_list):
    """
    convert the operated db_info_list back to dict
    """
    # all_property_name = []
    # all_property_all_data = []
    all_tuple_to_dict_list = []

    for property in db_info_list:
        
        property_name = property[0]
        property_all_data = property[1]
        # all_property_name.append(property_name)
        # all_property_all_data.append(property_all_data)

        tuple_to_dict = tuple([property_name, property_all_data])
        all_tuple_to_dict_list.append(tuple_to_dict)
    
    db_info_dict = dict(all_tuple_to_dict_list)

    return db_info_dict


def continue_check():

    continue_check_ip = sp_rtxt.rm_spc(input('[y/n]: ').lower())

    if continue_check_ip in ['y', 'yes']:
        continue_idx = 1
    elif continue_check_ip in ['n', 'no']:
        continue_idx = 0
    else:
        continue_idx = -1
    
    return continue_idx

def get_key(key):
    return lambda x:x.get(key)

def db_init(db_js: json) -> list:
    """_Return a list of keys and corresponding all values from db_

    Args:
        db_js (json): loaded db
    
    Returns:
        list: 
    
    """
    key_in_db_list = ['No.', 'CAS', 'Name', 'D', 'P', 'H', 'Mole_vol', 'ims_idx', 'bp', 'mw', 'viscosity', 'vis_temp', 'heat_of_vap', 'hov_temp', 'SMILES']

    full_db_info_list = []

    for key in key_in_db_list:
        db_key_list = [key, list(map(get_key(key), db_js))]
        full_db_info_list.append(db_key_list)
    
    return full_db_info_list


def version_info():
    """
    print version info at the beginning of the program
    """

    date_time = get_datetime()
    version_info = 'SolvPredictor v 2.0 \n License: GPL-3.0 \n'
    print(version_info)

    return version_info, date_time


def get_datetime():
    """
    Get current date and time
    """
    
    current_time = now.strftime("%H:%M:%S")
    
    print(str(today) + '  ' + str(current_time))
    
    date_time = [today, now]

    return date_time

def get_datetime_filename():
    """
    generate unique filename based on time and date
    """

    time_name = sp_rtxt.date_time_form(now)

    return time_name


def list2txt(list_to_convert, txt_name):
    """
    write calc_log_list to txt as reference
    """
    current_path = os.getcwd()

    if os.path.exists(current_path + '\\log'):
        pass
    else:
        os.mkdir('log')
    
    full_txt_path = current_path + "\\log\\" + str(txt_name) + '.txt'

    with open(str(full_txt_path), "w") as op_txt:
        op_txt.write(str(list_to_convert))
    
    return full_txt_path

def calc_log_list2txt(calc_log_list, log_type):
    """
    save the temporary calculation log
    """

    time_name = get_datetime_filename()
    txt_fname = 'calc_log' + str(log_type) + time_name
    
    txt_path = list2txt(calc_log_list, txt_fname)
    
    return txt_path


def calc_log_list2js(calc_log_list):
    """
    convert the calc log list to a dictionary
    ready to be converted to json as output
    """

    # cal_log_dict = {}
    calc_log_json_list = []

    time_name = get_datetime_filename()

    js_name = 'calc_log_bsc_chk_' + time_name

    current_path = os.getcwd()

    if os.path.exists(current_path + '\\log'):
        pass
    else:
        os.mkdir('log')

    full_js_path = current_path + "\\log\\" + str(js_name) + '.json'

    with open(str(full_js_path), "w") as op_js:

        for entry in calc_log_list:

            # cal_log_dict.clear()

            # print('entry: ')
            # print(entry)

            idx = entry[0] #int
            cas_comb = entry[1][0] #list
            conc = np.ndarray.tolist(np.array(entry[1][1]))
            err = np.ndarray.tolist(np.array(entry[1][2]))
            calc_hsp = np.ndarray.tolist(np.array(entry[1][3]))
            quality = entry[2] # string
            validity = str(entry[-1]) # bool2str
            
            data = {
                'idx' : idx,
                'cas_comb' : cas_comb,
                'conc' : conc,
                'err' : err,
                'calc_hsp' : calc_hsp,
                'quality' : quality,
                'validity' : validity
                }
            
            calc_log_json_list.append(data)
        
        # print(calc_log_json_list)

        json.dump(calc_log_json_list, op_js)
    
    return full_js_path, calc_log_json_list


def fail_calc_log(target_temp, n, target_hsp, tol_err, tol_conc, cand_cas_list, cand_name_list, calc_log_js_path):
    """
    summarise calculation details and related results files (based on failed test)
    """
    current_path = os.getcwd()

    time_name = get_datetime_filename()

    log_dir_name = 'log'

    if os.path.exists(current_path + '\\' + log_dir_name):
        pass
    else:
        os.mkdir(log_dir_name)
    
    txt_name = 'log_failed_' + str(time_name)
    
    full_txt_path = current_path + "\\" + log_dir_name + "\\" + txt_name + '.txt'

    version, test_time = version_info()
    current_time = now.strftime("%H:%M:%S")

    tgt_d = target_hsp[0]
    tgt_p = target_hsp[1]
    tgt_h = target_hsp[2]
    tol_err_d = tol_err[0]
    tol_err_p = tol_err[1]
    tol_err_h = tol_err[2]

    to_summarise = {

        'Target D /MPa^(1/2)' : tgt_d,
        'Target P /MPa^(1/2)' : tgt_p,
        'Target H /MPa^(1/2)' : tgt_h,
        'Temperature /degree c' : target_temp,
        'Number of candidates in each combination (n)' : n,
        'Tolerance of error for D /MPa^(1/2)' : tol_err_d,
        'Tolerance of error for P /MPa^(1/2)' : tol_err_p,
        'Tolerance of error for H /MPa^(1/2)' : tol_err_h,
        'Lowest concentration limit' : tol_conc,
        'Candidate cas' : cand_cas_list,
        'Candidate solvents' : cand_name_list,
        'Calculation log path' : calc_log_js_path,
        'Results' : 'Failed',
        'Advice' : 'Please consider to increase the number of candidates or error tolerance.'

    }

    with open(str(full_txt_path), "w") as op_txt:
        
        op_txt.write('===============================' + '\n')
        op_txt.write(str(version) + '\n')
        op_txt.write(str(current_time) + '\n' + str(today) + '\n')
        op_txt.write('===============================' + '\n'+ '\n')
        
        for key in to_summarise:
            op_txt.write(str(key) + ': ' + '\n' + str(to_summarise[key]) + '\n' + '\n')
    
    return full_txt_path


def sucs_calc_log(target_temp, n, target_hsp, tol_err, tol_conc, cand_cas_list, cand_name_list, calc_log_js_path, vld_log_list, db_info_dict):

    """
    output successful calculation results

    save the log for current results by removing all the false data.
    for multi-solvent comb: iterate through the results and reorganise/reformatting the data.

    """
    current_path = os.getcwd()

    time_name = get_datetime_filename()

    log_dir_name = 'log'

    if os.path.exists(current_path + '\\' + log_dir_name):
        pass
    else:
        os.mkdir(log_dir_name)
    
    txt_name = 'log_success_' + str(time_name)
    
    full_txt_path = current_path + "\\" + log_dir_name + "\\" + txt_name + '.txt'

    version, test_time = version_info()
    current_time = now.strftime("%H:%M:%S")

    tgt_d = target_hsp[0]
    tgt_p = target_hsp[1]
    tgt_h = target_hsp[2]
    tol_err_d = tol_err[0]
    tol_err_p = tol_err[1]
    tol_err_h = tol_err[2]

    to_summarise = {

        'Target D /MPa^(1/2)' : tgt_d,
        'Target P /MPa^(1/2)' : tgt_p,
        'Target H /MPa^(1/2)' : tgt_h,
        'Temperature /degree c' : target_temp,
        'Number of candidates in each combination (n)' : n,
        'Tolerance of error for D /MPa^(1/2)' : tol_err_d,
        'Tolerance of error for P /MPa^(1/2)' : tol_err_p,
        'Tolerance of error for H /MPa^(1/2)' : tol_err_h,
        'Lowest concentration limit' : tol_conc,
        'Candidate cas' : cand_cas_list,
        'Candidate solvents' : cand_name_list,
        'Calculation log path' : calc_log_js_path
    }

    # all_fetched_info = []
    with open(str(full_txt_path), "w") as op_txt:
        
        op_txt.write('===============================' + '\n')
        op_txt.write(str(version) + '\n')
        op_txt.write(str(current_time) + '\n' + str(today) + '\n')
        op_txt.write('===============================' + '\n'+ '\n')
        
        for key in to_summarise:
            op_txt.write(str(key) + ': ' + '\n' + str(to_summarise[key]) + '\n' + '\n')
        
        op_txt.write('===============================' + '\n')
        op_txt.write('Results: \n')
        op_txt.write('===============================' + '\n'+ '\n')

        for g, each_comb in enumerate(vld_log_list):

            op_txt.write('Group ' + str(g + 1) + ' : \n\n')

            cas_comb_list = each_comb['cas_comb']

            to_fetch_key = ['Name']

            fetched_info = sp_ftch_info.fetch_info_from_cas_list(cas_comb_list, to_fetch_key, db_info_dict)

            # all_fetched_info.append(fetched_info)

            n_in_each_comb = len(cas_comb_list)

            for i in range(0, n_in_each_comb):

                op_txt.write('solvent ' + str(i + 1) + ' : ')
                solvent_name = fetched_info[i]['Name']
                solvent_cas = fetched_info[i]['CAS']
                op_txt.write(str(solvent_name) + ' (' + str(solvent_cas) + ') \n')
                solvent_conc = each_comb['conc'][i][0]
                op_txt.write('concentration ' + str(i + 1) + " : "+ f"{solvent_conc: .2%}" + ' \n')
                op_txt.write('\n')
            
            calc_hsp = each_comb['calc_hsp']
            calc_err = each_comb['err']
            
            calc_d = calc_hsp[0][0]
            calc_p = calc_hsp[1][0]
            calc_h = calc_hsp[2][0]

            err_d = calc_err[0][0]
            err_p = calc_err[1][0]
            err_h = calc_err[2][0]

            op_txt.write('calculated D /MPa^(1/2): ' + str(calc_d) + '\n')
            op_txt.write('calculated P /MPa^(1/2): ' + str(calc_p) + '\n')
            op_txt.write('calculated H /MPa^(1/2): ' + str(calc_h) + '\n')
            op_txt.write('error of D /MPa^(1/2): ' + str(err_d) + '\n')
            op_txt.write('error of P /MPa^(1/2): ' + str(err_p) + '\n')
            op_txt.write('error of H /MPa^(1/2): ' + str(err_h) + '\n')

            op_txt.write('\n\n********\n')
    
    return full_txt_path


def adv_filt_exp_list2json(adv_filt_exp_list, js_type):
    """
    convert full results after advanced filtration into json
    """
    calc_log_json_list = []

    time_name = get_datetime_filename()

    js_name = js_type + time_name

    current_path = os.getcwd()

    if os.path.exists(current_path + '\\log'):
        pass
    else:
        os.mkdir('log')

    full_js_path = current_path + "\\log\\" + str(js_name) + '.json'

    with open(str(full_js_path), "w") as op_js:

        for i, solv_comb in enumerate(adv_filt_exp_list):

            data = {
                'group' : i,
                'full_detail' : solv_comb
            }
            
            calc_log_json_list.append(data)
        
        # print(calc_log_json_list)

        json.dump(calc_log_json_list, op_js)
    
    return full_js_path, calc_log_json_list


def adv_filt_fail_log(bsc_ip_info_dict, adv_all_js_path, filt_opt):
    """
    output log for failed advanced filtration
    """
    current_path = os.getcwd()

    time_name = get_datetime_filename()

    log_dir_name = 'log'

    if os.path.exists(current_path + '\\' + log_dir_name):
        pass
    else:
        os.mkdir(log_dir_name)
    
    txt_name = 'log_adv_filt_fail_' + str(time_name)
    
    full_txt_path = current_path + "\\" + log_dir_name + "\\" + txt_name + '.txt'

    version, test_time = version_info()
    current_time = now.strftime("%H:%M:%S")

    basic_ip_dict = bsc_ip_info_dict


    filt_opt_updt = []
    
    for opt in filt_opt:

        if opt not in ['solvent', 'idx']:
            filt_opt_updt.append(opt)


    # all_fetched_info = []
    with open(str(full_txt_path), "w") as op_txt:
        
        op_txt.write('===============================' + '\n')
        op_txt.write(str(version) + '\n')
        op_txt.write(str(current_time) + '\n' + str(today) + '\n')
        op_txt.write('===============================' + '\n'+ '\n')
        
        for key in basic_ip_dict:
            op_txt.write(str(key) + ': ' + '\n' + str(basic_ip_dict[key]) + '\n' + '\n')

        op_txt.write('Advanced filter options: \n' + str(filt_opt_updt)  + '\n' + '\n')

        op_txt.write('Full calculation log before filtration path: \n' + str(adv_all_js_path) + '\n' + '\n')
        
        op_txt.write('===============================' + '\n')
        op_txt.write('Results: \n')
        op_txt.write('===============================' + '\n'+ '\n')

        op_txt.write('Failed to find any combination matching the requirement.' + '\n'+ '\n')

    return full_txt_path


def adv_filt_sucs_log(adv_filt_exp_list, filt_opt, adv_js_path, adv_all_js_path, bsc_ip_info_dict):
    """
    export the final log after advanced filtration
    """
    current_path = os.getcwd()

    time_name = get_datetime_filename()

    log_dir_name = 'log'

    if os.path.exists(current_path + '\\' + log_dir_name):
        pass
    else:
        os.mkdir(log_dir_name)
    
    txt_name = 'log_adv_filt_success_' + str(time_name)
    
    full_txt_path = current_path + "\\" + log_dir_name + "\\" + txt_name + '.txt'

    version, test_time = version_info()
    current_time = now.strftime("%H:%M:%S")

    basic_ip_dict = bsc_ip_info_dict


    filt_opt_updt = []
    
    for opt in filt_opt:

        if opt not in ['solvent', 'idx']:
            filt_opt_updt.append(opt)


    # all_fetched_info = []
    with open(str(full_txt_path), "w") as op_txt:
        
        op_txt.write('===============================' + '\n')
        op_txt.write(str(version) + '\n')
        op_txt.write(str(current_time) + '\n' + str(today) + '\n')
        op_txt.write('===============================' + '\n'+ '\n')
        
        for key in basic_ip_dict:
            op_txt.write(str(key) + ': ' + '\n' + str(basic_ip_dict[key]) + '\n' + '\n')
        
        

        op_txt.write('Advanced filter options: \n' + str(filt_opt_updt)  + '\n' + '\n')
        
        op_txt.write('Calculation log path: \n' + str(adv_js_path) + '\n' + '\n')

        op_txt.write('Full calculation log before filtration path: \n' + str(adv_all_js_path) + '\n' + '\n')
        
        op_txt.write('===============================' + '\n')
        op_txt.write('Results: \n')
        op_txt.write('===============================' + '\n'+ '\n')

        for g, each_comb in enumerate(adv_filt_exp_list):

            op_txt.write('Group ' + str(g + 1) + ' : \n\n')

            # n_in_each_comb = len(each_comb)

            for i, solv in enumerate(each_comb):

                op_txt.write('solvent ' + str(i + 1) + ' : ')
                solvent_name = solv['Name']
                solvent_cas = solv['CAS']
                op_txt.write(str(solvent_name) + ' (' + str(solvent_cas) + ') \n')
                solvent_conc = solv['conc']
                op_txt.write('concentration ' + str(i + 1) + " : "+ f"{solvent_conc: .2%}" + ' \n')
                op_txt.write('\n')

                bp = solv['bp']
                op_txt.write('bp /degree C: ' + str(bp) + '\n' + '\n')

                
                ims_chk_msg = solv['ims_chk_msg']
                op_txt.write('miscibility check: \n')
                op_txt.write(str(ims_chk_msg) + '\n' + '\n')

                if i == len(each_comb) - 1:

                    calc_d = solv['calc_d']
                    calc_p = solv['calc_p']
                    calc_h = solv['calc_h']
                    err_d = solv['err_d']
                    err_p = solv['err_p']
                    err_h = solv['err_h']

                    op_txt.write('calculated D /MPa^(1/2): ' + str(calc_d) + '\n')
                    op_txt.write('calculated P /MPa^(1/2): ' + str(calc_p) + '\n')
                    op_txt.write('calculated H /MPa^(1/2): ' + str(calc_h) + '\n')
                    op_txt.write('error of D /MPa^(1/2): ' + str(err_d) + '\n')
                    op_txt.write('error of P /MPa^(1/2): ' + str(err_p) + '\n')
                    op_txt.write('error of H /MPa^(1/2): ' + str(err_h) + '\n')

                    op_txt.write('\n\n********\n')
    
    return full_txt_path



