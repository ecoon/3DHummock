#!/bin/bash
#!/bin/sh
# This script creates the 1D column file that gets fed to test7
cur_dir=`pwd`
cd $ATS_SRC_DIR/tools/utils/
rm -rf *.h5
cp lustre/or-hydra/cades-ccsi/oconnormt/repo/3DHummock-try3/test1/run02_09Oct18/visdump_data.h5 .
cp lustre/or-hydra/cades-ccsi/oconnormt/repo/3DHummock-try3/test1/run02_09Oct18/visdump_mesh.h5 .
python column_data.py -t 0
cd $cur_dir
cp $ATS_SRC_DIR/tools/utils/column_data.h5 column_data_run02_09Oct18.h5
echo 'Exp1 Column h5 file successfully created'
