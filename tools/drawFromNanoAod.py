from ROOT import *
from glob import glob
from shared_utils import *
gStyle.SetOptStat(0)
import os, sys

'''
=================================1-1 compare:
rm jobs/*
rm -rf pdfs/TTbar
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/Fast/*/step3_inNANOAODSIM.root"
rm -rf pdfs/T1tttt
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/T1tttt/Fast/*/step3_inNANOAODSIM.root"
#...
rm -rf ~/www/FastSim/Nano/27June2022/TTbar
cp -r pdfs/TTbar ~/www/FastSim/Nano/27June2022/
rm -rf ~/www/FastSim/Nano/27June2022/T1tttt
cp -r pdfs/T1tttt ~/www/FastSim/Nano/27June2022/
python /afs/desy.de/user/b/beinsam/www/dir_indexer.py /afs/desy.de/user/b/beinsam/www/FastSim/Nano -r -t /afs/desy.de/user/b/beinsam/www/templates/default.html
python tools/bigindexer.py "/afs/desy.de/user/b/beinsam/www/FastSim/Nano/"
==================================1-1-1 compare:
rm jobs/*
rm -rf pdfs/TTbar
rm -rf pdfs/T1tttt
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/Fast/*/step3_inNANOAODSIM.root,/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/FastEstatMeanGenDecays/*/step3_inNANOAODSIM.root"
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/Fast/*/step3_inNANOAODSIM.root,/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/FastGenDecays/*/step3_inNANOAODSIM.root"
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/T1tttt/Fast/*/step3_inNANOAODSIM.root,/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/T1tttt/FastGenDecays/*/step3_inNANOAODSIM.root"
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/Fast/*/step3_inNANOAODSIM.root,/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_9_4_11/src/TTbar/Fast/*/step3_inNANOAODSIM.root"
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_9_4_10/src/TTbar/Fast/*/step3_inNANOAODSIM.root"
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_9_4_11/src/TTbar/Fast/*/step3_inNANOAODSIM.root"
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_9_4_11/src/T1tttt/Fast/*/step3_inNANOAODSIM.root"
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/MuGun1100/Fast/*/step3_inNANOAODSIM.root"
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/MuGun1200/Fast/*/step3_inNANOAODSIM.root"

#dev
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/DevDecay/CMSSW_12_2_X_2022-07-10-0000/src/TTbar/Fast/*/step3_inNANOAODSIM.root,/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/DevDecay/CMSSW_12_2_X_2022-07-10-0000/src/TTbar/FastGenDecays/*/step3_inNANOAODSIM.root"
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/DevDecay/CMSSW_12_2_X_2022-07-10-0000/src/T1tttt/Fast/*/step3_inNANOAODSIM.root,/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/DevDecay/CMSSW_12_2_X_2022-07-10-0000/src/T1tttt/FastGenDecays/*/step3_inNANOAODSIM.root"

rm -rf pdfs/T1tttt
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/Refinement/Backport2Decayer/CMSSW_12_4_X_2023-05-16-2300/src/T1tttt/Fast/*/*NANO*.root,/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/DevDecay/CMSSW_12_2_X_2022-07-10-0000/src/T1tttt/FastGenDecays/*/step3_inNANOAODSIM.root"
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/T1tttt/Fast/*/step3_inNANOAODSIM.root,/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/FastEstatMean"

#..

#Check FastSim/FastSim differences (first set obvious flag to True below), then adjust:
rm -rf pdfs/T1tttt_Fast_C106XvsC10630
nohup python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/Refinement/Backport2Decayer/CMSSW_10_6_30/src/T1tttt/Fast/*/*NANO*.root,/nfs/dust/cms/user/beinsam/FastSim/Refinement/Backport2Decayer/CMSSW_10_6_X_2023-04-30-0000/src/T1tttt/Fast/*/*NANO*.root" &
rm -rf ~/www/FastSim/Nano/T1tttt_Fast_C106XvsC10630
cp -r pdfs/T1tttt_Fast_C106XvsC10630 ~/www/FastSim/Nano/T1tttt_Fast_C106XvsC10630
#...
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/Yash/CMSSW_14_1_X_2024-03-28-1100/src/T1ttttRun3/Fast/*/*NANO.root,/nfs/dust/cms/user/beinsam/FastSim/Yash/CMSSW_14_1_X_2024-03-28-1100/src/T1ttttRun3/Fast10e6/*/*NANO.root"
 
#run 3 NANO validation
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/Refinement/CMSSW_12_6_0/src/TTbarRun3/Fast/*/*NANO.root"

rm -rf ~/www/FastSim/Nano/6July2022/TTbar_HeadVsFastEstatMeanGenDecays
cp -r pdfs/T1tttt ~/www/FastSim/Nano/6July2022/T1tttt_9_4_11
cp -r pdfs/TTbar ~/www/FastSim/Nano/6July2022/TTbar_12_2_XDev
cp -r pdfs/T1tttt ~/www/FastSim/Nano/6July2022/T1tttt_12_2_XDev
cp -r pdfs/TTbar ~/www/FastSim/Nano/6July2022/TTbar_9_4_11
cp -r pdfs/MuGun1100 ~/www/FastSim/Nano/6July2022/MuGun1100
cp -r pdfs/MuGun1200 ~/www/FastSim/Nano/6July2022/MuGun1200
cp -r pdfs/TTbarRun3 ~/www/FastSim/Nano/6July2022/TTbarRun3_12_6_0
cp -r pdfs/T1tttt_Fast_C124X ~/www/FastSim/Nano/T1tttt_Fast_C124X
cp -r pdfs/T1tttt_Fast_C124Xmore ~/www/FastSim/Nano/T1tttt_Fast_C124Xmore

cp -r pdfs/T1ttttRun3_Fast_C14X/* ~/www/FastSim/Nano/T1ttttRun3_Fast_C14X/

python /afs/desy.de/user/b/beinsam/www/dir_indexer.py /afs/desy.de/user/b/beinsam/www/FastSim/Nano -r -t /afs/desy.de/user/b/beinsam/www/templates/default.html
python tools/bigindexer.py "/afs/desy.de/user/b/beinsam/www/FastSim/Nano/"
====================================


#try to locally develop multi-filer with the goal that it doesnt break using it for simple fast/full comparisons with identical commands as before
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/Fast/*/step3_inNANOAODSIM.root,/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/FastEstatMean"

'''


