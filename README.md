# SolvPred (v2.0)
Last update: 15/01/2023

## Introduction

As one of the [HSP toolkits](https://github.com/xueannafang/HSP_toolkit_docs/blob/main/hsp_tool_general_intro.md), SolvPred is a solvent selection assisstant aiming at providing multi-solvent suggestion based on target Hansen solubility parameters (HSP).


## What's new in this version?

 - Exclusively python/json-based. (A simple user interactive interface has been included. No longer require Microsoft Excel or Jupyter Notebook. Less dependent on operating system.)
 - More physical/chemical properties have been included in the database (molar volume, molecular weight, boiling point, immiscible solvent pairs, molar heat of evaporation, viscosity and related measuring temperatures based on avilable data on PubChem).
 - Auto check the validity of user input CAS (as well as the existence in database).
 - Auto check the validity of target HSP. Filter impossible missions, i.e., those targets locating outside the region connected by all the solvent candidates in the Hansen space.
 - Allow flexible control of acceptable error in each sub HSP.
 - Allow temperature control and include temperautre-dependent correction of HSP.
 - Advanced filtration step based on miscibility and boiling point has been included.

 ## Limitations

   - Some categories may have a limitation of avilable data, which will be labelled as -1 or None in the database.
   - The temperature control function is only based on correcting HSP in this version. Properties applied in advanced filtration (e.g., miscibility) may also be temperature-dependent but no direct correction is applied in this version.
   - If user manually edited the database and add additional solvents without available HSP, the temperature correction for data-missing group will be disabled and corresponding solvent will be removed from database after temperature updating check step.


## Data source

  - Phyciscal/Chemical data of solvents in the database were collected from PubChem.
  - HSP data remain same as [last version](https://github.com/xueannafang/hsp_toolkit_prototype), as collected from HSP handbook (ref 1).

## How to use (to be updated)

### Before start

Required packages:

- numpy, scipy.linalg, json, math, itertools, os, datetime


### Run SolvPred 2.0

```
python solv_pred_main.py
```


## References

1. C. Hansen, Hansen Solubility Parameters – A user’s handbook, 2nd edition, 2011.
2. X. Fang, C. F.J. Faul, N. Fey, E. Gale, SolvPred - A python toolkit to predict multi-solvent combinations with target Hansen solubility parameters (manuscript in preparation).


## Disclaimer

  - SolvPred is under continous tests and improvement. The output only provide suggestion. Results may vary with multi factors in complicated situations. It is the users responsbility to manuallay check the exact experimental performance in different scenarios.

 ---

This project is licensed under [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html).
