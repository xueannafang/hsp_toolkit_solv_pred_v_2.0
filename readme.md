# Solvent Predictor v2.0

## Key updates
- Database (db.xlsx) spreadsheet has been updated into .json format.
- Database has been renamed as db_mis.json.
- More parameters of solvents, including boiling point (degree C), molecular weight (g mol-1),  viscosity (mPa s), temperature of viscosity (degree C), heat of vaporisation (kJ mol-1) at temperature (hov_temp, degree C), SMILES, synonyms and alias, notes and other comments, have been included in the database. (Parameters were collected from [PubMed](https://pubchem.ncbi.nlm.nih.gov/); "-1" means data unavailable from PubMed.)
- Updated immiscible or slightly soluble combinations in "ims_idx". Miscibility check has been included in the toolkit.
