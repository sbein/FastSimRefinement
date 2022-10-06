import os, sys
from glob import glob
from random import shuffle 
from time import sleep

test = False

'''
#nano
python tools/submitJobs.py --analyzer tools/makeSynchTreesFromNANO.py --fnamekeyword "/nfs/dust/cms/user/beinsam/FastSim/CMSSW_10_6_22/src/TTbar/Fast/*/step3_inNANOAODSIM.root"
python tools/ahadd.py -f mc_fullfastnn_step3_fromNANOAODSIM.root output/smallchunks/mc_fullfastnn_*NANO*.root
python3 tools/drawFromSynchEventTree.py output/mc_fullfastnn_step3_fromNANOAODSIM.root

#mini
python tools/submitJobs.py --analyzer tools/makeSynchTreesFromMINI.py --fnamekeyword "/nfs/dust/cms/user/connorpa/FastSim/CMSSW_10_6_22/src/TTbar/Fast/*/step3_inMINIAODSIM.root"
python tools/ahadd.py -f output/mc_fullfastnn_step3_fromMINIAODSIM_Pt15Eta5p0GjAnDr0p4.root output/smallchunks/mc_fullfastnn_*MINI*.root
python3 tools/drawFromSynchEventTree.py output/mc_fullfastnn_step3_fromMINIAODSIM_Pt15Eta5p0GjAnDr0p4.root &
python3 tools/drawFromSynchEventTree.py output/mc_fullfastnn_step3_fromMINIAODSIM_Pt15Eta2p4.root &

#mini split training, test
python tools/submitJobs.py --analyzer tools/makeSynchTreesFromMINI.py --fnamekeyword "/nfs/dust/cms/user/connorpa/FastSim/CMSSW_10_6_22/src/TTbar/Fast/*/step3_inMINIAODSIM.root" --emod2 1
python tools/submitJobs.py --analyzer tools/makeSynchTreesFromMINI.py --fnamekeyword "/nfs/dust/cms/user/connorpa/FastSim/CMSSW_10_6_22/src/TTbar/Fast/*/step3_inMINIAODSIM.root" --emod2 2

python tools/ahadd.py -f output/mc_fullfastnn_step3_fromMINIAODSIM_Pt15Eta5p0GjAnDr0p2_ForTraining.root output/smallchunks/mc_fullfastnn_*MINI*ForTraining.root
python tools/ahadd.py -f output/mc_fullfastnn_step3_fromMINIAODSIM_Pt15Eta5p0GjAnDr0p2_ForTesting.root output/smallchunks/mc_fullfastnn_*MINI*ForTesting.root

python tools/ahadd.py -f output/mc_fullfastnn_TTbar_fromNANO_Pt15Eta5p0GjAnDr0p2_ForTraining.root output/smallchunksTTbar/mc_fullfastnn_*NANO*ForTraining.root
python tools/ahadd.py -f output/mc_fullfastnn_TTbar_fromNANO_Pt15Eta5p0GjAnDr0p2_ForTesting.root output/smallchunksTTbar/mc_fullfastnn_*NANO*ForTesting.root

python tools/submitJobs.py --analyzer tools/makeSynchTreesFromMINI.py --fnamekeyword "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/Fast/*/step3_inMINIAODSIM.root" --emod2 0
python tools/submitJobs.py --analyzer tools/makeSynchTreesFromMINI.py --fnamekeyword "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/FastEstatMean/*/step3_inMINIAODSIM.root" --emod2 0
python tools/ahadd.py -f output/mc_fullfastnn_step3_fromMINIAODSIM_FastEstatMean.root output/smallchunks/*EstatMean*.root
python tools/ahadd.py -f output/mc_fullfastnn_step3_fromMINIAODSIM_Ootb.root output/smallchunks/*Ootb*.root

#could also do 
python3 tools/drawFromSynchJetTree.py output/mc_fullfastnn_step3_fromMINIAODSIM_Pt15Eta5p0GjAnDr0p4.root



'''

