#This document allows personalise safety handle information for candidates selection.
#An interactive version can be found in candidate_prepare_by_safety_info.ipynb


import pandas as pd
import json
import numpy as np

#full safety keywords list
safety_kw_list = ['Flammable', 'Irritant', 'HealthHazard', 'Corrosive', 'AcuteToxic', 'EnvironmentalHazard', 'CompressedGas']

#Please modify your safety concern list, example:
concern_list = ["AcuteToxic", "EnvironmentalHazard", "HealthHazard"]

#load the database with safety keywords
file_name = "db_with_safe_info_reform.csv"

db_safe_df = pd.read_csv(file_name)
db_safe_dict = db_safe_df.to_dict("records")

def get_cand_without_safety_concern(full_data_dict = db_safe_dict, concern = ["AcuteToxic", "EnvironmentalHazard"]):
    safe_subset = []
    for entry in full_data_dict:
        safe_concern_found = 0
        entry["concern_type"] = []
        this_safety_kw = entry["safety_kw"]
#         print(this_safety_kw)
        if this_safety_kw is not np.NAN:
            for kw in this_safety_kw[1:-1].replace("'", "").split(","):
                if kw in concern:
                    safe_concern_found = 1
                    entry["concern_type"].append(kw)
                    
            if safe_concern_found == 0:
                entry["is_concern"] = "False"
                safe_subset.append(entry)
                entry["concern_type"] = -1
            else:
                entry["is_concern"] = "True"
        else:
            entry["is_concern"] = -1
            entry["concern_type"] = -1
            safe_subset.append(entry)

    return safe_subset, full_data_dict


safe_subset, db_filt = get_cand_without_safety_concern(full_data_dict = db_safe_dict, concern = concern_list)
#save subset and full data with safety classifided information

#specify your file reference, e.g., non_health_hazard
file_ref = "non_toxic_non_health_hazard_green"

#save full db with classified information
db_with_safe_info_classified = pd.DataFrame(db_filt)
db_with_safe_info_classified.to_csv(f"db_with_safe_info_classified_{file_ref}.csv", index = None)
db_with_safe_info_classified.to_json(f"db_with_safe_info_classified_{file_ref}.json", orient = "records")

#save db with candidate subset only
safe_subset_df = pd.DataFrame(safe_subset)
safe_and_green_candidates = pd.DataFrame()
safe_and_green_candidates["CAS"] = safe_subset_df["CAS"]
safe_and_green_candidates["Solvent"] = safe_subset_df["Name"]
# safe_and_green_candidates.head()
safe_and_green_candidates.to_csv(f"{file_ref}_candidates.csv", index = None)
safe_and_green_candidates.to_json(f"{file_ref}_candidates.json", orient ="records")
