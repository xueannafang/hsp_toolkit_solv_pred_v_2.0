import pandas as pd

#full db xlsx
db_xlsx_name = "db_mis.xlsx"

#special FG

#Cl

ele_Cl = {
    "ele" : "Cl",
    "title" : "chlorinated"
}


ele_F = {
    "ele" : "F",
    "title" : "fluorinated"
}




db_df = pd.read_excel(db_xlsx_name, na_values = -1)
db_dict = db_df.to_dict(orient="records")

ele_to_chk = ele_F

green_subset = []

for entry in db_dict:
    entry_sm = entry["SMILES"]

    if type(entry_sm) is str:
        if ele_to_chk["ele"] in entry_sm:
            entry[ele_to_chk["title"]] = "True"
        else:
            entry[ele_to_chk["title"]] = "False"
            green_subset.append(entry)
    else:
        entry[ele_to_chk["title"]] = -1
        green_subset.append(entry)

green_db = pd.DataFrame.from_dict(data = green_subset)
green_db.to_csv("non_fluorinated_subset.csv")
green_cand = pd.DataFrame()
green_cand["CAS"] = green_db["CAS"]
green_cand["Solvent"] = green_db["Name"]
green_cand.to_json("non_fluorinated_candidates.json", orient = "records")



# db_checked = pd.DataFrame.from_dict(data = db_dict)
# db_checked.to_csv("db_filtered.csv")




    
    