jobskeleton = '''#!/bin/zsh
source /etc/profile.d/modules.sh
source /afs/desy.de/user/b/beinsam/.bash_profile
module use -a /afs/desy.de/group/cms/modulefiles/
module load cmssw
export THISDIR=$PWD
echo "$QUEUE $JOB $HOST"
cd /nfs/dust/cms/user/beinsam/FastSim/Yash/CMSSW_14_1_X_2024-03-28-1100/src
cmsenv 
cd /nfs/dust/cms/user/beinsam/FastSim/Refinement/CMSSW_12_2_3/src
cd ../../
python3 tools/drawFromNanoAod.py "ARG1" "ARG2"
'''

batchmode = True #usually on
istest = False
dopdfs = False
IsFastFast = True
#python tools/whiphtml.py "pdfs/*.png"
#gROOT.SetBatch(1)

if batchmode: a = 1
else:  fnew = TFile('FastFullEvents.root','recreate')

try: 
	inputnames = sys.argv[1].split(',')[0]
	if len(sys.argv[1].split(','))>1: altdirs =  sys.argv[1].split(',')[1:]
	else: altdirs = []
except: 
    inputnames = '/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/Fast/1*/step3_inNANOAODSIM.root'
    altdir = []

try: drawarg = sys.argv[2]
except: drawarg = ''

print('inputnames', inputnames)
filesfast = glob(inputnames)
if IsFastFast: filesfull = glob(inputnames)
else: filesfull = glob(inputnames.replace('/Fast/','/Full/').replace('/FastGenDecays/','/Full/'))
if istest:
    filesfast = filesfast[:10]
    filesfull = filesfull[:10]    

