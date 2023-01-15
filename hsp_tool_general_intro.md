Last update: 15/01/2023

<p>
 <img src=https://github.com/xueannafang/hsp-toolkits/blob/main/figs/logo_all.png width=100>
 </p>

# Introduction

## Aim

The aim of this project is to develop quantitative solvent selection tools for synthesis and property control of functional materials. The focus is based on Hansen solubility parameters (HSP).

## HSP

HSP decompose the molecular interaction into dispersion (𝜹𝑫), dipolar (𝜹𝑷) and hydrogen-bonding (𝜹𝑯) interactions.

Solubility can be quantified by the Hansen distance (R). HSP of a solvent mixture follows a linear combination of its components, which greatly expands options based on given lab solvents.

<p>
 <img src=https://github.com/xueannafang/hsp-toolkits/blob/main/figs/HSP_general.png width=300>
 </p>

## Challenges

There are nevertheless a couple of challenges when using HSP:

1. Determining which solvent combinations can lead to a given HSP.

2. Obtaining HSP of the studied materials (M), especially for complicated systems without a clear understanding of structure, e.g., amorphous polymers.

## Solutions

To improve these issues, we developed two python-based toolkits:

1. *Solvent Predictor (SolvPred)*:
- Based on the target Hansen solubility parameters (HSPs), propose a list of multi-solvent combination.

Given that HSP of a solvent mixture follows a linear combination of each individual component, researchers can easily calculate the HSP of solvent systems with known components. It is however much more difficult to reverse this process.

<p>
 <img src="https://github.com/xueannafang/hsp-toolkits/blob/main/figs/bg_solvpred.png" width=800>
 </p>

The aim of *SolvPred* is to support the solvent suggestion when a desired goal of HSP is known.

The key function is to convert the target HSP into a multi-solvent list based on the requirement of user.

<p>
 <img src="https://github.com/xueannafang/hsp-toolkits/blob/main/figs/solv_pred_sch.png" width=300>
 </p>

 Advanced property filtration could be avilable depending on users preference.


2. *M Locator (MLoc)*:
- Predict HSPs of the studied material based on an experimental-measurable solubility score.

 <!-- <p>
  <img src="https://github.com/xueannafang/hsp-toolkits/blob/main/figs/sch_sp_mloc.png" width=700>
 </p> -->

As indicated by its name, *MLoc* locates "*M*" in the Hansen space.

It is a top-down approach aiming at obtaining the HSP of as-studied material (M) using a solubility score (*w<sub>i</sub>*) measured from a series of solvents.

*MLoc* can be useful for complicated systems whose exact chemical component is hard to confirm. This could be, for example, polymeric systems with high dispersity, mixtures of isomers or analogous, etc., where bottom-up method like group contribution may not be easy to be carried out. 

<p>
  <img src=https://github.com/xueannafang/hsp-toolkits/blob/main/figs/m_loc_sch.png width=300>
  </p>

Part of the *MLoc* can be connected to *SolvPred*] to provide multi-solvent suggestion based on the as-predicted HSP of the material.

The solubility indicator applied in the prototype version is based on UV-Vis spectroscoy features. User can specify their own indicator (served as the weight function).

The studied materials tested during the development of *MLoc* are mainly based on [conjugated microporous polymers (CMP)](https://www.sciencedirect.com/topics/engineering/conjugated-microporous-polymer).


## Versions

### SolvPred

- [v2.0](https://github.com/xueannafang/hsp_toolkit_solv_pred_v_2.0)

- [Prototype/v1.0](https://github.com/xueannafang/hsp_toolkit_prototype/tree/main/HSP_SolventPredictor)

### MLoc

<!-- - [v2.0](https://github.com/xueannafang/HSP_toolkit_MLoc_v2) -->
- [Prototype/v1.0](https://github.com/xueannafang/hsp_toolkit_prototype/tree/main/HSP_MLocator)


---

## References

1. C. Hansen, Hansen Solubility Parameters – A user’s handbook, 2nd edition, 2011.
2. X. Fang, C. F.J. Faul, N. Fey, E. Gale, SolvPred - A python toolkit to predict multi-solvent combinations with target Hansen solubility parameters (manuscript in preparation)
3. X. Fang, U. Karatayeva, S. A. A. Siyabi, B. B. Narzary, M. G. Girgin, D. Mukhanov, C. F.J. Faul, N. Fey, E. Gale, MLoc - A python toolkit to predict Hansen solubility parameters of functional materials (manuscript in preparation).

(Phyciscal/Chemical data of solvents in the database were collected from PubChem and HSP handbook.)

## Disclaimer

  - The as-mentioned HSP tools are under continous tests and improvement. The output only provide suggestion. Results may vary with multi factors in complicated situations. It is the users responsbility to manuallay check the exact experimental performance in different scenarios.

---

This project is developed by

- [Xue Fang](https://www.linkedin.com/in/xue-fang-811204163/) (School of chemistry, University of Bristol, UK)

with instruction from

- [Prof Charl FJ Faul](https://faulresearchgroup.com/charl-f-j-faul/) (School of chemistry, University of Bristol, UK)
- [Prof Natalie Fey](https://feygroupchem.wordpress.com/) (School of chemistry, University of Bristol, UK)
- [Dr Ella Gale](https://www.bristol.ac.uk/people/person/Ella-Gale-58ab10ba-8b85-4513-944e-6d9020b6ff2c/) (School of chemistry, University of Bristol, UK)

Experimental test data of *M Locator* is contributed by the Conjugated Microporous Polymers (CMP) team of the [Faul research group](https://faulresearchgroup.com/).


The development and communication of this work are funded by::

- [University of Bristol](https://www.bristol.ac.uk/) - [Chinese Scholarship Council](https://www.chinesescholarshipcouncil.com/) Joint Scholarship
- [Royal Society of Chemistry Researcher Development Grants](https://www.rsc.org/prizes-funding/funding/find-funding/researcher-development-grant/)
- [Bristol Doctoral College](http://www.bristol.ac.uk/doctoral-college/)

The author acknowledges all those who have provided inputs and technical support during the design and exploration of these toolkits, in particular:

- [Dr Jie Chen](https://scholar.google.com/citations?user=GPM9kTgAAAAJ&hl=en) (Fuzhou University, China)
- Jillisa Thompson (School of Chemistry, University of Bristol, UK)
- [Bo Gao](https://www.linkedin.com/in/bo-gao-771841199/) (School of physics, University of Bristol, UK)
- [ChatGPT](https://openai.com/blog/chatgpt/)


---

This project is licensed under [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html).
