# FastSimRefinement

This repo contains the basic code needed to process samples needed for refinement studies and to look at results produced by Moritz, Nils, and others. 

## Make synchronized FastSim-FullSim jet and event trees:

as a small  test
```
python3 tools/makeSynchTreesFromNANO.py --fnamekeyword "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/Fast/1485/step3_inNANOAODSIM.root"
```

to do a bunch of jobs, first (1-time only) make a couple of directories:

```
mkdir jobs output
```

submit jobs to produce training samples:
```
python tools/submitJobs.py --analyzer tools/makeSynchTreesFromNANO.py --fnamekeyword "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/T1tttt/FastGenDecays/*/*NANO*.root" --emod2 1 --outdir output/smallchunksT1tttt
```

then submit jobs to produce testing samples:
```
python tools/submitJobs.py --analyzer tools/makeSynchTreesFromNANO.py --fnamekeyword "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/T1tttt/FastGenDecays/*/*NANO*.root" --emod2 2 --outdir output/smallchunksT1tttt
```