print('len(filesfast)', len(filesfast))

print ('altdirs', altdirs)
fileslistsalt = []
#for altdir in altdirs: fileslistsalt.append(glob(inputnames.replace('/Fast/','/'+altdir.split('/')[-1]+'/')))
for altdir in altdirs: 
    if istest: fileslistsalt.append(glob(altdir)[:10])
    else: fileslistsalt.append(glob(altdir))


#processname = inputnames.split('CMSSW')[-1].split('/')[2]+'_Fast_C124Xmore'
processname = inputnames.split('CMSSW')[-1].split('/')[2]+'_Fast_C14X'
print('processname', processname)
#processname = 'None'
#if 'TTbar' in firstfname: processname = 'TTbar'
#if 'T1tttt' in firstfname: processname = 'T1tttt'

if not os.path.exists('pdfs/'+processname):
    os.system('mkdir -p '+'pdfs/'+processname)

if IsFastFast and len(fileslistsalt)>0:
    filesfast = fileslistsalt[0]
    fileslistsalt = fileslistsalt[1:]
    
chainfast = TChain('Events')
for ifile, f in enumerate(filesfast):
    if ifile<10: print ('adding', f, 'to fast', '...')
    chainfast.Add(f)
    #if ifile>1000: break
chainfull = TChain('Events')
for ifile, f in enumerate(filesfull):
    if ifile<10: print ('adding', f, 'to full', '...')
    chainfull.Add(f)
    #if ifile>1000: break
    
chainsalt = []
for filelist in fileslistsalt:
    chainsalt.append(TChain('Events'))
    for ifile, f in enumerate(filelist):
        if ifile<10: print ('adding', f, 'to alt', '...')
        chainsalt[-1].Add(f)
    
#if len(chainsalt)>0: print ('alt chain gonna have', chainsalt[-1].GetEntries(), 'entries')

chainfast.Show(0)

leleafies = chainfast.GetListOfBranches()
bnames = []
for b in leleafies:
    bnames.append(b.GetName())
    print (b, 'b.GetName()', b.GetName())

others = ['(GenMET_pt+ChsMET_pt)/2.0','(GenMET_pt+PuppiMET_pt)/2.0','(GenMET_pt+MET_pt)/2.0']
others.extend(['Jet_pt[0]','Jet_pt[1]','Jet_eta[0]','Jet_eta[1]'])
for other in others: bnames.append(other)

print ('we got this many', len(bnames), 'branches')
if not drawarg=='': bnames = [drawarg]

#bnames = others

