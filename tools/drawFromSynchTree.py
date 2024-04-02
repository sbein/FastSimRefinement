'''
#python3 tools/drawFromSynchTree.py output/mc_fullfastnn_step3_fromMINIAODSIM_Pt15Eta2p4.root 
python3 tools/drawFromSynchTree.py Regress/FestOutput/output_refinement_regression_20240305.root

#jet
mkdir ~/www/FastSim/Refinement/Run3Big2SidedLR5em10FewTrans/
rm plots/refinement/jet/*
python3 tools/drawFromSynchTree.py Regress/TrainingOutput/output_refineJet_regression_20240306.root
rm ~/www/FastSim/Refinement/Run3Big2SidedLR5em10FewTrans/*
cp plots/refinement/jet/* ~/www/FastSim/Refinement/Run3Big2SidedLR5em10FewTrans/

#electron
mkdir ~/www/FastSim/Refinement/Run3Big2SidedLR5em10FewTrans/
python3 tools/drawFromSynchTree.py Regress/TrainingOutput/output_refineElectron_regression_202403261114.root 
cp plots/refinement/electron/* ~/www/FastSim/Refinement/Run3Big2SidedLR5em10FewTrans/
cp Regress/plotting/plots/*RecElectron* ~/www/FastSim/Refinement/Run3Big2SidedLR5em10FewTrans/
cp Regress/trainRegression_Electron.py ~/www/FastSim/Refinement/Run3Big2SidedLR5em10FewTrans/ && python /afs/desy.de/user/b/beinsam/www/dir_indexer.py /afs/desy.de/user/b/beinsam/www/FastSim/Refinement/ -r -t /afs/desy.de/user/b/beinsam/www/templates/default.html && python tools/bigindexer.py "/afs/desy.de/user/b/beinsam/www/FastSim/Refinement/"


#muon
mkdir ~/www/FastSim/Refinement/Run3Big2SidedLR5em10FewTrans/
rm plots/refinement/muon/*
python3 tools/drawFromSynchTree.py Regress/TrainingOutput/output_refineMuon_regression_202404021318.root 
cp plots/refinement/muon/* ~/www/FastSim/Refinement/Run3Big2SidedLR5em10FewTrans/
cp Regress/plotting/plots/*Muon* ~/www/FastSim/Refinement/Run3Big2SidedLR5em10FewTrans/
cp Regress/trainRegression_Muon.py ~/www/FastSim/Refinement/Run3Big2SidedLR5em10FewTrans/ && python /afs/desy.de/user/b/beinsam/www/dir_indexer.py /afs/desy.de/user/b/beinsam/www/FastSim/Refinement/ -r -t /afs/desy.de/user/b/beinsam/www/templates/default.html && python tools/bigindexer.py "/afs/desy.de/user/b/beinsam/www/FastSim/Refinement/"




python /afs/desy.de/user/b/beinsam/www/dir_indexer.py /afs/desy.de/user/b/beinsam/www/FastSim/Refinement/ -r -t /afs/desy.de/user/b/beinsam/www/templates/default.html && python tools/bigindexer.py "/afs/desy.de/user/b/beinsam/www/FastSim/Refinement/"

'''

from ROOT import *
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
import os, sys

datamc = 'mc'
lumi = 'X/fb'
from shared_utils import *

styles = [1, kDashed]

try:  infname = sys.argv[1]
except: 
	infname = 'output/mc_fullfastnn_step3_fromNANOAODSIM.root' 
	infname = 'output/mc_fullfastnn_step3_fromMINIAODSIM.root' 
	
refinedobject = infname.split('output_')[-1].split('_regression')[0].replace('refine','')
treename = 't'+refinedobject
print('treename', treename)

fFastFull = TFile(infname)
tFastFull = fFastFull.Get(treename)
tFastFull.Show(0)
#univsel = "GenJet_pt>30 && GenJet_pt<100 && abs(GenJet_eta)<1.4"
univsel = "1"
if refinedobject=='Muon':
    print('we are here')
    univsel = "RecMuon_mvaMuID_FastSim > -1 && RecMuon_mvaMuID_FullSim > -1 && RecMuon_softMva_FastSim > -0.9 && RecMuon_softMva_FullSim > -1"


newfile = TFile('newfile_from'+infname.split('/')[-1].split('_from')[-1].split('.root')[0]+'.root','recreate')

