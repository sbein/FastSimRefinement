from ROOT import *
from shared_utils import *


ShouldPauseAndDrawLive = True


if not ShouldPauseAndDrawLive: gROOT.SetBatch(1)

fin = TFile('/nfs/dust/cms/user/beinsam/FastSim/Refinement/output/mc_fullfastnn_step3_fromMINIAODSIM_Pt30Eta2p4.root')
tJet = fin.Get('tJet')

c1 = TCanvas()
c1.SetLogz()
c1.SetGridx()
c1.SetGridy()

tJet.Draw("JetDrGenRec_FullSim:min(600,GenJetPt)","","colz")
hDrVsPt = tJet.GetHistogram().Clone('hDrVsPt')
hDrVsPt = normalizeTh2Columnarly(hDrVsPt)
hDrVsPt.Draw('colz')
f1 = TF1('f1','10/x+0.02',0,600)
f1.Draw('same')
c1.Update()
if ShouldPauseAndDrawLive: pause()


    