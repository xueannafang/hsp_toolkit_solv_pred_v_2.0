import pandas as pd
from rdkit import Chem
from rdkit.Chem import MACCSkeys

db_json_name = "db_solv_pred_v2.json"
db_df = pd.read_json(db_json_name)

db_dict = db_df.to_dict("records")

#dig of target FG

#Check this database for full substructure information: https://github.com/rdkit/rdkit-orig/blob/master/rdkit/Chem/MACCSkeys.py

alcohol = {
    "MACCS_dig" : 139,
    "FG" : "OH"
}


def get_MACCS_from_sm(sm):
    mol = Chem.MolFromSmiles(sm)
    fp = MACCSkeys.GenMACCSKeys(mol)
    mol_MACCS = fp.ToBitString()
    return mol_MACCS

FG_to_chk = alcohol


# OH_subset = []
non_OH_subset = []

for entry in db_dict:
    entry_sm = entry["SMILES"]
    if type(entry_sm) is str:
        entry_MACCS = get_MACCS_from_sm(entry_sm)
        FG_dig = FG_to_chk["MACCS_dig"]
        if entry_MACCS[FG_dig] == str(1):
            entry[FG_to_chk["FG"]] = "True"
            # OH_subset.append(entry)
        else:
            entry[FG_to_chk["FG"]] = "False"
            non_OH_subset.append(entry)
    else:
        entry[FG_to_chk["FG"]] = -1


# FG_filt_db = pd.DataFrame.from_dict(data = db_dict)
# FG_filt_db.to_csv("alcohol_chk.csv", index = None)

# OH_db = pd.DataFrame.from_dict(data = OH_subset)
# OH_db.to_csv("OH_subset.csv")
# OH_cand = pd.DataFrame()
# OH_cand["CAS"] = OH_db["CAS"]
# OH_cand["Solvent"] = OH_db["Name"]
# OH_cand.to_json("OH_candidates.json", orient = "records")

non_OH_db = pd.DataFrame.from_dict(data = non_OH_subset)
non_OH_db.to_csv("non_OH_subset.csv")
non_OH_cand = pd.DataFrame()
non_OH_cand["CAS"] = non_OH_db["CAS"]
non_OH_cand["Solvent"] = non_OH_db["Name"]
non_OH_cand.to_json("non_OH_candidates.json", orient = "records")




        
    