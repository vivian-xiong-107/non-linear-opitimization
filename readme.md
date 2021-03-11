<center><b><font size='5'>The guide to using code</font></b></center>

## Python File

`economic dispatch.py`: Economic dispatch

`dc-opf.py`: DC-OPF

`asm.py`: Active set method

`simplex_api.py`: Simplex method. referred from https://github.com/privateEye-zzy/simplex



## Economic Dispatch

#### How to set?

Change the data in related csv in `economic-dispatch-csv`.

**1.`economic_dispatch.csv`: set the limit on the generation of each bus and the total demand**

content:

`bus`: bus number

`Pmax`: maximum real power output

`Pmin`: minimum real power output

`total_demand`: total demand

**2.`gen_cost.csv`: set the cost function of each bus**

content:

`n^2`: Coefficient of quadratic term

`n`: Coefficient of first term

`c`: Constant

(Attention: the order corresponds to `bus 1` to `bus n`)

#### How to run?

Run `economic dispatch.py`



## DC-OPF

#### How to set?

Change the data in related csv in `dcopf-csv`.

**1.`bus_data.csv`: set the demand of each bus**

content:

`bus`: bus number

`Pd`: Demand of each bus

**2.`generator_data.csv`: set the limit on the generation of each bus**

content:

`bus`: bus number

`Pmax`: maximum of the generation

`Pmin`: minimum of the generation

**3.`branch_data.csv`: set branch data**

`fbud`: from bus number

`tbus`: to bus number

`x`: reactance

`angmin`:  minimum angle difference, angle(Vf) - angle(Vt) (degrees)

`angmax`: maximum angle difference, angle(Vf) - angle(Vt) (degrees)

(Attention: `fbud` should be smaller than `tbus`)

**4.`gen_cost.csv`: set the cost function of each bus**

`n^2`: Coefficient of quadratic term

`n`: Coefficient of first term

`c`: Constant

(Attention: the order corresponds to `bus 1` to `bus n`)

#### How to run?

Run `dc-opf.py`



**Attention**: The address of csv files used in `open` function may need to be reset according to the actual situtaion. 

