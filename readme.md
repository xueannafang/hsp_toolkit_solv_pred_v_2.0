# Solvent Predictor v2.0

## Key updates
- Database (db.xlsx) spreadsheet has been updated into .json format.
- Database (db.xlsx) has been renamed as db_mis.json.
- More parameters of solvents, including boiling point ( $^{\circ} C$), molecular weight (g mol $^{-1}$),  viscosity (mPa s) at temperature **vis_temp** ( $^{\circ} C$), heat of vaporisation (kJ mol $^{-1}$) at temperature **hov_temp** ( $^{\circ} C$), SMILES, synonyms and alias, notes and other comments, have been included in the database. (Parameters were collected from [PubChem](https://pubchem.ncbi.nlm.nih.gov/); "-1" means data unavailable.)
- Updated immiscible or slightly soluble combinations in "ims_idx". Miscibility check has been included in the toolkit.
