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
python3 tools/drawFromNanoAod.py "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/T1tttt/Fast/*/step3_inNANOAODSIM.root,/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/FastEstatMean"
#...

rm -rf ~/www/FastSim/Nano/6July2022/
cp -r pdfs/T1tttt ~/www/FastSim/Nano/6July2022/T1tttt_9_4_11
cp -r pdfs/TTbar ~/www/FastSim/Nano/6July2022/TTbar_12_2_XDev
cp -r pdfs/T1tttt ~/www/FastSim/Nano/6July2022/T1tttt_12_2_XDev
cp -r pdfs/TTbar ~/www/FastSim/Nano/6July2022/TTbar_9_4_11
cp -r pdfs/MuGun1100 ~/www/FastSim/Nano/6July2022/MuGun1100
cp -r pdfs/MuGun1200 ~/www/FastSim/Nano/6July2022/MuGun1200
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
cd /nfs/dust/cms/user/beinsam/FastSim/Refinement/CMSSW_12_2_3/src
cmsenv 
cd ../../
python3 tools/drawFromNanoAod.py "ARG1" "ARG2"
'''

batchmode = True
istest = False
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

filesfast = glob(inputnames)
filesfull = glob(inputnames.replace('/Fast/','/Full/'))


print ('altdirs', altdirs)
fileslistsalt = []
#for altdir in altdirs: fileslistsalt.append(glob(inputnames.replace('/Fast/','/'+altdir.split('/')[-1]+'/')))
for altdir in altdirs: fileslistsalt.append(glob(altdir))


firstfname = filesfast[0]
processname = inputnames.split('CMSSW')[-1].split('/')[2]
#processname = 'None'
#if 'TTbar' in firstfname: processname = 'TTbar'
#if 'T1tttt' in firstfname: processname = 'T1tttt'

if not os.path.exists('pdfs/'+processname):
    os.system('mkdir -p '+'pdfs/'+processname)

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
    chainfull.Draw(name2draw)
    histfull = chainfull.GetHistogram().Clone('h'+easiername+'_FullSim')
    histfull.SetTitle('FullSim')    
    #histoStyler(histfull, kBlack)
    histoStylerBigLabels(histfull, kBlack)
    histfull.GetXaxis().SetRange(0, histfull.GetNbinsX() + 1)
    histfull.SetLineWidth(3)

    histfast = histfull.Clone('h'+easiername+'_FastSim')
    histfast.SetTitle('FastSim')
    histfast.Reset()
    histfast.GetXaxis().SetTitle(histfast.GetXaxis().GetTitle().replace('_pt',' p_{T} [GeV]').replace('_eta',' #eta').replace('_phi',' #phi').replace('_mass',' mass'))
    chainfast.Draw(name2draw+'>>'+histfast.GetName(),'','same')
    #histoStyler(histfast, kOrange+1)
    histoStylerBigLabels(histfast, kOrange+1)
    histfast.GetXaxis().SetRange(0, histfast.GetNbinsX() + 1)

    leg = mklegend(x1=.49, y1=.46, x2=.89, y2=.62, color=kWhite)
    c1 = mkcanvas('c_'+easiername)
    hratio, hpromptmethodsyst = FabDraw(c1,leg,histfast,[histfull],datamc=datamc,lumi='x', title = '', LinearScale=False, fractionthing='Fast / Full')
    pad1, pad2 = hpromptmethodsyst[-2:]
    hratio.SetDirectory(0)
    hratio.GetXaxis().SetTitleSize(0.2)
    hratio.GetXaxis().SetLabelSize(0.18)
    hratio.GetXaxis().SetTitleOffset(0.9)    
    
    hratio.GetYaxis().SetTitleSize(0.2)
    hratio.GetYaxis().SetLabelSize(0.18)    
    hratio.GetYaxis().SetTitleOffset(0.26)
    
    histsalt = []
    ratsalt = []
    for ialt, chainalt in enumerate(chainsalt):
        histalt = histfull.Clone('h'+easiername+'_Alt_'+str(ialt))
        histalt.SetTitle('ALT_'+str(ialt))
        histalt.Reset()
        print ('alt chain', chainalt, 'has entries', chainalt.GetEntries())
        histalt.GetXaxis().SetTitle(histalt.GetXaxis().GetTitle().replace('_pt',' p_{T} [GeV]').replace('_eta',' #eta').replace('_phi',' #phi').replace('_mass',' mass'))
        chainalt.Draw(name2draw+'>>'+histalt.GetName(),'','same')
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
    c1.Print('pdfs/'+processname+'/'+name+'.png')
    
if not batchmode: print ('just created', fnew.GetName())

