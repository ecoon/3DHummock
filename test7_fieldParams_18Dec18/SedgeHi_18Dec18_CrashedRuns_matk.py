import matplotlib
matplotlib.use('agg')

import numpy as np
from matk import matk
import parse_ats
import atsxml

#checkpointRunName = "_27Nov18"

def model(pars, hostname='dum', processor=1):
	# ATS ##############################################################################
    	# Modify base ats xml input file and run ats
	branchName = "hillslope-fieldParams_18Dec18"
	fname = branchName + "-" + str(pars['bac']) + "bac_" + str(pars['bct']) + "bct"
	
	m = atsxml.get_root('../test7_' + branchName + '_template' + '_18Dec18_CrashedRuns' + '_input.xml')
	
	atsxml.replace_by_path(m,['mesh','domain','read mesh file parameters','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','computational domain acrotelm','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','computational domain catotelm','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','computational domain mineral','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','computational domain bedrock','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','surface','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','bottom face','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['state','permeability','function','acrotelm','function','function-constant','value'],pars['Kac'])
	atsxml.replace_by_path(m,['state','permeability','function','catotelm','function','function-constant','value'],pars['Kct'])
	atsxml.replace_by_path(m,['state','permeability','function','rest domain','function','function-constant','value'],pars['Kmn'])
	atsxml.replace_by_path(m,['cycle driver','restart from checkpoint file'],'../checkpoint_files/' + runName + checkpointSuffix + '/' + runName + checkpointSuffix + '.' + str(pars['RunNum']) + 'checkpoint_last.h5')

    	atsxml.run(m, nproc=1, mpiexec='mpirun', stdout='stdout.out', stderr='stdout.err', cpuset=processor)
	return True


# Create cpusets, 4 cpus to a set
# This is necessary so that the ATS runs get spread evenly over processors and doesn't stack up on processors
# On our servers, the host key ('dum' below) isn't necessary since we run all jobs on the same server.
# On clusters, you may be sending different runs to different hosts (computers). 
# In that case, the dictionary keys are important for indicating the host.
# The dictionary values (lists of integers) identify which processors to put each ATS run.
njobs = 6
nparams = 6
hosts = {'dum': map(str, range(10,njobs))}
print hosts

# Instantiate MATK object specifying the "model" function defined above as the MATK "model"
p = matk(model=model)

# Add parameters that you want to sample over and their ranges
p.add_par('bac', min=0.01, max=0.22, value=0.1)
p.add_par('bct',min=0.02, max=0.4, value=0.14)
p.add_par('Kac',min=1.03e-3, max=2.8e-3, value=1.92e-3)
p.add_par('Kct',min=2.52e-6, max=3.51e-5, value = 5e-6)
p.add_par('Kmn',min=2.09e-6, max=1.25e-5, value = 5e-6)
p.add_par('RunNum',min=1,max=32, value = 6)

d = [[0.1,0.2,1.57e-10,4.68e-13,1.05e-15,5],[0.1,0.2,1.57e-10,4.68e-13,7.97e-14,6],[0.1,0.2,1.57e-10,1.43e-12,1.05e-15,7],[0.1,0.2,1.57e-10,1.43e-12,7.97e-14,8],[0.17,0.2,1.05e-11,1.43e-12,7.97e-14,20],[0.17,0.2,1.57e-10,1.43e-12,1.05e-15,23]]

runName = 'SedgeHi'
checkpointSuffix = '_18Dec18'
# Create MATK sampleset
s = p.create_sampleset(d)

# Create parameter study of all combinations of min and max values for each parameter
# s = p.parstudy(nvals=[2,3,3])
# Save samples to file for inspection
# s.savetxt('sample.txt')
# Run sampleset using "hosts" dictionary defined above. 
s.run(cpus=hosts, workdir_base=runName + '_18Dec18_CrashedRuns' + 'checkpointTest', reuse_dirs=True)
