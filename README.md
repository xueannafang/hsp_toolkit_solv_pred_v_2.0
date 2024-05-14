# SolvPred (v2.0)
Last update: 30/05/2023

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
 - A checklist for candidate selection criteria in different situations is proposed.


## Data source

  - Physical/Chemical data of solvents in the database were collected from [PubChem](https://pubchem.ncbi.nlm.nih.gov/).
  - HSP data remain same as [last version](https://github.com/xueannafang/hsp_toolkit_prototype), as collected from HSP handbook (ref 1).

## How to use?

### Before start

#### Required packages:

- [numpy](https://numpy.org/), [scipy.linalg](https://docs.scipy.org/doc/scipy/reference/linalg.html), [json](https://docs.python.org/3/library/json.html), [math](https://docs.python.org/3/library/math.html), [itertools](https://docs.python.org/3/library/itertools.html), [os](https://docs.python.org/3/library/os.html), [datetime](https://docs.python.org/3/library/datetime.html).


#### Auto-loaded files:

*Must be stored under current working directory. DO NOT rename or remove!*

##### database (db_solv_pred_v2.json)

Database in this version contains property information for 249 solvents.

Example structure of one entry:

```
{
  "No.": 2,
  "CAS": "64-19-7",
  "Name": "Acetic acid",
  "D": 14.5,
  "P": 8,
  "H": 13.5,
  "Mole_vol": "57.1",
  "ims_idx": "139;190;39",
  "bp": 117,
  "mw": 60.05,
  "viscosity": 1.056,
  "vis_temp": 25,
  "heat_of_vap": 23.7,
  "hov_temp": 117.9,
  "SMILES": "CC(=O)O",
  "synonyms": "ethanoic acid;Ethylic acid;Vinegar acid"
 }
```

Each explained in the comment below:

```
{
  "No.": 2, # idx of entry in the database. In the last version, this is called "no_db" or "db_no"
  "CAS": "64-19-7", # CAS No. of this entry
  "Name": "Acetic acid", # solvent name.
  "D": 14.5, # dispersion term of HSP, unit: MPa^(1/2).
  "P": 8, # dipolar term of HSP, unit: MPa^(1/2).
  "H": 13.5, # hydrogen bond term of HSP, unit: MPa^(1/2).
  "Mole_vol": "57.1", # molecular volume, unit: cm^3 mol^(-1).
  "ims_idx": "139;190;39", # solvent index that has immiscible record with the current solvent on PubChem.
  "bp": 117, # boiling point, unit: degree C.
  "mw": 60.05, # molecular weight, unit: g mol^(-1).
  "viscosity": 1.056, # viscosity, unit: mPas or cP.
  "vis_temp": 25, # temperature of viscosity recorded, unit: degree C.
  "heat_of_vap": 23.7, # molar heat of evaporation, unit: kJ mol^(-1).
  "hov_temp": 117.9, # temperature of molar heat of evaporation is recorded, unit: degree C.
  "SMILES": "CC(=O)O", # structure of current solvent.
  "synonyms": "ethanoic acid;Ethylic acid;Vinegar acid" # synonyms - if helpful for user to search name, but not recommended.
 }
```


##### default solvent candidate list (default_solv_candidate.json)

A list of solvent cas and name dictionaries, serving as candidates (also called "solvent pool" in the previous version.)

Take one entry as an example:

```
{
  "CAS": "121-44-8",
  "Solvent": "Triethylamine"
 }
```

Note that only "CAS" is useful for further calculation. Solvent name ("Solvent") does not matter too much, just as a reference.

Please check here with the document for candidate selection checklist.



### Run SolvPred

Go to terminal. Activate the correct environment (i.e., with required packages pre-installed). Go to the correct directory.

```
python solv_pred_main.py
```

You will see:

```
2023-01-22  10:15:54
SolvPredictor v 2.0 
 (License: GPL-3.0) 

Loading database and default candidate list...
Done. 

Please follow the instruction to continue:    
=========================
Step 1: Generate solvent candidate list:
 You can select to use the default list (recommend) or manually input the CAS No. for each solvent.

Please select the method to construct solvent candidate list:
 [d] - default (recommend - the default list can still be edited in the following steps)
 [m] - manual
 [v] - visualise default solvent list
 [q] - quit

```

### Step 1: candidate list construction

The first step is to construct solvent candidate list. We recommend to first load the *default* list (press [d]) and modify on it if necessary.

You can view the default solvent list by pressing [v]. You will see:

```
v
The default solvent candidates include the following solvents: 

{'CAS': '121-44-8', 'Solvent': 'Triethylamine'}
{'CAS': '109-66-0', 'Solvent': 'Pentane'}
{'CAS': '1330-20-7', 'Solvent': 'Xylene'}
{'CAS': '60-29-7', 'Solvent': 'Glycerol'}
{'CAS': '109-99-9', 'Solvent': 'Tetrahydrofuran'}
{'CAS': '110-54-3', 'Solvent': 'Hexane'}
{'CAS': '79-01-6', 'Solvent': 'Trichloroethylene'}
{'CAS': '142-82-5', 'Solvent': 'Heptane'}
{'CAS': '110-82-7', 'Solvent': 'Cyclohexane'}
{'CAS': '108-88-3', 'Solvent': 'toluene'}
{'CAS': '71-43-2', 'Solvent': 'benzene'}
{'CAS': '108-90-7', 'Solvent': 'chlorobenzene'}
{'CAS': '75-09-2', 'Solvent': 'methylene dichloride'}
{'CAS': '75-65-0', 'Solvent': 't-butyl alcohol'}
{'CAS': '67-63-0', 'Solvent': '2-propanol'}
{'CAS': '141-78-6', 'Solvent': 'ethyl acetate'}
{'CAS': '123-91-1', 'Solvent': 'dioxane'}
{'CAS': '71-23-8', 'Solvent': '1-propanol'}
{'CAS': '67-64-1', 'Solvent': 'acetone'}
{'CAS': '110-86-1', 'Solvent': 'pyridine'}
{'CAS': '64-17-5', 'Solvent': 'ethyl alcohol'}
{'CAS': '68-12-2', 'Solvent': 'dimethylformamide'}
{'CAS': '67-56-1', 'Solvent': 'methanol'}
{'CAS': '108-95-2', 'Solvent': 'phenol'}
{'CAS': '75-05-8', 'Solvent': 'acetonitrile'}
{'CAS': '67-68-5', 'Solvent': 'dimethylsulfoxide'}
{'CAS': '74-87-3', 'Solvent': 'Methylcyclohexane'}
{'CAS': '67-66-3', 'Solvent': 'chloroform'}
{'CAS': '616-47-7', 'Solvent': 'NMI'}
{'CAS': '108-32-7', 'Solvent': 'Propylene carbonate'}
{'CAS': '91-22-5', 'Solvent': 'Quinoline'}
{'CAS': '108-39-4', 'Solvent': 'm-Cresol'}
{'CAS': '108-67-8', 'Solvent': 'Mesitylene'}
{'CAS': '872-50-4', 'Solvent': 'N-Methyl-2-pyrrolidone'}
{'CAS': '56-81-5', 'Solvent': 'Glycerol'}
{'CAS': '127-19-5', 'Solvent': 'N,N-dimethylacetamide'}
Please select the method to construct solvent candidate list:
 [d] - default (recommend - the default list can still be edited in the following steps)
 [m] - manual
 [v] - visualise default solvent list
 [q] - quit

```

#### Default

After selecting the default list, you have a chance to remove any unwanted solvents:

```
d
You have selected to use the default solvent candidate list.
Solvent candidate list has been generated successfully.
Do you want to remove any solvent?

[y/n]:
```

If you am happy with the default list, press [n] to process.

If you want to remove some candidates, which, may be unavailable in your lab or you don't like certain properties, press [y] to enter CAS of unwanted solvents. Press [enter] to finish.



```
Do you want to remove any solvent?

[y/n]: y
Please enter the CAS No. of solvent candidate 1 : 108-39-4
Please enter the CAS No. of solvent candidate 2 : 
Have all the solvent candidates been added?
[y/n]:
```

If you are doing solvent replacement, remember to remove the solvent to be replaced at this step. (Otherwise your output will include all the combination of 100% solvent to be replaced + 0% the rest available on the candidate list.)

For example, if you want to replace DMF, you need to input the cas No. of DMF (68-12-2, which can be searched in default_solv_candidate.json) in this removal step.

*Make sure you enter the correct CAS (with correct format, on both the candidate list and database. (This version will auto check before removing anything from the candidate list and pop up warning if any input is invalid.)*

You will then be asked again whether you want to remove any solvent. Press [n] to continue.

*SolvPred* will then return the list of solvents to be removed from the current list and check if they are removable from current list and database.

```
Do you want to remove any solvent? 

[y/n]: n
Continue? 
[y/n]: y
The following solvents will be removed: 
['108-39-4']
Checking if any solvent is not on the candidate list...
Done.
 Checking if any solvent is not in the database...
Done.
```

Once this is done. You can submit by selecting [y].

(If you did not edit the default list, you will directly go to this step.)

```
Submit?
[y/n]: y
```

The candidates will be presented to you:

```
The following solvents will be considered as candidates: 
['67-66-3', '108-95-2', '108-32-7', '121-44-8', '110-86-1', '74-87-3', '616-47-7', '1330-20-7', '75-05-8', '67-68-5', '141-78-6', '75-09-2', '108-90-7', '142-82-5', '67-63-0', '60-29-7', '123-91-1', '79-01-6', '68-12-2', '110-54-3', '109-99-9', '75-65-0', '872-50-4', '127-19-5', '56-81-5', '108-67-8', '67-64-1', '110-82-7', '71-23-8', '109-66-0', '91-22-5', '67-56-1', '108-88-3', '64-17-5', '71-43-2']    
Candidate list has been successfully generated:
['Chloroform', 'Phenol', 'Propylene carbonate', 'Triethylamine', 'Pyridine', 'Methyl chloride', '1-Methylimidazole', 'm-Xylene', 'Acetonitrile', 'Dimethyl sulfoxide', 'Ethyl acetate', 'Methylene dichloride', 'Chlorobenzene', 'Heptane', '2-Propanol', 'Diethyl ether', '1,4-Dioxane', 'Trichloroethylene', 'Dimethylformamide', 'Hexane', 'Tetrahydrofuran', 't-Butyl Alcohol', 'Methyl-2-pyrrolidone', 'N,N-dimethylacetamide', 'Glycerol', 'Mesitylene', 'Acetone', 'Cyclohexane', '1-Propanol', 'Pentane', 'Quinoline', 'Methanol', 'Toluene', 'Ethanol', 'Benzene']
```

#### Manual

Back to the start, if you choose to manually add solvent candidates. Press [m] and add CAS No. based on your preference.

```
Please follow the instruction to continue: 
=========================
Step 1: Generate solvent candidate list: 
 You can select to use the default list (recommend) or manually input the CAS No. for each solvent.

Please select the method to construct solvent candidate list: 
 [d] - default (recommend - the default list can still be edited in the following steps) 
 [m] - manual 
 [v] - visualise default solvent list
 [q] - quit
m
Please submit CAS No. of solvents to be considered as candidates. Add one solvent at one time. Press [enter] to continue.
Please enter the CAS No. of solvent candidate 1 : 121-44-8
Please enter the CAS No. of solvent candidate 2 : 109-66-0
Please enter the CAS No. of solvent candidate 3 : 109-99-9
Please enter the CAS No. of solvent candidate 4 : 
Have all the solvent candidates been added?
[y/n]: y
Solvent candidate list has been generated successfully.
Do you want to remove any solvent?

[y/n]: n
Continue? 
[y/n]: y
```

Again, *SolvPred* will quickly look at your candidates in case anything is beyond its control.

If everything goes smoothly, you will see the message below:

```
Checking if any solvent is not on the candidate list...
Done.
 Checking if any solvent is not in the database...
Done.
```

Before submission, you will have a final chance to edit the candidate list:

```
Submit?
[y/n]:
```

In the above example, you will see all the valid candidates before you go to the next step:

```
y
The following solvents will be considered as candidates: 
['121-44-8', '109-66-0', '109-99-9']
Candidate list has been successfully generated:
['Triethylamine', 'Pentane', 'Tetrahydrofuran']
```

#### Final edit before submission

If you choose [n] during the submission confirm, you will still be able to edit your candidate list by adding[a] or removing[rm] any entry. 

```
Submit?
[y/n]: n
Please select one of the following options: 
[a] - add CAS
[rm] - remove CAS
[v] - visualise current candidate list
[s] - submit
[q] - quit
```

Press [v] can see current candidate list.

```
v
Current candidate list:
['108-90-7', '79-01-6', '110-54-3', '127-19-5', '91-22-5', '872-50-4', '108-39-4', '67-68-5', '108-88-3', '64-17-5', '108-32-7', '68-12-2', '109-99-9', '110-82-7', '67-56-1', '75-09-2', '1330-20-7', '67-66-3', '616-47-7', '121-44-8', '75-05-8', '71-43-2', '67-63-0', '60-29-7', '109-66-0', '71-23-8', '67-64-1', '75-65-0', '141-78-6', '56-81-5', '74-87-3', '123-91-1', '142-82-5', '108-67-8', '110-86-1', '108-95-2']
Continue?
[y/n]:
```

Please note, after this step, the candidate list will not be editable.





### Step 2: Specify parameters

You will now see:

```
=========================

Step 2: Specify parameters.
 Please follow the instruction to specify the
 - Maximum number of solvents (n) to be included in each combination (default = 2);
 - Highest acceptable error of HSP (tol_err) of the predicted combination (default = 0.5);
 - Lowest acceptable concentration (tol_conc) of each predicted solvent component (default = 0.01).
 - Target HSP (target D, P, H).
 Temperature (default = 25 degree C).

[t] - set a different temperature
[c] - continue as room temperature (25 degree c).
[q] - quit

```

This step requires you to specify all the calculation parameters (details summarised below).

#### target_d: Target D to be achieved.

- unit: MPa^(1/2)
- value example: 18
- requirement: non-negative float; must fall in the range of (min D, max D) of all solvent candidates. 

(*SolvPred* will auto check the validity of the target. Here the basic is, your target point must be surrounded by all the candidates, since you have to attribute your candidate with a positive concentration. Therefore, if any target falls beyond the interval quantified by all the solvent candidates, that mission would be impossible.)

#### target_p: Target P to be achieved.

- unit: MPa^(1/2)
- value example: 3
- requirement: non-negative float; must fall in the range of (min P, max P) of all solvent candidates.


#### target_h: Target H to be achieved.

- unit: MPa^(1/2)
- value example: 2
- requirement: non-negative float; must fall in the range of (min H, max H) of all solvent candidates.

#### err_d: maximum error of D.

- unit: MPa^(1/2)
- value example: 0.5
- default: 0.5
- requirement: non-negative float.

#### err_p: maximum error of P.

- unit: MPa^(1/2)
- value example: 0.5
- default: 0.5
- requirement: non-negative float.

#### err_h: maximum error of H.

- unit: MPa^(1/2)
- value example: 0.5
- default: 0.5
- requirement: non-negative float.

#### n: maximum number of solvents in each combination.

- value example: 2
- default: 2
- requirement: n >=2, integer, less than total number of candidates. Recommend to be 2 or 3.

#### tol_conc: lowest acceptable concentration.

Any prediction with solvent whose concentration below this value will be determined as "redundant results". This is to include the practical experimental situation, for some extremely low conc. component, their contribution towards final HSP would be very limited but still creating complexity to the experiment operation. Therefore, we set this parameter to filter out unnecessary results.

- value example: 0.01 (which means conc. below 1% is regarded as redundant.)
- default: 0.01
- requirement: float in the range of (0, 1) (*Please DO NOT enter percentage format.*).

#### target_temp: target temperature of prediction.

Applying a different temperature will update all D, P, H in the database.

Temperature correction is based on the following formula (ref Hansen user book):

temp_corr_d = ori_d * exp(-1.25 * tml_expn_coeff * delta_temp)

temp_corr_p = ori_p * exp(-0.5 * tml_expn_coeff * delta_temp)

temp_corr_h = ori_h * exp(-(0.00122 + 0.5 * tml_expn_coeff) * delta_temp)

where

the thermal expansion coefficient (tml_expn_coeff) = 0.0007, unit: K^(-1).

delta_temp is the temperature difference between target temp and room temp (25 degree C).


You can decide to edit the temperature by pressing [t] or continue as room temperature [c].

If you choose to edit the temperature (for example, for the purpose of selecting a correct condition matching your reaction), you will then see:

```
t
Please enter the target temperature (in degree C):
``` 


Enter the desired temperature (60 in this example; the unit is degree c):

```
Please enter the target temperature (in degree C): 60
Temperature has been set as: 60
Applying temperature correction for standard HSP...
Database HSP temperature correction done.
```

Now all the HSP in the database has been corrected based on your setting.

You will then see the following instruction (If you continue as room temperature in the last step, you will go to this step directly.):

```
Set parameters:
[d] - use default settings for all parameters.     
[m] - manually set parameters.
```

In this step, you need to determine whether to adapt default settings for all the parameters of *err_d, p, h*, *tol_conc*, *n* or not.

Enter [d] for default settings:

```
d
Default parameters will be applied.
[n, tol_err_d, tol_err_p, tol_err_h, tol_conc] : [2, 0.5, 0.5, 0.5, 0.01]
```

Alternatively, enter [m] to manually set up these parameters following the instruction:

Specify *n*:

```
m
Please specify parameters:
n is the maximum number of solvents involved in each prediction.
Must be a postivie integer >= 2. (recommend to be 2 or 3)
Please specify n:
```

Specify error for D: 

```
tolerance of error is the highest acceptable absolute error of HSP from the predicted solvent mixture. 
 Must be a positive float.
Please specify tolerance of error for dispersion term (tol_err_D):
```

And same for error of P and H:

```
Please specify tolerance of error for dispersion term (tol_err_D): 0.5
Please specify tolerance of error for dipolar term (tol_err_P): 0.2
Please specify tolerance of error for hydrogen bond term (tol_err_H): 0.3
```

(In this example, we set them as 0.5, 0.2, 0.3, respectively.)

Now specify the *tol_conc*:

```
lowest acceptable concentration is the threshold of predicted solvent concentration below which will be filtered out. 
Must be a float between 0 and 1.

Please specify lowest acceptable concentration:
```

We set it as 0.02 for an example. You now need to confirm the settings:

```
Please specify lowest acceptable concentration: 0.02
n, tol_err, tol_conc have been specified as: 
[2, 0.5, 0.2, 0.3, 0.02]
Continue?
[y/n]:
```

Note that in this step, if any parameter is invalid, *SolvPred* will ask you to re-input a valid number.

Now specify target D, P, H:

```
target d, p, h are target HSPs to be achieved. 
 Must be non-negative float.
Please specify the target of dispersion term (target D):
```

Note if you input a set of target that is beyond the capacity of your candidates, *SolvPred* will remind you of the constraints and ask you to re-consider your target HSP:

See this example, we ask *SolvPred* to give us a 36 for target D:

```
Please specify the target of dispersion term (target D): 36
Please specify the target of dipolar term (target P): 2
Please specify the target of hydrogen bond term (target H): 3
target d, target p, target h have been specified as: 
['36', '2', '3']
Continue?
[y/n]: y
```

It will validate your goal:

```
Validating parameters...
Validating n...
Validation of n is done.
Validating target HSP...
```

And tell you target D is an impossible task:

```
Target D is not achievable.
Target D must be in the interval of 14.062668321565182 to 19.396783891814046
Target P validation done.
Target H validation done.
```

You gonna make sure target D falls in the interval suggested above (in this case, 14.06 and 19.40).

Note that this issue coming out depending on the selection of solvent candidates:

In this example, all the dispersion term (D) of candidates fall between (14.06 and 19.40). This is a hard-to-change fact that common lab solvents we put on the default candidate list can only achieve these values.

(We will address this issue again in *MLoc v2.0* and illustrate the impact of this issue towards HSP prediction for materials.)

Now you have two options, either update your target (enter [r]), or find more candidates ([a]) that may expand the achievable target in the Hansen space. (NOTE THAT THE SECOND OPTION IS STILL UNDER TEST.)

(This would be case dependent, for P and H term, expanding candidates may help, but D would be a bit tricky.)

```
Please choose to reset the required parameters or add more solvent candidates.
 [r] - reset
 [a] - add
 [q] - quit
```

We would go for the easier case (reset target) for simplicity. (And this is also more recommended. You can of course play around the other option, but it may be a bit tough as you need to be clear of the candidate HSP before including them in the calculation, which might not be a quick job.)

Let's go for 18, 3, 2 for target d, p, h now:

```
r
Please reset target HSP.
target d, p, h are target HSPs to be achieved.
 Must be non-negative float.
Please specify the target of dispersion term (target D): 18
Please specify the target of dipolar term (target P): 3
Please specify the target of hydrogen bond term (target H): 2
target d, target p, target h have been specified as: 
['18', '3', '2']
Continue?
[y/n]: y
```

This is a possible task and successfully passed the ckeck:

```
Validating parameters...
Validating n...
Validation of n is done.
Validating target HSP...
Target D validation done.
Target P validation done.
Target H validation done.
Parameter selection done.
```

### Step 3: carry out main calculation process

Now *SolvPred* will generate a perturbated HSP matrix based on the absolute target. This is to apply a +/- 0.1 fluctuation (reflected by a Gaussian random number) to your target. (Otherwise you may receive a prediction with an accuarcy of the 16th decimal place, that, significantly shrinks the valid results. In addition, this step is to serve as a statistic stability check to filter out some unstable results, say, a tiny deviation in concentration, which is common in experimental operation, will lead to a large deviation in resulting HSP.)

```
Generating perturbated target HSP matrix...
Done.
```

So far, the basic calculation has been finished.

You may see (and only see, hopefully) the time, date and version, license info again on your terminal:

```
2023-01-22  10:15:54
SolvPredictor v 2.0 
 (License: GPL-3.0)
```

(A congrats if nothing containing pathway poping out - in that case, please go for the suggested path, which is the failed-calculation log, to check what's going wrong there.)

In the above example, we can get a list of successful predictions.

If you go to your current working directory, you can see a new folder named "log". We briefly look at what is already there:

(Note that the 14-digit suffix is the date and time when this calculation was carried out, so as to avoid accidental overwriting of your previous outputs.)

#### log_success_01222023101554.txt

This one contains the majority of things you are interested in.

The first part is the version info and input parameters:

```
===============================
SolvPredictor v 2.0 
 (License: GPL-3.0) 

10:15:54
2023-01-22
===============================

Target D /MPa^(1/2): 
18

Target P /MPa^(1/2): 
3

Target H /MPa^(1/2): 
2

Temperature /degree c: 
60.0

Number of candidates in each combination (n): 
2

Tolerance of error for D /MPa^(1/2): 
0.5

Tolerance of error for P /MPa^(1/2): 
0.2

Tolerance of error for H /MPa^(1/2): 
0.3

Lowest concentration limit: 
0.02

Candidate cas: 
['67-66-3', '108-95-2', '108-32-7', '121-44-8', '110-86-1', '74-87-3', '616-47-7', '1330-20-7', '75-05-8', '67-68-5', '141-78-6', '75-09-2', '108-90-7', '142-82-5', '67-63-0', '60-29-7', '123-91-1', '79-01-6', '68-12-2', '110-54-3', '109-99-9', '75-65-0', '872-50-4', '127-19-5', '56-81-5', '108-67-8', '67-64-1', '110-82-7', '71-23-8', '109-66-0', '91-22-5', '67-56-1', '108-88-3', '64-17-5', '71-43-2']

Candidate solvents: 
['Chloroform', 'Phenol', 'Propylene carbonate', 'Triethylamine', 'Pyridine', 'Methyl chloride', '1-Methylimidazole', 'm-Xylene', 'Acetonitrile', 'Dimethyl sulfoxide', 'Ethyl acetate', 'Methylene dichloride', 'Chlorobenzene', 'Heptane', '2-Propanol', 'Diethyl ether', '1,4-Dioxane', 'Trichloroethylene', 'Dimethylformamide', 'Hexane', 'Tetrahydrofuran', 't-Butyl Alcohol', 'Methyl-2-pyrrolidone', 'N,N-dimethylacetamide', 'Glycerol', 'Mesitylene', 'Acetone', 'Cyclohexane', '1-Propanol', 'Pentane', 'Quinoline', 'Methanol', 'Toluene', 'Ethanol', 'Benzene']
```

We dumped the full calculation log in a json file named after  "calc_log_bsc_chk_",  whose path is stored in the next part of successful log output:

```
Calculation log path: 
C:\Users\sh19129\OneDrive - University of Bristol\Documents\MyProject\ML\HSP_python\calculation\cal_20221227_solv_pred_v2\hsp_toolkit_solv_pred_v_2.0\log\calc_log_bsc_chk_01222023101554.json

```

The next part is the results:

```
===============================
Results: 
===============================

Group 1 : 

solvent 1 : Propylene carbonate (108-32-7) 
concentration 1 :  9.47% 

solvent 2 : Toluene (108-88-3) 
concentration 2 :  90.53% 

calculated D /MPa^(1/2): 17.640788087782173
calculated P /MPa^(1/2): 2.9357929244636503
calculated H /MPa^(1/2): 2.0812967786641057
error of D /MPa^(1/2): -0.3592119122178268
error of P /MPa^(1/2): -0.06420707553634974
error of H /MPa^(1/2): 0.08129677866410567


********
Group 2 : 

solvent 1 : Propylene carbonate (108-32-7) 
concentration 1 :  16.91% 

solvent 2 : Benzene (71-43-2) 
concentration 2 :  83.09% 

calculated D /MPa^(1/2): 18.10739983538574
calculated P /MPa^(1/2): 3.0062706660797662
calculated H /MPa^(1/2): 2.2291355259840344
error of D /MPa^(1/2): 0.10739983538573838
error of P /MPa^(1/2): 0.0062706660797662295
error of H /MPa^(1/2): 0.22913552598403442


********
Group 3 : 

solvent 1 : Pyridine (110-86-1) 
concentration 1 :  32.62% 

solvent 2 : Mesitylene (108-67-8) 
concentration 2 :  67.38% 

calculated D /MPa^(1/2): 17.773456056552682
calculated P /MPa^(1/2): 2.835511627256973
calculated H /MPa^(1/2): 2.2042847617417625
error of D /MPa^(1/2): -0.22654394344731799
error of P /MPa^(1/2): -0.16448837274302708
error of H /MPa^(1/2): 0.20428476174176247


********
Group 4 : 

solvent 1 : m-Xylene (1330-20-7) 
concentration 1 :  34.80% 

solvent 2 : Chlorobenzene (108-90-7) 
concentration 2 :  65.20% 

calculated D /MPa^(1/2): 17.95449539667164
calculated P /MPa^(1/2): 3.113363706209861
calculated H /MPa^(1/2): 2.2553543627245842
error of D /MPa^(1/2): -0.045504603328360815
error of P /MPa^(1/2): 0.11336370620986091
error of H /MPa^(1/2): 0.2553543627245842


********
Group 5 : 

solvent 1 : Dimethyl sulfoxide (67-68-5) 
concentration 1 :  17.37% 

solvent 2 : Mesitylene (108-67-8) 
concentration 2 :  82.63% 

calculated D /MPa^(1/2): 17.524490650842214
calculated P /MPa^(1/2): 2.8140266478430767
calculated H /MPa^(1/2): 2.1462982015123093
error of D /MPa^(1/2): -0.475509349157786
error of P /MPa^(1/2): -0.18597335215692334
error of H /MPa^(1/2): 0.14629820151230932


********
Group 6 : 

solvent 1 : Chlorobenzene (108-90-7) 
concentration 1 :  56.54% 

solvent 2 : Toluene (108-88-3) 
concentration 2 :  43.46% 

calculated D /MPa^(1/2): 18.005452235642807
calculated P /MPa^(1/2): 3.002650279283027
calculated H /MPa^(1/2): 1.8930649467880154
error of D /MPa^(1/2): 0.005452235642806613
error of P /MPa^(1/2): 0.0026502792830269684
error of H /MPa^(1/2): -0.1069350532119846


********
Group 7 : 

solvent 1 : Chlorobenzene (108-90-7) 
concentration 1 :  71.73% 

solvent 2 : Benzene (71-43-2) 
concentration 2 :  28.27% 

calculated D /MPa^(1/2): 18.262437183814317
calculated P /MPa^(1/2): 3.046811966163837
calculated H /MPa^(1/2): 1.8930649467880154
error of D /MPa^(1/2): 0.2624371838143169
error of P /MPa^(1/2): 0.04681196616383687
error of H /MPa^(1/2): -0.1069350532119846


********

```

#### calc_log_bsc_chk_01222023101554.json

This json file contains the full calculation log (including what has been filtered out and the reason why they have been filtered out).

We take the first entry as an example:

```
{
  "idx": 0, "cas_comb": ["67-66-3", "108-95-2"], 
  "conc": [[[1.4414674981149098], [-0.39069270146057705]], [[0.013704739565376992], [0.012101233403607914]]], 
  "err": [[[0.06547142600175924], [-0.8699042557516072], [0.2748449378482521], [0.05077479665433273]], [[0.007840492471920472], [0.09953634088029777], [0.03144069036004137], [0.00475221830136207]]], 
  "calc_hsp": [[18.063888149221956], [2.137121558765653], [2.26698643610238], [1.0507747966543328]], 
  "quality": "UnstableResult", 
  "validity": "False"
  }
```

Here it stores everything including:

- solvent combination ('cas_comb'),
- corresponding concentration statistical information ('conc', with full statistic details: the first element for each solvent is statistic average, the second is std.),
- statistical information for error (in the order of D, P, H, 1; for each term, the first entry corresponds to average, and the second is std.),
- calculated HSP from this combination ('calc_hsp', in the order of D, P, H, 1).
- data quality (suggests if the result is valid or not, and the reason to be filtered out), and
- validity (False results will be filtered out).

In short, the structure of the full calculation log json is:

```
[{
  "idx" : index,
  "cas_comb" : [cas_1, cas_2, ..., cas_n],
  "conc" : [[[average of conc for solvent 1], [std of conc for solvent 1]], ..., [conc info for solvent n]],
  "err" : [[[average error of D], [std of error of D], [average error of P], [std of error of P]], [[average error of H], [std of error of H], [average of error from 1], [std of error from 1]]],
  "calc_hsp": [[calculated D], [calculated P], [calculated H], [calculated "1"]], 
  "quality": "summary of data quality, can be an error message", 
  "validity": "True or False"

}]
```

#### Other outputs

calc_log_vld_01222023101554.txt: This file contains all the valid results after filteration. Information here has been reorganised into the successful log txt file. No need to pay too much attention on this file. (This is for the dedeveloper team to check intermediate output.)


### Step 4: advanced filtration

Now you can decide to relax or continue the advanced filtration step, which is based on the physical/chemical properties check.

In this version, we check the boiling point and miscibility. (There is limitation due to data availbility. Check Limitation section for more details.)

You will see:

```
=========================
Step 4: Advanced filtration (optional)
 This step will further include the consideration of solvent properties according to the condition set up.
 In this version, miscibility and boiling point will be evaluated.
 Data are based on PubChem.
 Please note, there could be some limitation of this function due to data availability. Check README for more discussion.

Continue advanced filtration?

[y/n]:
```

Select [y] will start two more filtration based on miscibility and boiling point check.

- If a solvent has an immiscible pair within the same predicted group, this group will be filtered out.
- If a solvent has a lower boiling point than set temperature, this group will be filtered out.

Once everything has been successfully checked, *SolvPred* will return you the path of advanced filtration log.The whole process has now been finished:


```
Continue advanced filtration?

[y/n]: y
2023-01-23  07:50:28
SolvPredictor v 2.0
 (License: GPL-3.0)

Please check:
C:\Users\sh19129\OneDrive - University of Bristol\Documents\MyProject\ML\HSP_python\calculation\cal_20221227_solv_pred_v2\hsp_toolkit_solv_pred_v_2.0\log\log_adv_filt_success_01232023075028.txt for calculation log.
```

The version, time and license info will also present again. *Don't worry about the huge time difference from the previous.. This example was done on the second day morning.*

The normal calculation time for a 2-solvent combination would be less than 1 second.

For 3-solvent it might be longer, but no longer than 5 seconds normally.

In the very rare case if it stucks to give any update after 10 seconds (dead loop somewhere I guess - hope not happen), use [ctrl + c] to force abort the program.


More output files will be saved in the log folder. We will briefly mention how it works as we go through those outputs.

#### log_adv_filt_success_01222023101554.txt

Again, this is the one of your interest.

The first part remains same. One more filtration option list will be stored:

```
Advanced filter options: 
['miscibility', 'bp']
```

One more filteration log json (named after "adv_filt_exp_info_") path will be presented:

```
Calculation log path: 
C:\Users\sh19129\OneDrive - University of Bristol\Documents\MyProject\ML\HSP_python\calculation\cal_20221227_solv_pred_v2\hsp_toolkit_solv_pred_v_2.0\log\adv_filt_exp_info_01222023101554.json
```

In the results section, more details regarding advanced filteration properties will be discussed:

```
Group 1 : 

solvent 1 : Propylene carbonate (108-32-7) 
concentration 1 :  9.47% 

bp /degree C: 241.6

miscibility check: 
No recorded miscibility issue or no solubility record. Manual check is recommended.

solvent 2 : Toluene (108-88-3) 
concentration 2 :  90.53% 

bp /degree C: 110.6

miscibility check: 
No recorded miscibility issue. Manual check is recommended if temperature has been varied.

calculated D /MPa^(1/2): 17.640788087782173
calculated P /MPa^(1/2): 2.9357929244636503
calculated H /MPa^(1/2): 2.0812967786641057
error of D /MPa^(1/2): -0.3592119122178268
error of P /MPa^(1/2): -0.06420707553634974
error of H /MPa^(1/2): 0.08129677866410567


```

There are two different message for immiscibility check:

The first one corresponds to the situation when the database does not contain any info of miscibility for this solvent. *SolvPred* will return a message saying:

```
No recorded miscibility issue or no solubility record. Manual check is recommended.
```

If this solvent contains an immiscible solvent pair in the database but no solvent in the same group conflicts to that, you will see:

```
No recorded miscibility issue. Manual check is recommended if temperature has been varied.
```

Refer to the Limitation section of this function, miscibility data is very limited in current database (based on PubChem). We can only provide as much info as we have to prevent miscibility issue. In addition, this property is temperature-dependent, which has even less experimental data available for each solvent. Therefore, for now we would still suggest to do manual check and can not 100% guarantee the as-predicted combinations do not lead to any undesired situation. (Improvement is on going!) 



#### adv_filt_exp_info_01222023101554.json

This file contain full details for each advanced filtration process.

The list could be very long. Let's take one element as an example:

```
{
  "group": 4, 
  "full_detail": 
  [
    {
      "CAS": "67-68-5", 
      "No.": 93, 
      "Name": "Dimethyl sulfoxide", 
      "ims_idx": "139;81;244;47;136;240;190;106", 
      "bp": 189, 
      "ori_idx": 285, 
      "ims_chk_msg": "No recorded miscibility issue. Manual check is recommended if temperature has been varied.", 
      "ims_solvent_in_comb": null, 
      "ims_validity": true, 
      "bp_chk_msg": "Above or equal to set temp", 
      "bp_validity": true, 
      "conc": 0.17370185847668593, 
      "calc_d": 17.524490650842214, 
      "calc_p": 2.8140266478430767, 
      "calc_h": 2.1462982015123093, 
      "err_d": -0.475509349157786, 
      "err_p": -0.18597335215692334, 
      "err_h": 0.14629820151230932
    }, 
    {
      "CAS": "108-67-8", 
      "No.": 149, 
      "Name": "Mesitylene", 
      "ims_idx": "243", 
      "bp": 164.7, 
      "ori_idx": 285, 
      "ims_chk_msg": "No recorded miscibility issue. Manual check is recommended if temperature has been varied.", 
      "ims_solvent_in_comb": null, 
      "ims_validity": true, 
      "bp_chk_msg": "Above or equal to set temp", 
      "bp_validity": true, 
      "conc": 0.826298141523314, 
      "calc_d": 17.524490650842214, 
      "calc_p": 2.8140266478430767, 
      "calc_h": 2.1462982015123093, 
      "err_d": -0.475509349157786, 
      "err_p": -0.18597335215692334, 
      "err_h": 0.14629820151230932
    }
  ]
}
      
```

The key process of immiscbility check is to look at whether the idx in db ("No." in the above json case) matches any idx in the "ims_idx" list. (In this case, there is no crash, so its "ims_validity" is True.)


#### Other outputs

Other outputs (adv_filt_all_01222023101554.json, calc_log_adv_all_01222023101554.txt, calc_log_adv_exp_01222023101554.txt, calc_log_adv_filt_01222023101554.txt) have overlaped info with the above mentioned results. (They are intermediate output for the developer team to test and check.)


#### Not continue advanced filtration

If you do not want to conduct this process, select [n]. *SolvPred* will return you the path of where the previous step log has been stored, so that you can check:

```
Continue advanced filtration?

[y/n]: n
Please check C:\Users\sh19129\OneDrive - University of Bristol\Documents\MyProject\ML\HSP_python\calculation\cal_20221227_solv_pred_v2\hsp_toolkit_solv_pred_v_2.0\log\log_success_01232023074457.txt for calculation log.

```

It will then terminate the whole program. To start another attempt, you need to go back to the first step and run it from the beginning:

```
(hsp_solv_pred_2) PS C:\Users\sh19129\OneDrive - University of Bristol\Documents\MyProject\ML\HSP_python\calculation\cal_20221227_solv_pred_v2\hsp_toolkit_solv_pred_v_2.0> python solv_pred_main.py
```

### General note

Please read the instruction carefully and enter the correct format for each input as possible. (though *SolvPred* will check the validity in many cases.)

In case something unexpected has been submitted, you may see:

```
Invalid input. Press enter to continue. [enter]
```

See the example below: 

```
[t] - set a different temperature
[c] - continue as room temperature (25 degree c).
[q] - quit

# Here I pressed enter without entering anything....
```

If the "Invalid input" warning pop up, a follow-up suggestion will present. (In this case it asks you to press [enter], any other character will return the same error message).


```
Invalid input. Press enter to continue. [enter]q
Invalid input. Press enter to continue. [enter]
[t] - set a different temperature
[c] - continue as room temperature (25 degree c).
[q] - quit
q
```


## Limitations

   - Some categories may have a limitation of avilable data, which will be labelled as -1 or None in the database.
   - The temperature control function is only based on correcting HSP in this version. Properties applied in advanced filtration (e.g., miscibility) may also be temperature-dependent but no direct correction is applied in this version.
   - If user manually edited the database and add additional solvents without available HSP, the temperature correction for data-missing group will be disabled and corresponding solvent will be removed from database after temperature updating check step.
   - The miscbility check function may not be 100% guaranteed due to limited data and complex temperature-dependent behaviour. In addition, the defintion of "miscibility" is ambiguous: partial soluble cases (which nevertheless has a severe lack of data in terms of the partition threshold) will be regarded as not-immiscible in this version and will be present as valid results. It is recommended to manually check the performance if unsure.


## References

1. C. Hansen, Hansen Solubility Parameters – A user’s handbook, 2nd edition, 2011.
2. X. Fang, C. F.J. Faul, N. Fey, E. Gale, SolvPred - A python toolkit to predict multi-solvent combinations with target Hansen solubility parameters (manuscript in preparation).


## Disclaimer

  - SolvPred is under continous tests and improvement. The output only provide suggestion. Results may vary with multi factors in complicated situations. It is the users responsbility to manuallay check the exact experimental performance in different scenarios.

 ---

This project is licensed under [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html).
