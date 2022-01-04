# Automating MOS characterisation

import numpy as np
import matplotlib.pyplot as plt
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
dc vgs 0.05 1.3 0.01

* Run the sim
run

set filetype=ascii
set wr_singlescale
set wr_vecnames

wrdata output.txt @M1[id], @M1[vdsat], @M1[cgs], @M1[cgg], @M1[cds] 
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


exit
.endc

*************************************
* End of file
*************************************
.end

'''

# TODO : change length and call the above code again. Define the above code in a function

with open(filename,"w") as file:
    file.write(contents)

call(["ngspice", "dummy.cir"])

# start post processing

with open('output.txt') as txtfile :
    temp = np.genfromtxt(txtfile, dtype=float)

# ngspice extracted values

vgs    = temp[1:,0]
id     = temp[1:,1]
vdsat  = temp[1:,2]
cgs    = temp[1:,3]
cgg    = temp[1:,4]
cds    = temp[1:,5] 
cdd    = temp[1:,6]
gm     = temp[1:,7]
gds    = temp[1:,8]
gmbs   = temp[1:,9]
vth    = temp[1:,10]

# custom definitions

gm_by_id   = gm/id 
gain       = gm/gds
ft         = gm/cgg

width      = 100e-6

id_wid     = id/width
gm_wid     = gm/width
gds_wid    = gds/width
cgg_wid    = cgg/width
cgs_wid    = cgs/width
gmbs_wid   = gmbs/width
cdd_wid    = cdd/width
cds_wid    = cds/width

# Plotting relevant figures

plt.figure(1)
plt.plot(gm_by_id,vgs)
plt.title("Vgs vs gm/Id")
plt.ylabel("Vgs")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()

plt.figure(2)
plt.plot(gm_by_id,id_wid)
plt.title("Id/width vs gm/Id")
plt.ylabel("Id/W")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()

plt.figure(3)
plt.plot(gm_by_id,gm_wid)
plt.title("gm/width vs gm/Id")
plt.ylabel("Vgs")
plt.xlabel("gm/W")
plt.grid(True)
plt.show()

plt.figure(4)
plt.plot(gm_by_id,gds_wid)
plt.title("gds/width vs gm/Id")
plt.ylabel("Vgs")
plt.xlabel("gds/W")
plt.grid(True)
plt.show()

plt.figure(5)
plt.plot(gm_by_id,cgs_wid)
plt.title("Cgs/width vs gm/Id")
plt.ylabel("Vgs")
plt.xlabel("Cgs/W")
plt.grid(True)
plt.show()

plt.figure(6)
plt.plot(gm_by_id,cgg_wid)
plt.title("Cgg/width vs gm/Id")
plt.ylabel("Cgg/W")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()

plt.figure(6)
plt.plot(gm_by_id,cgg_wid)
plt.title("Cdd/width vs gm/Id")
plt.ylabel("Cdd/W")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()

plt.figure(7)
plt.plot(gm_by_id,vth)
plt.title("Vth vs gm/Id")
plt.ylabel("Vth")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()

plt.figure(8)
plt.plot(gm_by_id,vdsat)
plt.title("vdsat vs gm/Id")
plt.ylabel("Vdsat")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()

plt.figure(9)
plt.plot(gm_by_id,gain)
plt.title("Gain vs gm/Id")
plt.ylabel("Gain")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()