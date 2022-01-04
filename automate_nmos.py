# Automating MOS characterisation

import numpy as np
from subprocess import call

filename = "dummy.cir"

contents = f'''NMOS characterisation

*************************************
* Include model file 
*************************************
.include 130nm_bulk.pm

*************************************
* Defining arameters 
*************************************
.param len = 0.13u
.param width = 100u 
.param lmin = 0.13u

*************************************
* Circuit definition
*************************************
vgs 1 0 dc 0.5
M1 1 1 0 0 nmos l={{len}} w={{width}} as={{2*lmin*width}} ad={{2*lmin*width}} ps={{4*lmin+2*width}} pd={{4*lmin+2*width}}

*************************************
* Control section
*************************************

.control 

save @M1[id], @M1[vdsat], @M1[vth], @M1[cgs], @M1[cgg], @M1[cds] ,
+ @M1[cdd], @M1[gm], @M1[gds], @M1[gmbs], @M1[vsat]

* DC sweep
dc vgs 0 1.3 0.01

* Run the sim
run

set filetype=ascii
set wr_singlescale
set wr_vecnames

wrdata output.csv @M1[id], @M1[vdsat], @M1[cgs], @M1[cgg], @M1[cds] 
+ @M1[cdd], @M1[gm], @M1[gds], @M1[gmbs], @M1[vth]

* Plot commands
* plot @M1[id]
* plot @M1[gm]
* plot @M1[gmbs]
* plot @M1[gds]
* plot @M1[cgs]
* plot @M1[cgg]
* plot @M1[vdsat]
* plot @M1[vsat]


*exit
.endc

*************************************
* End of file
*************************************
.end

'''

# TODO : clear output.csv before running ngspice
#! do length sweep in ngspice code and write it all at oncce

with open(filename,"w") as file:
    file.write(contents)

call(["ngspice", "dummy.cir"])