import argparse
parser = argparse.ArgumentParser()
defaultfkey = 'Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2_28'
parser.add_argument("-v", "--verbosity", type=bool, default=False,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultfkey,help="file")
parser.add_argument("-outdir", "--outdir", type=str, default='output/smallchunks')
parser.add_argument("-nfpj", "--nfpj", type=int, default=1)
parser.add_argument("-emod2", "--emod2", type=int, default=0)
args = parser.parse_args()
nfpj = args.nfpj
fnamekeyword = args.fnamekeyword.strip()
filenames = fnamekeyword
analyzer = args.analyzer
analyzer = analyzer.replace('python/','').replace('tools/','')
outdir = args.outdir
nfpj = args.nfpj
emod2 = args.emod2


#try: 
moreargs = ' '.join(sys.argv)
moreargs = moreargs.split('--fnamekeyword')[-1]
moreargs = ' '.join(moreargs.split()[1:])

args4name = moreargs#.replace(' ','').replace('--','-')

moreargs = moreargs.strip()
print ('moreargs', moreargs)

cwd = os.getcwd()
filelist = glob(filenames)
#shuffle(filelist)

if not os.path.exists(outdir): os.system('mkdir -p '+outdir)

filesperjob = nfpj

print ('len(filelist)', len(filelist))
print ('filesperjob', filesperjob)

def main():
	ijob = 1
	files = ''
	jobcounter_ = 0
	for ifname, fname in enumerate(filelist):
		files += fname+','
		if (ifname)%filesperjob==0: jname = fname
		if (ifname)%filesperjob==filesperjob-1 or ifname==len(filelist)-1:
			jobname = analyzer.replace('.py','')+'_'+jname[jname.rfind('/')+1:].replace('.root','_'+str(ijob))+'_'+outdir.split('/')[-1]
			if len(fname.split('/'))>1: 
				jobname = jobname+'__'.join(fname.split('/')[-2:])
			if 'EstatMean' in fnamekeyword: 
				jobname = jobname+'_EstatMean.root'
			if os.path.isfile('jobs/'+jobname+'.sh'):
				print ('skipping', fname, 'since', 'jobs/'+jobname+'.sh', 'exists')
				continue
			fjob = open('jobs/'+jobname+'.sh','w')
			files = files[:-1]#this just drops the comma
			fjob.write(jobscript.replace('CWD',cwd).replace('FNAMEKEYWORD',files).replace('ANALYZER',analyzer).replace('MOREARGS',moreargs).replace('JOBNAME',jobname).replace('OUTDIR',outdir))
			fjob.close()
			os.chdir('jobs')
			command = 'condor_qsub -cwd '+jobname+'.sh &'
			jobcounter_+=1
			print ('command', command)
			if not test: os.system(command)
			os.chdir('..')
			files = ''
			ijob+=1
			sleep(0.05)
	print ('submitted', jobcounter_, 'jobs')
	

jobscript = '''#!/bin/zsh
source /etc/profile.d/modules.sh
source /afs/desy.de/user/b/beinsam/.bash_profile
module use -a /afs/desy.de/group/cms/modulefiles/
module load cmssw
export THISDIR=$PWD
echo "$QUEUE $JOB $HOST"


cd /nfs/dust/cms/user/beinsam/FastSim/Refinement/CMSSW_12_2_3/src
cmsenv 
cd ../../
export HOME=/afs/desy.de/user/b/beinsam
#export PYTHONPATH=$HOME/.local/lib/python3.8/site-packages:$PYTHONPATH

python3 -m pip install torch===1.10.2
python3 -m pip install scikit-learn
python3 -m pip install --upgrade scikit-learn==0.24.2
python3 -m pip install --upgrade pandas==1.4.1

cd ../../

export timestamp=$(date +%Y%m%d_%H%M%S%N)
mkdir $timestamp
cd $timestamp
cp -r CWD/tools .
cp -r CWD/datasets . 
cp CWD/*.pkl .
echo doing a good old pwd:
pwd
python3 tools/ANALYZER --fnamekeyword FNAMEKEYWORD MOREARGS
mv *.root CWD/OUTDIR
mv *.json CWD/OUTDIR
cd ../
rm -rf $timestamp
'''

'''
source /cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc8-opt/setup.sh
python3 -m pip install scikit-learn
python3 -m pip install --upgrade scikit-learn==0.24.2
export PYTHONPATH=$HOME/.local/lib/python3.8/site-packages:$PYTHONPATH
'''

main()
