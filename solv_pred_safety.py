import requests
import json
import pandas as pd
import time


def get_cid_by_smiles(sm, prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"):
    
    """
    Get CID first
    """
    get_cid_part_url = "/compound/smiles/cids/txt"
    url = prolog + get_cid_part_url
    struct = {'smiles': sm}
    res = requests.get(url, params = struct)
    cid = res.text
    return cid

def get_full_data_by_cid(cid, prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/", form = "/JSON"):
    url = "".join([prolog, str(cid).rstrip(), form])
#     print(url)
    res = requests.get(url)
    return res.text

def get_content_by_sec_head(full_data_json, sec_head = "Chemical Safety"):
    if "Record" in full_data_json.keys():
        found_item = 0
        for item in full_data_json["Record"]["Section"]:
            if "TOCHeading" in item.keys():
                if item["TOCHeading"] == sec_head:
                    return(item)
                    found_item = 1
            else:
                return -1
        if found_item == 0:
            return -1
    else:
        return -1

    
def get_safety_kw_from_safety_section(safety_section):
    if safety_section != -1:
        if "Information" in safety_section.keys():
            safety_info_list = safety_section["Information"]
            all_safety_value_dict = safety_info_list[0]["Value"]

            safety_kw_list = []
            if "StringWithMarkup" in all_safety_value_dict.keys():
                for kw_dict in all_safety_value_dict["StringWithMarkup"][0]["Markup"]:
                    safety_kw_list.append(kw_dict["Extra"])
                return safety_kw_list
            else:
                return -1
        else:
            return -1
    else:
        return -1

        
def get_safety_kw_from_sm(sm):
    cid = get_cid_by_smiles(sm)
    full_data = get_full_data_by_cid(cid)
    full_data_json = json.loads(full_data)
    safety_section = get_content_by_sec_head(full_data_json, sec_head = "Chemical Safety")
    safety_kw_list = get_safety_kw_from_safety_section(safety_section)
    return safety_kw_list
    

solv_db = pd.read_excel("db_mis.xlsx", na_values = "-1")
db_dict = solv_db.to_dict("records")



#get safety info from pubchem in batch
time_count = 0

for entry in db_dict:
    print(entry["No."])
    print(entry["Name"])
    entry_sm = entry["SMILES"]
    if type(entry_sm) is str:
        safety_kw_list = get_safety_kw_from_sm(entry_sm)
        entry["safety_kw"] = safety_kw_list
    else:
        entry["safety_kw"] = -1
    time_count += 1
    if time_count % 4 == 0:
        time.sleep(1)
    print(entry["safety_kw"])
    

db_with_safe = pd.DataFrame.from_dict(data = db_dict)
db_with_safe.head()

# db_with_safe.to_csv("db_with_safe_info.csv", index = None)
db_with_safe.to_json("db_with_safe_info.json", orient = "records")
        

