from ROOT import *
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
import os, sys

datamc = 'mc'
lumi = 'X/fb'
from shared_utils import *

styles = [1, kDashed]

surveyNN = True

'''
python3 tools/drawFromSynchEventTree.py output/T1tttt.root && python3 tools/drawFromSynchEventTree.py output/TTbar.root

cp -r pdfs/2022 ~/www/FastSim/TTBarEventsJune27a
python /afs/desy.de/user/b/beinsam/www/dir_indexer.py /afs/desy.de/user/b/beinsam/www/FastSim/ -r -t /afs/desy.de/user/b/beinsam/www/templates/default.html
python tools/bigindexer.py

'''

try: 
	infname = sys.argv[1]
except: 
	infname = 'output/mc_fullfastnn_step3_fromNANOAODSIM.root' 
	infname = 'output/mc_fullfastnn_step3_fromMINIAODSIM.root' 
fFastFull = TFile(infname)
tFastFull = fFastFull.Get('tEvent')
tFastFull.Show(0)

univsel = "1==1"

#newfile = TFile('newfile_from'+infname.split('_from')[-1].split('.root')[0]+'.root','recreate')
newfile = TFile('newfile_from'+infname.split('/')[-1],'recreate')

args = ['min(Met_FastSim,1199)>>hadc(25,0,1200)','min(Mht_FastSim,1199)>>hadc(25,0,1200)']
for arg in args:
    c1 = mkcanvas(arg)
    tFastFull.Draw(arg, univsel)
    hFast = tFastFull.GetHistogram().Clone('hFast')
    hFast.SetTitle('FastSim t#bar{t}+jets (2016 C10-6)')
    hFast.GetXaxis().SetTitle(arg)
    hFast.GetYaxis().SetTitle('number of events')
    histoStyler(hFast, kTeal-5)
    hFast.SetLineWidth(4)

    tFastFull.Draw(arg.replace('Fast','Full'),univsel)
    hFull = tFastFull.GetHistogram().Clone('hFull')
    hFull.SetTitle('FullSim t#bar{t}+jets (2016 C10-6)')
    hFull.GetXaxis().SetTitle(arg)
    hFull.GetYaxis().SetTitle('number of events')
    histoStyler(hFull, kBlack)
    hFull.SetLineWidth(4)
    
    if surveyNN:
        
        tFastFull.Draw(arg.replace('FastSim','NnSplice'),univsel)
        hNnSplice = tFastFull.GetHistogram().Clone('hNnSplice')
        hNnSplice.SetTitle('NN-corrected FastSim')
        hNnSplice.GetXaxis().SetTitle(arg)
        hNnSplice.GetYaxis().SetTitle('number of events')
        histoStyler(hNnSplice, kRed+1)
        hNnSplice.SetLineWidth(4)
        
        
        tFastFull.Draw(arg.replace('FastSim','GenSmear'),univsel)
        hGenSmear = tFastFull.GetHistogram().Clone('hGenSmear')
        hGenSmear.SetTitle('GEN-smear with NN')
        hGenSmear.GetXaxis().SetTitle(arg)
        hGenSmear.SetLineWidth(4)
        hGenSmear.GetYaxis().SetTitle('number of events')
        histoStyler(hGenSmear, kViolet)
        hGenSmear.SetLineWidth(4)
    
    ##tFastFull.Draw(arg.replace('FastSim','Gen'),univsel)
    ##hGen = tFastFull.GetHistogram().Clone('hGen')
    ##hGen.SetTitle('GEN')
    ##hGen.GetXaxis().SetTitle(arg)
    ##hGen.GetYaxis().SetTitle('number of events')
    ##histoStyler(hGen, kOrange)
    ##hGen.SetLineWidth(4)
    

    #tFastFull.Draw(arg.replace('Met_FastSim','(Met_FastSim+Met_Gen)/2').replace('Mht_FastSim','(Mht_FastSim+Mht_Gen)/2'),univsel)
    #hGenAvgd = tFastFull.GetHistogram().Clone('hGenAvgd')
    #hGenAvgd.SetTitle('GEN-RECO average')
    #hGenAvgd.GetXaxis().SetTitle(arg)
    #hGenAvgd.GetYaxis().SetTitle('number of events')
    #histoStyler(hGenAvgd, kBlue+1)     
    #hGenAvgd.SetLineWidth(4)
    
    
    #tFastFull.Draw(arg.replace('FastSim','GenSplice'),univsel)
    #hGenSplice = tFastFull.GetHistogram().Clone('hGenSplice')
    #hGenSplice.SetTitle('GEN-splice')
    #hGenSplice.GetXaxis().SetTitle(arg)
    #hGenSplice.GetYaxis().SetTitle('number of events')
    #histoStyler(hGenSplice, kGray+1)     
    #hGenSplice.SetLineWidth(4)


    leg = mklegend(0.14,0.05,0.59,0.36)
    hratio, hpromptmethodsyst = FabDrawSystyRatio(c1,leg,hFast,[hFull],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='Fast/Full')
    hratio.GetYaxis().SetRangeUser(0.7,1.3)
    if 'Met' in arg: hratio.GetXaxis().SetTitle('E_{T}^{miss} [GeV]')
    else: hratio.GetXaxis().SetTitle('H_{T}^{miss} [GeV]')
    newfile.cd()

    pad1, pad2 = hpromptmethodsyst[-2:]
    pad1.cd()
    hFull.Draw("hist same")
    if surveyNN:
        hNnSplice.Draw("hist same")
        leg.AddEntry(hNnSplice, hNnSplice.GetTitle())
        hGenSmear.Draw("hist same")    
        leg.AddEntry(hGenSmear, hGenSmear.GetTitle())
    ##hGen.Draw("hist same")    
    ##leg.AddEntry(hGen, hGen.GetTitle())   
    #hGenSplice.Draw("hist same e")    
    #leg.AddEntry(hGenSplice, hGenSplice.GetTitle())        
    #hGenAvgd.Draw("hist same e")    
    #leg.AddEntry(hGenAvgd, hGenAvgd.GetTitle())            
    #pad1.Update()
    pad2.cd()
    if surveyNN:
        hratNnSplice = hNnSplice.Clone('hratNnSplice')
        hratNnSplice.Divide(hFull)
        hratNnSplice.Draw('hist same')
        hratGenSmear = hGenSmear.Clone('hratGenSmear')
        hratGenSmear.Divide(hFull)    
        hratGenSmear.SetMarkerStyle(22)
        hratGenSmear.SetLineWidth(3)        
        hratGenSmear.Draw('same hist p e')
        hFast.Draw('same')
    ##hratGen = hGen.Clone('hratGen')
    ##hratGen.Divide(hFull)    
    ##hratGen.Draw('same hist')
    #hratGenSplice = hGenSplice.Clone('hratGenSplice')
    #hratGenAvgd = hGenAvgd.Clone('hratGenAvgd')
    #hratGenAvgd.Divide(hFull)    
    #hratGenAvgd.Draw('same hist e')    
    #pad2.Update()

    c1.Update()
    c1.Write(arg.split(',')[0].replace('min(',''))
    c1.Print(arg.split(',')[0].replace('min(','')+infname.split('/')[-1].split('.root')[0]+'.png')
    #pause()


print ('just created', newfile.GetName())
newfile.Close()