for name in bnames:
    
    if 'run' in name: continue
    if 'lum' in name: continue
    if 'event' in name: continue
    if 'Nested' in name: continue
    if 'Electron_convVeto' in name: continue
    if 'Electron_cutBased_HEEP' in name: continue
    if istest:
        if not 'MET' in name: continue
    easiername = name.replace('/','Over').replace('(','LPar').replace(')','RPar')
    print ('now doin', name, easiername)
    
    jobcounter = 0
    if batchmode and drawarg=='':
        
        jobname = processname+'_'+str(jobcounter)+'_'+easiername
        jobscript = open('jobs/'+jobname+'.sh','w')
        arg1 = inputnames
        if len(altdirs)>0: arg1 = inputnames+','+','.join(altdirs)
        jobscript.write(jobskeleton.replace('ARG1',arg1).replace('ARG2',name))
        jobscript.close()
        os.chdir('jobs')
        command = 'condor_qsub -cwd '+jobname+'.sh '
        if not jobcounter%10==0: command+=' &'
        jobcounter+=1
        print ('command', command)
        if not istest: os.system(command)
        os.chdir('..')
        if istest: break      
        continue
    
    if 'MET_pt' in name: 
        name2draw = 'min('+name+',1999)'
        print ('updated name to', name2draw)
    else: name2draw = name
    nfull = chainfull.GetEntries()
    print('gonna draw', name2draw)
    chainfull.Draw(name2draw,'1.0/'+str(nfull))
    histfull = chainfull.GetHistogram().Clone('h'+easiername+'_FullSim')
    if IsFastFast: histfull.SetTitle('FastSim') 
    else: histfull.SetTitle('FullSim')    
    #histoStyler(histfull, kBlack)
    histoStylerBigLabels(histfull, kBlack)
    histfull.GetXaxis().SetRange(0, histfull.GetNbinsX() + 1)
    histfull.SetLineWidth(3)
    #histfull.SetMarkerSize(2)

    histfast = histfull.Clone('h'+easiername+'_FastSim')
    if IsFastFast: histfast.SetTitle('FastSim (alt)')
    else: histfast.SetTitle('FastSim')
    histfast.Reset()
    histfast.GetXaxis().SetTitle(histfast.GetXaxis().GetTitle().replace('_pt',' p_{T} [GeV]').replace('_eta',' #eta').replace('_phi',' #phi').replace('_mass',' mass'))
    nfast = chainfast.GetEntries()
    chainfast.Draw(name2draw+'>>'+histfast.GetName(),'1.0/'+str(nfast),'same')
    #histoStyler(histfast, kOrange+1)
    histoStylerBigLabels(histfast, kOrange+1)
    histfast.SetLineWidth(3)
    histfast.GetXaxis().SetRange(0, histfast.GetNbinsX() + 1)

    leg = mklegend(x1=.51, y1=.51, x2=.93, y2=.76, color=kWhite)
    c1 = mkcanvas('c_'+easiername)
    hratio, hpromptmethodsyst = FabDraw(c1,leg,histfast,[histfull],datamc=datamc,lumi='x', title = '', LinearScale=False, fractionthing='Fast / Full')
    pad1, pad2 = hpromptmethodsyst[-2:]
    hratio.SetDirectory(0)
    hratio.GetXaxis().SetTitleSize(0.2)
    hratio.GetXaxis().SetLabelSize(0.17)
    hratio.GetXaxis().SetTitleOffset(0.9)    
    
    hratio.GetYaxis().SetTitleSize(0.18)
    hratio.GetYaxis().SetLabelSize(0.17)    
    hratio.GetYaxis().SetTitleOffset(0.26)
    
    histsalt = []
    ratsalt = []
    for ialt, chainalt in enumerate(chainsalt):
        histalt = histfull.Clone('h'+easiername+'_Alt_'+str(ialt))
        histalt.SetTitle('ALT_'+str(ialt))
        histalt.Reset()
        print ('alt chain', chainalt, 'has entries', chainalt.GetEntries())
        histalt.GetXaxis().SetTitle(histalt.GetXaxis().GetTitle().replace('_pt',' p_{T} [GeV]').replace('_eta',' #eta').replace('_phi',' #phi').replace('_mass',' mass'))
        nalt = chainalt.GetEntries()
        chainalt.Draw(name2draw+'>>'+histalt.GetName(),'1.0/'+str(nalt),'same')
        #histoStyler(histalt, kOrange+1)
        histoStylerBigLabels(histalt, kViolet)
        histsalt.append(histalt)
        pad1.cd()
        leg.AddEntry(histalt, histalt.GetTitle())
        histsalt[-1].Draw('hist same')
        pad2.cd()
        ratalt = histsalt[-1].Clone()
        ratalt.Divide(histfull)
        ratsalt.append(ratalt)
        ratsalt[-1].Draw('hist same')
          
    
    if not batchmode: fnew.cd()
    if not batchmode: c1.Write()
    name = name.replace('(',"LP").replace(')',"RP").replace('/',"Over")
    if not batchmode: 
        pad1.cd()
        pad1.Update()
        pad2.cd()
        pad2.Update()        
        c1.Update()    
        pause()
    if dopdfs: c1.Print('pdfs/'+processname+'/'+name+'.pdf')
    else: c1.Print('pdfs/'+processname+'/'+name+'.png')
    
if not batchmode: print ('just created', fnew.GetName())

