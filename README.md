# SolvPred (v2.0)
Last update: 12/01/2023

## Introduction

SolvPred is a solvent selection assisstant aiming at providing multi-solvent suggestion based on target Hansen solubility parameters (HSP)

## What's new in this version?

 - Exclusively python/json-based. (A simple user interactive interface has been included. No longer require Microsoft Excel or Jupyter Notebook. Less dependent on operating system.)
 - More physical/chemical properties has been included in the database (molar volume, molecular weight, boiling point, immiscible solvent pairs, molar heat of evaporation, viscosity and related measuring temperatures based on avilable data on PubChem).
 - Auto check the validity of user input CAS (as well as the existence in database).
 - Auto check the validity of target HSP. Filter impossible missions, i.e., those targets locating outside the region connected by all the solvent candidates in the Hansen space.
 - Allow flexible control of acceptable error in each sub HSP.
 - Allow temperature control and include temperautre-dependent correction of HSP.
 - The format of database and default candidate lists has been updated to json.
 - Advanced filtration step based on miscibility and boiling point has been included.

 
 ## Disclaimer

  - Phyciscal/Chemical data of solvents in the database were collected from PubChem.
  - Some categories may have a limitation of avilable data, which will be labelled as -1 or None in the database.
  - The temperature control function is only based on correcting HSP in this version. Properties applied in advanced filtration (e.g., miscibility) may also be temperature-dependent but no direct correction is applied in this version.
  - SolvPred only provides suggestion. Results may vary with multi factors in complicated situations. It is the users responsbility to manuallay check the exact experimental performance in different scenarios.


## Acknowledgement

 This work is developed by:
 - Xue Fang (School of Chemistry, University of Bristol)

 with the instruction from:
 - Prof Charl FJ Faul (School of Chemistry, University of Bristol)
 - Prof Natalie Fey (School of Chemistry, University of Bristol)
 - Dr Ella Gale (School of Chemistry, University of Bristol)

 and the following people providing techniqual advice:
 - Jillisa Thompson (School of Chemistry, University of Bristol)
 - Bo Gao (School of Physics, University of Bristol)

 The development and communication of this work are funded by:
 - University of Bristol - Chinese Scholarship Council Joint Scholarship
 - Royal Society of Chemistry Researcher Development Grants (2022)