#args = ['min(JetResponse_FastSim,2.9)>>hadc(40,0,3)']
branches = [br.GetName() for br in tFastFull.GetListOfBranches() if '_FastSim' in br.GetName()]
args = []

for br in branches:
    if 'hadronFlavour' in br: 
        continue
    tFastFull.Draw(br.replace('FastSim','FullSim') + ">>tempHist(100)", univsel, "goff")
    tempHist = gDirectory.Get("tempHist")

    # Calculate 10th and 90th percentiles
    quantiles = [0.01, 0.99]
    quantiles = [0.05, 0.95]    
    #quantiles = [0.00, 1.0]
    qValues = array('d', [0.0, 0.0])  # Array to store quantile values
    tempHist.GetQuantiles(2, qValues, array('d', quantiles))
    print('qValues', qValues)
    if qValues[0]>0 and qValues[1]<1: 
        qValues[0], qValues[1] = 0,1
    
    # Define the modified observable using min and max functions
    modified_br = "min(max({},{}),{})".format(br, qValues[0], qValues[1])
    # Now set histogram edges to quantile values explicitly
    draw_command = "{}>>h{}(50,{},{})".format(modified_br, br, qValues[0]-epsilon, qValues[1]+epsilon)

    print('Drawing', br, 'modified to be within', qValues[0], 'and', qValues[1], 'with explicit histogram edges.')

    args.append((draw_command, br))  # Store the draw command and original branch name
    

for draw_command, br in args:
    c1 = mkcanvas(br)  # Use the original branch name for canvas creation
    xtit = br.replace('_FastSim','')#'_'.join(br.split('_')[:-3])

    tFastFull.Draw(draw_command, univsel, "goff")
    hFast = tFastFull.GetHistogram().Clone('hFast'+br)
    hFast.SetTitle('FastSim t#bar{t}+jets (2016 C10-6)')
    hFast.GetXaxis().SetTitle(xtit)
    hFast.GetYaxis().SetTitle('number of events')
    histoStyler(hFast, kTeal-5)

    tFastFull.Draw(draw_command.replace('Fast','Full'), univsel, "goff")
    hFull = tFastFull.GetHistogram().Clone('hFull')
    hFull.SetTitle('FullSim t#bar{t}+jets (2016 C10-6)')
    hFull.GetXaxis().SetTitle(xtit)
    hFull.GetYaxis().SetTitle('number of events')
    hFull.GetYaxis().SetTitleSize(0.15)
    histoStyler(hFull, kYellow+1)
    
    tFastFull.Draw(draw_command.replace('FastSim','Refined'), univsel, "goff")
    hFastRefined = tFastFull.GetHistogram().Clone('hFastRefined')
    hFastRefined.SetTitle('Refined FastSim')
    hFastRefined.GetXaxis().SetTitle(xtit)
    hFastRefined.GetYaxis().SetTitle('number of events')
    histoStyler(hFastRefined, kViolet+1)

    
    leg = mklegend(0.17,0.62,0.61,0.9)
    hratio, hpromptmethodsyst = FabDraw(c1,leg,hFast,[hFull],datamc=datamc,lumi=lumi, title = 'Entries / bin', LinearScale=False, fractionthing='Fast / FullSim')
    hratio.GetYaxis().SetRangeUser(0.5,1.5)
    #hratio.GetYaxis().SetRangeUser(-0.5,2.0)    
    hratio.GetXaxis().SetTitle(xtit)
    hratio.GetYaxis().SetTitleSize(0.15)
    hratio.GetYaxis().SetTitleOffset(0.2)
    hratio.GetXaxis().SetTitleSize(0.15)
    newfile.cd()

    pad1, pad2 = hpromptmethodsyst[-2:]
    pad1.cd()
    hFull.Draw("hist same")
    hFast.Draw("p same")
    hFastRefined.SetMarkerStyle(23)
    hFastRefined.Draw("p same")
    leg.AddEntry(hFastRefined, hFastRefined.GetTitle())


    #pad1.Update()
    pad2.cd()
    hratRefined = hFastRefined.Clone('hRatioRefined')
    hratRefined.Divide(hFull)
    hratRefined.Draw('p same')
    #pad2.Update()

    c1.Update()
    plotname = br.split(',')[0].replace('min(','').split('>>')[0].replace('_FastSim','')
    c1.Write(plotname)
    c1.Print('plots/refinement/'+refinedobject.lower()+'/'+plotname+'.png')
    #pause()


print ('just created', newfile.GetName())
newfile.Close()
