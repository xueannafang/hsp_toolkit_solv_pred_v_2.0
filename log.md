# Solvent Predictor v2.0


## TODO (03/01/2022)
 - check the logic of quit check (finish check - unboundlocalerror: to_continue_finish referenced before assignment.
 - test the error input
 - include matrix calculation and filtration step


## updates (30/12/2022)

- db_mis.json has been renamed as db_solv_pred_v2.json
- UI included
- separate different functions
- db init
- remove func included, with filtration check


## updates (26/12/2022)
- Database (db.xlsx) spreadsheet has been updated into .json format.
- Database (db.xlsx) has been renamed as db_mis.json.
- More parameters of solvents, including boiling point ( $^{\circ} C$), molecular weight (g mol $^{-1}$),  viscosity (mPa s) at temperature **vis_temp** ( $^{\circ} C$), heat of vaporisation (kJ mol $^{-1}$) at temperature **hov_temp** ( $^{\circ} C$), SMILES, synonyms and alias, notes and other comments, have been included in the database. (Parameters were collected from [PubChem](https://pubchem.ncbi.nlm.nih.gov/); "-1" means data unavailable.)
- Updated immiscible or slightly soluble combinations in "ims_idx". Miscibility check has been included in the toolkit.

## TODO
- django and SQL database
- user selection (solvent candidate)
- default candidate list
- user input error handling
- temperature correction
- output style