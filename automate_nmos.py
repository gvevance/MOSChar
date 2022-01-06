# Automating MOS characterisation

import numpy as np
import matplotlib.pyplot as plt
from subprocess import call

cir_filename = "temp_nmos.cir"
value_file = "values_nmos.txt"

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

wrdata {value_file} @M1[id], @M1[vdsat], @M1[cgs], @M1[cgg], @M1[cds] 
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

with open(cir_filename,"w") as file:
    file.write(contents)

call(["ngspice", cir_filename])

# start post processing

with open(value_file) as txtfile :
    temp = np.genfromtxt(txtfile, dtype=float)

# ngspice extracted values

vgs    = temp[1:,0]
id     = temp[1:,1]
vdsat  = temp[1:,2]
cgs    = -temp[1:,3]
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
gm_by_gmbs = gm/gmbs

# Plotting relevant figures

plt.figure(1)
plt.plot(vgs,gm_by_id)
plt.title("gm/Id vs Vgs")
plt.ylabel("gm/Id")
plt.xlabel("Vgs")
plt.grid(True)
plt.show()

plt.figure(2)
plt.plot(gm_by_id,np.log10(id_wid))
plt.title("log10(Id/width) vs gm/Id")
plt.ylabel("log10(Id/W)")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()

plt.figure(3)
plt.plot(gm_by_id,np.log10(gm_wid))
plt.title("log10(gm/width) vs gm/Id")
plt.ylabel("log10(gm/W)")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()

plt.figure(4)
plt.plot(gm_by_id,np.log10(gds_wid))
plt.title("log10(gds/width) vs gm/Id")
plt.ylabel("log10(gds/W)")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()

plt.figure(5)
plt.plot(gm_by_id,np.log10(cgs_wid))
plt.title("log10(Cgs/width) vs gm/Id")
plt.ylabel("log10(cgs/W)")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()

plt.figure(6)
plt.plot(gm_by_id,np.log10(cgg_wid))
plt.title("log10(cgg/width) vs gm/Id")
plt.ylabel("log10(cgg/W)")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()

plt.figure(6)
plt.plot(gm_by_id,np.log10(cgg_wid))
plt.title("log10(Cdd/width) vs gm/Id")
plt.ylabel("log10(cdd/W)")
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
plt.plot(gm_by_id,np.log10(gain))
plt.title("log10(Gain) vs gm/Id")
plt.ylabel("log10(gm/gds)")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()

plt.figure(10)
plt.plot(gm_by_id,np.log10(gm_by_gmbs))
plt.title("log10(gm/gmbs) vs gm/Id")
plt.ylabel("log10(gm/gmbs)")
plt.xlabel("gm/Id")
plt.grid(True)
plt.show()
