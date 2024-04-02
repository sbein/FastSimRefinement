'''
cd /nfs/dust/cms/user/beinsam/FastSim/Refinement/CMSSW_12_2_3/src/
cmsenv 
cd ../../
python3 tools/makeSynchTreesFromNANO.py --fnamekeyword "/nfs/dust/cms/user/beinsam/FastSim/Refinement/TrainingSamples/CMSSW_13_0_13/src/TTbarRun3/Fast/*/*NANO.root"
python3 tools/makeSynchTreesFromNANO.py --fnamekeyword "/nfs/dust/cms/user/beinsam/FastSim/Refinement/TrainingSamples/CMSSW_13_0_13/src/T1ttttRun3/Fast/1234/*NANO.root"
'''
#! /usr/bin/env python
from shared_utils import *
import sys
from glob import glob
import os, sys
import numpy as np
from DataFormats.FWLite import Events, Handle
from ROOT import *
        
gROOT.SetStyle('Plain') 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-fin", "--fnamekeyword", type=str,default='/nfs/dust/cms/user/beinsam/FastSim/CMSSW_10_6_22/src/TTbar/Fast/*/step3_inNANOAODSIM.root',help="file")
parser.add_argument("-nfpj", "--nfpj", type=int, default=1)
parser.add_argument("-emod2", "--emod2", type=int, default=0)
parser.add_argument("-outdir", "--outdir", type=str, default='output/smallchunks')
args = parser.parse_args()
fnamekeyword = args.fnamekeyword.strip()
nfpj = args.nfpj
emod2 = args.emod2
fastsimlist = glob(fnamekeyword)
sorted(fastsimlist)
fullsimlist = glob(fnamekeyword.replace('/Fast/','/Full/').replace('/FastEstatMean/','/Full/').replace('/FastGenDecays/','/Full/'))
sorted(fullsimlist)
      
##The following 2 lines are absolutely necessary to avoid a terrible seg fault. thank goodness I found them after weeks of wandering in the desert. 
fTest = TFile('/nfs/dust/cms/user/beinsam/FastSim/CMSSW_10_6_22/src/TTbar/Fast/705/step3_inNANOAODSIM.root')
fTest.Close()
methodTMVA = 'MLPBNN'
reader = TMVA.Reader("")
reader.SetName('reader')
from array import array
_GenJet_pt_ = array('f',[50])
_GenJet_eta_ = array('f',[1])
_GenJet_phi_ = array('f',[1])
_GenJet_mass_ = array('f',[1])
_JetResponse_ = array('f',[0.0])
thingy = 'Lr10m3Tanh512HiddenLayers7NCycles600NTrain5000000'
reader.AddVariable("GenJetPt",_GenJet_pt_)          
reader.AddVariable("abs(GenJetEta)",_GenJet_eta_)
reader.AddVariable("JetResponse",_JetResponse_)
reader.BookMVA(methodTMVA, 'datasets/dataset'+thingy+'/weights/TMVAClassification_'+methodTMVA+'.weights.xml')
fv = np.array([0,0,0],'d')
def mlpresponse(x, pt, eta):
    _JetResponse_[0] = x   
    _GenJet_pt_[0] = pt
    _GenJet_eta_[0] = eta
    mlp = reader.EvaluateMVA(methodTMVA)
    calib = 1#gcalib.Eval(mlp) 
    out = mlp*calib
    return out/(1-out)
print (mlpresponse(1.2, 50.0, 2.1))
def rejection_sampler(p, pt, eta, xbounds):
    pmax = p(1, pt, eta)
    width = xbounds[1]-xbounds[0]
    while True:
        x = np.random.rand(1)*width+xbounds[0]
        y = np.random.rand(1)*pmax
        if y<=p(x, pt, eta):
            return x                 
innstub = '_'.join(fastsimlist[0].split('/')[-2:]).replace('.root','')
def main():
    name = 'mc_fullfastnn_'+innstub+'_fromNANO.root'
    name = name.replace('.root.root','.root')
    name = name.replace('.root','_Ootb.root')
    if emod2==1: name = name.replace('.root','_ForTraining.root')
    if emod2==2: name = name.replace('.root','_ForTesting.root')    
    fnew = TFile(name,'recreate')
        
    tJet = TTree('tJet','tJet')
    container_GenJet_pt = np.zeros(1,dtype=float)    
    tJet.Branch('GenJet_pt', container_GenJet_pt,'GenJet_pt/D')
    container_GenJet_eta = np.zeros(1,dtype=float)
    tJet.Branch('GenJet_eta', container_GenJet_eta,'GenJet_eta/D')
    container_GenJet_phi = np.zeros(1,dtype=float)
    tJet.Branch('GenJet_phi', container_GenJet_phi,'GenJet_phi/D')    
    container_GenJet_mass = np.zeros(1,dtype=float)
    tJet.Branch('GenJet_mass', container_GenJet_mass,'GenJet_mass/D')        
    container_GenJet_hadronFlavour = np.zeros(1,dtype=int)
    tJet.Branch('GenJet_hadronFlavour', container_GenJet_hadronFlavour,'GenJet_hadronFlavour/I')
    container_GenJet_partonFlavour = np.zeros(1,dtype=int)
    tJet.Branch('GenJet_partonFlavour', container_GenJet_partonFlavour,'GenJet_partonFlavour/I')
    container_JetDrGenRec = np.zeros(1,dtype=float)    
    tJet.Branch('JetDrGenRec', container_JetDrGenRec,'JetDrGenRec/D')

    jetvars = ["Jet_area","Jet_btagDeepFlavB","Jet_btagDeepFlavCvB","Jet_btagDeepFlavCvL","Jet_btagDeepFlavQG","Jet_btagRobustParTAK4B","Jet_btagRobustParTAK4CvB","Jet_btagRobustParTAK4CvL","Jet_btagRobustParTAK4QG","Jet_chEmEF","Jet_chHEF","Jet_eta","Jet_hfsigmaEtaEta","Jet_hfsigmaPhiPhi","Jet_mass","Jet_muEF","Jet_muonSubtrFactor","Jet_neEmEF","Jet_neHEF","Jet_phi","Jet_pt","Jet_rawFactor", 'Jet_hadronFlavour']
    container_jetvars_full = {}    
    container_jetvars_fast = {}
    for jetvar in jetvars:
        if '_n' in jetvar and not '_ne' in jetvar:
            container_jetvars_full[jetvar] = np.zeros(1,dtype=int)            
            container_jetvars_fast[jetvar] = np.zeros(1,dtype=int)        
            tJet.Branch('Rec'+jetvar+'_FullSim', container_jetvars_full[jetvar], 'Rec'+jetvar+'_FullSim'+'/I')
        else:
            container_jetvars_full[jetvar] = np.zeros(1,dtype=float)
            container_jetvars_fast[jetvar] = np.zeros(1,dtype=float)
            tJet.Branch('Rec'+jetvar+'_FullSim', container_jetvars_full[jetvar] ,'Rec'+jetvar+'_FullSim'+'/D')
            tJet.Branch('Rec'+jetvar+'_FastSim', container_jetvars_fast[jetvar] ,'Rec'+jetvar+'_FastSim'+'/D')
    container_JetResponse_FullSim = np.zeros(1,dtype=float)
    tJet.Branch('JetResponse_FullSim', container_JetResponse_FullSim,'JetResponse_FullSim/D')    
    container_JetResponse_FastSim = np.zeros(1,dtype=float)    
    tJet.Branch('JetResponse_FastSim', container_JetResponse_FastSim,'JetResponse_FastSim/D')
    container_JetResponse_Nn = np.zeros(1,dtype=float)    
    tJet.Branch('JetResponse_Nn', container_JetResponse_Nn,'JetResponse_Nn/D')
    container_JetDrGenRec_FastSim = np.zeros(1,dtype=float)    
    tJet.Branch('JetDrGenRec_FastSim', container_JetDrGenRec_FastSim,'JetDrGenRec_FastSim/D')    
    container_JetDrGenRec_FullSim = np.zeros(1,dtype=float)    
    tJet.Branch('JetDrGenRec_FullSim', container_JetDrGenRec_FullSim,'JetDrGenRec_FullSim/D')    

    tMuon = TTree('tMuon', 'tMuon')
    container_GenMuon_pt = np.zeros(1,dtype=float)    
    tMuon.Branch('GenMuon_pt', container_GenMuon_pt,'GenMuon_pt/D')
    container_GenMuon_eta = np.zeros(1,dtype=float)
    tMuon.Branch('GenMuon_eta', container_GenMuon_eta,'GenMuon_eta/D')
    container_GenMuon_phi = np.zeros(1,dtype=float)
    tMuon.Branch('GenMuon_phi', container_GenMuon_phi,'GenMuon_phi/D')    
    muonvars = ["Muon_dxy","Muon_dxyErr","Muon_dxybs","Muon_dz","Muon_dzErr","Muon_eta","Muon_ip3d","Muon_jetPtRelv2","Muon_jetRelIso","Muon_mass","Muon_miniPFRelIso_all","Muon_miniPFRelIso_chg","Muon_mvaMuID","Muon_pfRelIso03_all","Muon_pfRelIso03_chg","Muon_pfRelIso04_all","Muon_phi","Muon_pt","Muon_ptErr","Muon_segmentComp","Muon_sip3d","Muon_softMva","Muon_tkRelIso","Muon_tunepRelPt","Muon_bsConstrainedChi2","Muon_bsConstrainedPt","Muon_bsConstrainedPtErr","Muon_mvaLowPt","Muon_mvaTTH"]
    container_muonvars_full = {}
    container_muonvars_fast = {}
    for muonvar in muonvars:
        dtype = float
        if muonvar in ["Muon_charge", "Muon_looseId"]:
            dtype = int
        container_muonvars_full[muonvar] = np.zeros(1, dtype=dtype)
        container_muonvars_fast[muonvar] = np.zeros(1, dtype=dtype)
        tMuon.Branch('Rec'+muonvar+'_FullSim', container_muonvars_full[muonvar], 'Rec'+muonvar+'_FullSim' + ('/I' if dtype == int else '/D'))
        tMuon.Branch('Rec'+muonvar+'_FastSim', container_muonvars_fast[muonvar], 'Rec'+muonvar+'_FastSim' + ('/I' if dtype == int else '/D'))
    container_MuonResponse_FullSim = np.zeros(1,dtype=float)
    tMuon.Branch('RecMuonResponse_FullSim', container_MuonResponse_FullSim,'RecMuonResponse_FullSim/D')    
    container_MuonResponse_FastSim = np.zeros(1,dtype=float)    
    tMuon.Branch('RecMuonResponse_FastSim', container_MuonResponse_FastSim,'RecMuonResponse_FastSim/D')
    container_MuonDrGenRec_FastSim = np.zeros(1,dtype=float)    
    tMuon.Branch('RecMuonDrGenRec_FastSim', container_MuonDrGenRec_FastSim,'RecMuonDrGenRec_FastSim/D')    
    container_MuonDrGenRec_FullSim = np.zeros(1,dtype=float)    
    tMuon.Branch('RecMuonDrGenRec_FullSim', container_MuonDrGenRec_FullSim,'RecMuonDrGenRec_FullSim/D')
    
    
    tElectron = TTree('tElectron', 'tElectron')
    container_GenElectron_pt = np.zeros(1,dtype=float)    
    tElectron.Branch('GenElectron_pt', container_GenElectron_pt,'GenElectron_pt/D')
    container_GenElectron_eta = np.zeros(1,dtype=float)
    tElectron.Branch('GenElectron_eta', container_GenElectron_eta,'GenElectron_eta/D')
    container_GenElectron_phi = np.zeros(1,dtype=float)
    tElectron.Branch('GenElectron_phi', container_GenElectron_phi,'GenElectron_phi/D')    
    electronvars = ["Electron_dxy","Electron_dxyErr","Electron_dz","Electron_dzErr","Electron_eInvMinusPInv","Electron_energyErr","Electron_eta","Electron_hoe","Electron_ip3d","Electron_jetPtRelv2","Electron_jetRelIso","Electron_mass","Electron_miniPFRelIso_all","Electron_miniPFRelIso_chg","Electron_mvaHZZIso","Electron_mvaIso","Electron_mvaNoIso","Electron_pfRelIso03_all","Electron_pfRelIso03_chg","Electron_phi","Electron_pt","Electron_r9","Electron_scEtOverPt","Electron_sieie","Electron_sip3d","Electron_mvaTTH"]
    container_electronvars_full = {}
    container_electronvars_fast = {}
    for electronvar in electronvars:
        dtype = float
        if electronvar in ["Electron_charge", "Electron_looseId"]:
            dtype = int
        container_electronvars_full[electronvar] = np.zeros(1, dtype=dtype)
        container_electronvars_fast[electronvar] = np.zeros(1, dtype=dtype)
        tElectron.Branch('Rec'+electronvar+'_FullSim', container_electronvars_full[electronvar], 'Rec'+electronvar+'_FullSim' + ('/I' if dtype == int else '/D'))
        tElectron.Branch('Rec'+electronvar+'_FastSim', container_electronvars_fast[electronvar], 'Rec'+electronvar+'_FastSim' + ('/I' if dtype == int else '/D'))
    container_ElectronResponse_FullSim = np.zeros(1,dtype=float)
    tElectron.Branch('RecElectronResponse_FullSim', container_ElectronResponse_FullSim,'RecElectronResponse_FullSim/D')    
    container_ElectronResponse_FastSim = np.zeros(1,dtype=float)    
    tElectron.Branch('RecElectronResponse_FastSim', container_ElectronResponse_FastSim,'RecElectronResponse_FastSim/D')
    container_ElectronDrGenRec_FastSim = np.zeros(1,dtype=float)    
    tElectron.Branch('RecElectronDrGenRec_FastSim', container_ElectronDrGenRec_FastSim,'RecElectronDrGenRec_FastSim/D')    
    container_ElectronDrGenRec_FullSim = np.zeros(1,dtype=float)    
    tElectron.Branch('RecElectronDrGenRec_FullSim', container_ElectronDrGenRec_FullSim,'RecElectronDrGenRec_FullSim/D')      
    
    tPhoton = TTree('tPhoton', 'tPhoton')
    container_GenPhoton_pt = np.zeros(1,dtype=float)    
    tPhoton.Branch('GenPhoton_pt', container_GenPhoton_pt,'GenPhoton_pt/D')
    container_GenPhoton_eta = np.zeros(1,dtype=float)
    tPhoton.Branch('GenPhoton_eta', container_GenPhoton_eta,'GenPhoton_eta/D')
    container_GenPhoton_phi = np.zeros(1,dtype=float)
    tPhoton.Branch('GenPhoton_phi', container_GenPhoton_phi,'GenPhoton_phi/D')    
    photonvars = ["Photon_ecalPFClusterIso","Photon_energyErr","Photon_energyRaw","Photon_esEffSigmaRR","Photon_esEnergyOverRawE","Photon_eta","Photon_etaWidth","Photon_haloTaggerMVAVal","Photon_hcalPFClusterIso","Photon_hoe","Photon_hoe_PUcorr","Photon_mvaID","Photon_pfChargedIso","Photon_pfChargedIsoPFPV","Photon_pfChargedIsoWorstVtx","Photon_pfPhoIso03","Photon_pfRelIso03_all_quadratic","Photon_pfRelIso03_chg_quadratic","Photon_phi","Photon_phiWidth","Photon_pt","Photon_r9","Photon_s4","Photon_sieie","Photon_sieip","Photon_sipip","Photon_trkSumPtHollowConeDR03","Photon_trkSumPtSolidConeDR04","Photon_x_calo","Photon_y_calo","Photon_z_calo"]
    container_photonvars_full = {}
    container_photonvars_fast = {}
    for photonvar in photonvars:
        dtype = float
        if photonvar in ["Photon_charge", "Photon_looseId"]:
            dtype = int
        container_photonvars_full[photonvar] = np.zeros(1, dtype=dtype)
        container_photonvars_fast[photonvar] = np.zeros(1, dtype=dtype)
        tPhoton.Branch('Rec'+photonvar+'_FullSim', container_photonvars_full[photonvar], 'Rec'+photonvar+'_FullSim' + ('/I' if dtype == int else '/D'))
        tPhoton.Branch('Rec'+photonvar+'_FastSim', container_photonvars_fast[photonvar], 'Rec'+photonvar+'_FastSim' + ('/I' if dtype == int else '/D'))
    container_PhotonResponse_FullSim = np.zeros(1,dtype=float)
    tPhoton.Branch('RecPhotonResponse_FullSim', container_PhotonResponse_FullSim,'RecPhotonResponse_FullSim/D')    
    container_PhotonResponse_FastSim = np.zeros(1,dtype=float)    
    tPhoton.Branch('RecPhotonResponse_FastSim', container_PhotonResponse_FastSim,'RecPhotonResponse_FastSim/D')
    container_PhotonDrGenRec_FastSim = np.zeros(1,dtype=float)    
    tPhoton.Branch('RecPhotonDrGenRec_FastSim', container_PhotonDrGenRec_FastSim,'RecPhotonDrGenRec_FastSim/D')    
    container_PhotonDrGenRec_FullSim = np.zeros(1,dtype=float)    
    tPhoton.Branch('RecPhotonDrGenRec_FullSim', container_PhotonDrGenRec_FullSim,'RecPhotonDrGenRec_FullSim/D')  
    
    tTau = TTree('tTau', 'tTau')
    container_GenTau_pt = np.zeros(1,dtype=float)    
    tTau.Branch('GenTau_pt', container_GenTau_pt,'GenTau_pt/D')
    container_GenTau_eta = np.zeros(1,dtype=float)
    tTau.Branch('GenTau_eta', container_GenTau_eta,'GenTau_eta/D')
    container_GenTau_phi = np.zeros(1,dtype=float)
    tTau.Branch('GenTau_phi', container_GenTau_phi,'GenTau_phi/D')    
    tauvars = ["Tau_chargedIso","Tau_dxy","Tau_dz","Tau_eta","Tau_leadTkDeltaEta","Tau_leadTkDeltaPhi","Tau_leadTkPtOverTauPt","Tau_mass","Tau_neutralIso","Tau_phi","Tau_photonsOutsideSignalCone","Tau_probDM0PNet","Tau_probDM10PNet","Tau_probDM11PNet","Tau_probDM1PNet","Tau_probDM2PNet","Tau_pt","Tau_ptCorrPNet","Tau_puCorr","Tau_qConfPNet","Tau_rawDeepTau2017v2p1VSe","Tau_rawDeepTau2017v2p1VSjet","Tau_rawDeepTau2017v2p1VSmu","Tau_rawDeepTau2018v2p5VSe","Tau_rawDeepTau2018v2p5VSjet","Tau_rawDeepTau2018v2p5VSmu","Tau_rawIso","Tau_rawIsodR03","Tau_rawPNetVSe","Tau_rawPNetVSjet","Tau_rawPNetVSmu"]
    container_tauvars_full = {}
    container_tauvars_fast = {}
    for tauvar in tauvars:
        dtype = float
        if tauvar in ["Tau_charge", "Tau_looseId"]:
            dtype = int
        container_tauvars_full[tauvar] = np.zeros(1, dtype=dtype)
        container_tauvars_fast[tauvar] = np.zeros(1, dtype=dtype)
        tTau.Branch('Rec'+tauvar+'_FullSim', container_tauvars_full[tauvar], 'Rec'+tauvar+'_FullSim' + ('/I' if dtype == int else '/D'))
        tTau.Branch('Rec'+tauvar+'_FastSim', container_tauvars_fast[tauvar], 'Rec'+tauvar+'_FastSim' + ('/I' if dtype == int else '/D'))
    container_TauResponse_FullSim = np.zeros(1,dtype=float)
    tTau.Branch('RecTauResponse_FullSim', container_TauResponse_FullSim,'RecTauResponse_FullSim/D')    
    container_TauResponse_FastSim = np.zeros(1,dtype=float)    
    tTau.Branch('RecTauResponse_FastSim', container_TauResponse_FastSim,'RecTauResponse_FastSim/D')
    container_TauDrGenRec_FastSim = np.zeros(1,dtype=float)    
    tTau.Branch('RecTauDrGenRec_FastSim', container_TauDrGenRec_FastSim,'RecTauDrGenRec_FastSim/D')    
    container_TauDrGenRec_FullSim = np.zeros(1,dtype=float)    
    tTau.Branch('RecTauDrGenRec_FullSim', container_TauDrGenRec_FullSim,'RecTauDrGenRec_FullSim/D')              

    tEvent = TTree('tEvent','tEvent')
    container_Met_FullSim = np.zeros(1,dtype=float)
    tEvent.Branch('Met_FullSim', container_Met_FullSim,'Met_FullSim/D') 
    container_Met_FastSim = np.zeros(1,dtype=float)    
    tEvent.Branch('Met_FastSim', container_Met_FastSim,'Met_FastSim/D') 
    container_Met_NnSplice = np.zeros(1,dtype=float)    
    tEvent.Branch('Met_NnSplice', container_Met_NnSplice,'Met_NnSplice/D') 
    container_Met_Gen = np.zeros(1,dtype=float)    
    tEvent.Branch('Met_Gen', container_Met_Gen,'Met_Gen/D')         
    container_Met_GenSmear = np.zeros(1,dtype=float)    
    tEvent.Branch('Met_GenSmear', container_Met_GenSmear,'Met_GenSmear/D')
    container_Met_GenSplice = np.zeros(1,dtype=float)    
    tEvent.Branch('Met_GenSplice', container_Met_GenSplice,'Met_GenSplice/D')    
    container_Mht_FullSim = np.zeros(1,dtype=float)
    tEvent.Branch('Mht_FullSim', container_Mht_FullSim,'Mht_FullSim/D') 
    container_Mht_FastSim = np.zeros(1,dtype=float)    
    tEvent.Branch('Mht_FastSim', container_Mht_FastSim,'Mht_FastSim/D') 
    container_Mht_NnSplice = np.zeros(1,dtype=float)    
    tEvent.Branch('Mht_NnSplice', container_Mht_NnSplice,'Mht_NnSplice/D') 
    container_Mht_Gen = np.zeros(1,dtype=float)    
    tEvent.Branch('Mht_Gen', container_Mht_Gen,'Mht_Gen/D')         
    container_Mht_GenSmear = np.zeros(1,dtype=float)    
    tEvent.Branch('Mht_GenSmear', container_Mht_GenSmear,'Mht_GenSmear/D')
    container_Mht_GenSplice = np.zeros(1,dtype=float)    
    tEvent.Branch('Mht_GenSplice', container_Mht_GenSplice,'Mht_GenSplice/D')         
    
    nfiles = len(fastsimlist)
    evcounter = 0
    
    for ifname in range(len(fastsimlist)):
      print ('now processing', ifname, 'of', nfiles)
      
      FULLNAME = fastsimlist[ifname].replace('/Fast/','/Full/').replace('/FastEstatMean/','/Full/').replace('/FastGenDecays/','/Full/').replace('SIM_RECOBEFMIX_DIGI_L1_DIGI2RAW_L1Reco_RECO_','')
      print ('main file:', fastsimlist[ifname])
      print ('tagging along is', FULLNAME)
      if not os.path.exists(FULLNAME):
          print ('fullsim doesnt exist yet')
          continue
            
      fFast = TFile(str(fastsimlist[ifname]))
      c_FastSim = fFast.Get('Events')
      if ifname==0: 
          print ('hallo', fastsimlist[ifname])
          c_FastSim.Show(0)
          print ('auf wiedersehen')
      fFull = TFile(FULLNAME)
      c_FullSim = fFull.Get('Events')
      nevents = c_FastSim.GetEntries()
      
      if not nevents==c_FullSim.GetEntries():
        print ('not the same number of events in Fast/Full')
        continue
      print ('going to analyze ', nevents, 'events')
      for ievent in range(nevents):
           if evcounter%1==0: print ('analyzing file %d of %d, having counted %d events' % (ifname, nfiles, evcounter))
           if emod2>0:
               if not ievent%2==emod2%2: continue        
           evcounter+=1
           c_FastSim.GetEntry(ievent)
           c_FullSim.GetEntry(ievent)
           
           container_Met_FullSim[0] = 0
           container_Met_FastSim[0] = 0        
           container_Met_NnSplice[0] = 0
           container_Met_GenSplice[0] = 0
           container_Met_Gen[0] = 0
           container_Met_GenSmear[0] = 0        
           
           container_Mht_FullSim[0] = 0
           container_Mht_FastSim[0] = 0        
           container_Mht_NnSplice[0] = 0
           container_Mht_GenSplice[0] = 0
           container_Mht_Gen[0] = 0
           container_Mht_GenSmear[0] = 0        
           
           metfastsim = TLorentzVector()
           metfastsim.SetPtEtaPhiE(c_FastSim.MET_pt, 0, c_FastSim.MET_phi, c_FastSim.MET_pt)
           metfullsim = TLorentzVector()
           metfullsim.SetPtEtaPhiE(c_FullSim.MET_pt, 0, c_FullSim.MET_phi, c_FullSim.MET_pt)                
           metnnsplice = TLorentzVector()
           metnnsplice.SetPtEtaPhiE(c_FastSim.MET_pt, 0, c_FastSim.MET_phi, c_FastSim.MET_pt)
           metgensplice = TLorentzVector()
           metgensplice.SetPtEtaPhiE(c_FastSim.MET_pt, 0, c_FastSim.MET_phi, c_FastSim.MET_pt)
           metgen = TLorentzVector()
           metgen.SetPtEtaPhiE(c_FastSim.GenMET_pt, 0, c_FastSim.GenMET_phi, c_FastSim.GenMET_pt)
           metgensmear = TLorentzVector()
           metgensmear.SetPtEtaPhiE(c_FastSim.GenMET_pt, 0, c_FastSim.GenMET_phi, c_FastSim.GenMET_pt)
           
           mhtfastsim = TLorentzVector(0,0,0,0)
           mhtfullsim = TLorentzVector(0,0,0,0)
           mhtnnsplice = TLorentzVector(0,0,0,0)
           mhtgensplice = TLorentzVector(0,0,0,0)        
           mhtgen = TLorentzVector(0,0,0,0)
           mhtgensmear = TLorentzVector(0,0,0,0)
           
           #gather gen jets
           genjets = []
           for ig in range(c_FastSim.nGenJet):
               gtlv = TLorentzVector()
               gtlv.SetPtEtaPhiM(c_FastSim.GenJet_pt[ig], c_FastSim.GenJet_eta[ig], c_FastSim.GenJet_phi[ig], c_FastSim.GenJet_mass[ig])
               genjets.append(gtlv)
               resp = rejection_sampler(mlpresponse,gtlv.Pt(), min(2.4,abs(gtlv.Eta())), [0,2.5])    
               if gtlv.Pt()>30 and abs(gtlv.Eta())<5.0:
                   mhtgen-=gtlv
                   gtlvSmear = gtlv.Clone()
                   gtlvSmear*=resp
                   mhtgensmear-=gtlvSmear
                   metgensmear+=gtlv
                   metgensmear-=gtlvSmear               
           #gen muons:
           genmuons = []
           genelectrons = []
           genphotons = []
           gentaus = []                   
           for igen in range(c_FastSim.nGenPart):  # Assuming nGenPart is the number of gen muons
               if not abs(c_FastSim.GenPart_pdgId[igen]) in [11,13,15,22]: continue
               ##check status or something?if not c_FastSim.Muon_muonId[imuon]==6: continue
               if abs(c_FastSim.GenPart_pdgId[igen])==13:
                  muonlv = TLorentzVector()
                  muonlv.SetPtEtaPhiM(c_FastSim.GenPart_pt[igen], c_FastSim.GenPart_eta[igen], c_FastSim.GenPart_phi[igen], c_FastSim.GenPart_mass[igen])
                  genmuons.append(muonlv)
               if abs(c_FastSim.GenPart_pdgId[igen])==11:
                  electronlv = TLorentzVector()
                  electronlv.SetPtEtaPhiM(c_FastSim.GenPart_pt[igen], c_FastSim.GenPart_eta[igen], c_FastSim.GenPart_phi[igen], c_FastSim.GenPart_mass[igen])
                  genelectrons.append(electronlv)    
               if abs(c_FastSim.GenPart_pdgId[igen])==15:
                  taulv = TLorentzVector()
                  taulv.SetPtEtaPhiM(c_FastSim.GenPart_pt[igen], c_FastSim.GenPart_eta[igen], c_FastSim.GenPart_phi[igen], c_FastSim.GenPart_mass[igen])
                  gentaus.append(taulv)                      
               if abs(c_FastSim.GenPart_pdgId[igen])==22:
                  photonlv = TLorentzVector()
                  photonlv.SetPtEtaPhiM(c_FastSim.GenPart_pt[igen], c_FastSim.GenPart_eta[igen], c_FastSim.GenPart_phi[igen], c_FastSim.GenPart_mass[igen])
                  genphotons.append(photonlv)                                    
           
           
           #we will next focus on event-level variables to refine, such as MET.
           for ijet in range(c_FastSim.nJet):
                jettlv = TLorentzVector()
                jettlv.SetPtEtaPhiM(c_FastSim.Jet_pt[ijet], c_FastSim.Jet_eta[ijet], c_FastSim.Jet_phi[ijet], c_FastSim.Jet_mass[ijet])
                if not jettlv.Pt()>15: continue #15 GeV is same as nano cut
                #if not jettlv.Pt()>30: continue
                if not abs(jettlv.Eta())<5.0: continue
                if jettlv.Pt()>30: 
                	mhtfastsim-=jettlv
                	mhtgensplice-=jettlv
                	mhtnnsplice-=jettlv
                #if not abs(jettlv.Eta())<2.4: continue
                drmax = 99
                gtlvbest = jettlv.Clone()
                for gtlv in genjets:
                    dr = jettlv.DeltaR(gtlv)
                    if not (dr<0.2 and dr < drmax): continue
                    drmax = dr
                    gtlvbest = gtlv
                if drmax<0.2:
                    metgensplice+=jettlv
                    metgensplice-=gtlvbest
                    mhtgensplice+=jettlv
                    mhtgensplice-=gtlvbest                
                    nnjettlv = gtlvbest.Clone()
                    nnjettlv*= rejection_sampler(mlpresponse,gtlvbest.Pt(), min(2.4,abs(gtlvbest.Eta())), [0,2.5])
                    metnnsplice+=jettlv
                    metnnsplice-=nnjettlv
                    mhtnnsplice+=jettlv
                    mhtnnsplice-=nnjettlv                                
           for ijet in range(c_FullSim.nJet):
               jettlv = TLorentzVector()
               jettlv.SetPtEtaPhiM(c_FullSim.Jet_pt[ijet], c_FullSim.Jet_eta[ijet], c_FullSim.Jet_phi[ijet], c_FullSim.Jet_mass[ijet])
               if not jettlv.Pt()>30: continue
               if not abs(jettlv.Eta())<5.0: continue
               mhtfullsim-=jettlv
           container_Met_FullSim[0] = metfullsim.Pt()
           container_Met_FastSim[0] = metfastsim.Pt()
           container_Met_NnSplice[0] = metnnsplice.Pt()
           container_Met_GenSplice[0] = metgensplice.Pt()                
           container_Met_Gen[0] = metgen.Pt()        
           container_Met_GenSmear[0] = metgensmear.Pt()
           container_Mht_FullSim[0] = mhtfullsim.Pt()
           container_Mht_FastSim[0] = mhtfastsim.Pt()
           container_Mht_NnSplice[0] = mhtnnsplice.Pt()
           container_Mht_GenSplice[0] = mhtgensplice.Pt() 
           container_Mht_Gen[0] = mhtgen.Pt()        
           container_Mht_GenSmear[0] = mhtgensmear.Pt()            
           tEvent.Fill()                           
           #now begin the jet tree
           for ig, gtlv in enumerate(genjets):
               if not (c_FastSim.GenJet_pt[ig]==c_FullSim.GenJet_pt[ig]):
                   print ('fail!', c_FastSim.GenJet_pt[ig], c_FullSim.GenJet_pt[ig])
               if not abs(gtlv.Eta())<5.0: continue    
               closestDr = 9999
               for jg in range(c_FastSim.nGenJet):
                   if jg==ig: continue
                   gtlv2 = TLorentzVector()
                   gtlv2.SetPtEtaPhiM(c_FastSim.GenJet_pt[jg], c_FastSim.GenJet_eta[jg], c_FastSim.GenJet_phi[jg], c_FastSim.GenJet_mass[jg])
                   closestDr = min(closestDr, gtlv2.DeltaR(gtlv))
                   if closestDr<0.6: break
               if closestDr<0.6: continue     
               container_GenJet_pt[0] = gtlv.Pt()
               container_GenJet_eta[0] = gtlv.Eta()
               container_GenJet_phi[0] = gtlv.Phi()
               container_GenJet_mass[0] = gtlv.M()               
               container_GenJet_hadronFlavour[0] = c_FastSim.GenJet_hadronFlavour[ig]
               container_GenJet_partonFlavour[0] = c_FastSim.GenJet_partonFlavour[ig]
               container_JetDrGenRec_FastSim[0] = -1.0
               container_JetResponse_FastSim[0] = -1.0
               container_JetDrGenRec_FullSim[0] = -1.0
               container_JetResponse_FullSim[0] = -1.0        
               for varkey in container_jetvars_fast.keys():
                   container_jetvars_fast[varkey][0] = -1
                   container_jetvars_full[varkey][0] = -1
   
               isfastmatched, isfullmatched = False, False
               drmax = 99
               uniqueMatch = True
               closestRecoJet = TLorentzVector(0,0,0,0)
               for ijet in range(c_FastSim.nJet):
                   if not c_FastSim.Jet_jetId[ijet]==6: continue
                   jettlv = TLorentzVector()
                   jettlv.SetPtEtaPhiM(c_FastSim.Jet_pt[ijet], c_FastSim.Jet_eta[ijet], c_FastSim.Jet_phi[ijet], c_FastSim.Jet_mass[ijet])
                   dr = jettlv.DeltaR(gtlv)
                   if dr>=0.2 and dr<0.6:
                       uniqueMatch = False
                       break
                   if not (dr<0.2 and dr < drmax): continue
                   drmax = dr
                   closestRecoJet = jettlv.Clone()
                   isfastmatched = True
                   container_JetDrGenRec_FastSim[0] = jettlv.DeltaR(gtlv)
                   for varkey in container_jetvars_fast.keys(): container_jetvars_fast[varkey][0] = getattr(c_FastSim, varkey)[ijet]             
                   container_JetResponse_FastSim[0] = jettlv.Pt()/gtlv.Pt()
                   break
               if not uniqueMatch: continue
               
               nnjettlv = gtlv.Clone()
               nnjettlv*= resp
               container_JetResponse_Nn[0] = nnjettlv.Pt()/gtlv.Pt()
               if not isfastmatched: continue
               drmax = 99                
               for ijet in range(c_FullSim.nJet):
                   if not c_FullSim.Jet_jetId[ijet]==6: continue
                   jettlv = TLorentzVector()
                   jettlv.SetPtEtaPhiM(c_FullSim.Jet_pt[ijet], c_FullSim.Jet_eta[ijet], c_FullSim.Jet_phi[ijet], c_FullSim.Jet_mass[ijet])
                   dr = jettlv.DeltaR(gtlv)
                   if not (dr<0.2 and dr < drmax): continue
                   drmax = dr                    
                   isfullmatched = True                    
                   container_JetDrGenRec_FullSim[0] = jettlv.DeltaR(gtlv)
                   for varkey in container_jetvars_full.keys(): container_jetvars_full[varkey][0] = getattr(c_FullSim, varkey)[ijet]                
                   container_JetResponse_FullSim[0] = jettlv.Pt()/gtlv.Pt()
                   break
               if not isfullmatched: continue
               tJet.Fill()
           for ig, gtlv in enumerate(genmuons):
               if not (c_FastSim.GenPart_pt[ig]==c_FullSim.GenPart_pt[ig]):
                   print ('fail!', c_FastSim.GenPart_pt[ig], c_FullSim.GenPart_pt[ig])    
               container_GenMuon_pt[0] = gtlv.Pt()
               container_GenMuon_eta[0] = gtlv.Eta()
               container_GenMuon_phi[0] = gtlv.Phi()
               container_MuonDrGenRec_FastSim[0] = -1.0
               container_MuonResponse_FastSim[0] = -1.0
               container_MuonDrGenRec_FullSim[0] = -1.0
               container_MuonResponse_FullSim[0] = -1.0        
               for varkey in container_jetvars_fast.keys():
                   container_jetvars_fast[varkey][0] = -1
                   container_jetvars_full[varkey][0] = -1
               isfastmatched, isfullmatched = False, False
               drmax = 99
               closestRecoMuon = TLorentzVector(0,0,0,0)
               for imuon in range(c_FastSim.nMuon):
                   ##check status or something?if not c_FastSim.Muon_muonId[imuon]==6: continue
                   muontlv = TLorentzVector()
                   muontlv.SetPtEtaPhiM(c_FastSim.Muon_pt[imuon], c_FastSim.Muon_eta[imuon], c_FastSim.Muon_phi[imuon], c_FastSim.Muon_mass[imuon])
                   dr = muontlv.DeltaR(gtlv)
                   if not (dr<0.01 and dr<drmax): continue
                   drmax = dr                   
                   closestRecoMuon = muontlv.Clone()
                   isfastmatched = True
                   container_MuonDrGenRec_FastSim[0] = muontlv.DeltaR(gtlv)
                   for varkey in container_muonvars_fast.keys(): container_muonvars_fast[varkey][0] = getattr(c_FastSim, varkey)[imuon]             
                   container_MuonResponse_FastSim[0] = muontlv.Pt()/gtlv.Pt()
               if not isfastmatched: continue
               drmax = 99                
               for imuon in range(c_FullSim.nMuon):
                   muontlv = TLorentzVector()
                   muontlv.SetPtEtaPhiM(c_FullSim.Muon_pt[imuon], c_FullSim.Muon_eta[imuon], c_FullSim.Muon_phi[imuon], c_FullSim.Muon_mass[imuon])
                   dr = muontlv.DeltaR(gtlv)
                   if not (dr<0.01 and dr<drmax): continue
                   drmax = dr                                       
                   isfullmatched = True                    
                   container_MuonDrGenRec_FullSim[0] = muontlv.DeltaR(gtlv)
                   for varkey in container_muonvars_full.keys(): container_muonvars_full[varkey][0] = getattr(c_FullSim, varkey)[imuon]  
                   container_MuonResponse_FullSim[0] = muontlv.Pt()/gtlv.Pt()
               if not isfullmatched: continue
               tMuon.Fill()
               
           for ig, gtlv in enumerate(genelectrons):
               if not (c_FastSim.GenPart_pt[ig]==c_FullSim.GenPart_pt[ig]):
                   print ('fail!', c_FastSim.GenPart_pt[ig], c_FullSim.GenPart_pt[ig])    
               container_GenElectron_pt[0] = gtlv.Pt()
               container_GenElectron_eta[0] = gtlv.Eta()
               container_GenElectron_phi[0] = gtlv.Phi()
               container_ElectronDrGenRec_FastSim[0] = -1.0
               container_ElectronResponse_FastSim[0] = -1.0
               container_ElectronDrGenRec_FullSim[0] = -1.0
               container_ElectronResponse_FullSim[0] = -1.0        
               for varkey in container_jetvars_fast.keys():
                   container_jetvars_fast[varkey][0] = -1
                   container_jetvars_full[varkey][0] = -1
               isfastmatched, isfullmatched = False, False
               drmax = 99
               closestRecoElectron = TLorentzVector(0,0,0,0)
               for ielectron in range(c_FastSim.nElectron):
                   ##check status or something?if not c_FastSim.Electron_electronId[ielectron]==6: continue
                   electrontlv = TLorentzVector()
                   electrontlv.SetPtEtaPhiM(c_FastSim.Electron_pt[ielectron], c_FastSim.Electron_eta[ielectron], c_FastSim.Electron_phi[ielectron], c_FastSim.Electron_mass[ielectron])
                   dr = electrontlv.DeltaR(gtlv)
                   if not (dr<0.01 and dr<drmax): continue
                   drmax = dr     
                   isfastmatched = True
                   container_ElectronDrGenRec_FastSim[0] = electrontlv.DeltaR(gtlv)
                   for varkey in container_electronvars_fast.keys(): container_electronvars_fast[varkey][0] = getattr(c_FastSim, varkey)[ielectron]             
                   container_ElectronResponse_FastSim[0] = electrontlv.Pt()/gtlv.Pt()
               if not isfastmatched: continue
               drmax = 99                
               for ielectron in range(c_FullSim.nElectron):
                   electrontlv = TLorentzVector()
                   electrontlv.SetPtEtaPhiM(c_FullSim.Electron_pt[ielectron], c_FullSim.Electron_eta[ielectron], c_FullSim.Electron_phi[ielectron], c_FullSim.Electron_mass[ielectron])
                   dr = electrontlv.DeltaR(gtlv)
                   if not (dr<0.01 and dr<drmax): continue
                   drmax = dr                                      
                   isfullmatched = True                    
                   container_ElectronDrGenRec_FullSim[0] = electrontlv.DeltaR(gtlv)
                   for varkey in container_electronvars_full.keys(): container_electronvars_full[varkey][0] = getattr(c_FullSim, varkey)[ielectron]  
                   container_ElectronResponse_FullSim[0] = electrontlv.Pt()/gtlv.Pt()
               if not isfullmatched: continue
               tElectron.Fill()   
               
           for ig, gtlv in enumerate(genphotons):
               if not (c_FastSim.GenPart_pt[ig]==c_FullSim.GenPart_pt[ig]):
                   print ('fail!', c_FastSim.GenPart_pt[ig], c_FullSim.GenPart_pt[ig])    
               container_GenPhoton_pt[0] = gtlv.Pt()
               container_GenPhoton_eta[0] = gtlv.Eta()
               container_GenPhoton_phi[0] = gtlv.Phi()
               container_PhotonDrGenRec_FastSim[0] = -1.0
               container_PhotonResponse_FastSim[0] = -1.0
               container_PhotonDrGenRec_FullSim[0] = -1.0
               container_PhotonResponse_FullSim[0] = -1.0        
               for varkey in container_jetvars_fast.keys():
                   container_jetvars_fast[varkey][0] = -1
                   container_jetvars_full[varkey][0] = -1
               isfastmatched, isfullmatched = False, False
               drmax = 99
               closestRecoPhoton = TLorentzVector(0,0,0,0)
               for iphoton in range(c_FastSim.nPhoton):
                   ##check status or something?if not c_FastSim.Photon_photonId[iphoton]==6: continue
                   photontlv = TLorentzVector()
                   photontlv.SetPtEtaPhiM(c_FastSim.Photon_pt[iphoton], c_FastSim.Photon_eta[iphoton], c_FastSim.Photon_phi[iphoton], 0)
                   dr = photontlv.DeltaR(gtlv)
                   if not (dr<0.01 and dr<drmax): continue
                   drmax = dr     
                   isfastmatched = True
                   container_PhotonDrGenRec_FastSim[0] = photontlv.DeltaR(gtlv)
                   for varkey in container_photonvars_fast.keys(): container_photonvars_fast[varkey][0] = getattr(c_FastSim, varkey)[iphoton]             
                   container_PhotonResponse_FastSim[0] = photontlv.Pt()/gtlv.Pt()
               if not isfastmatched: continue
               drmax = 99                
               for iphoton in range(c_FullSim.nPhoton):
                   photontlv = TLorentzVector()
                   photontlv.SetPtEtaPhiM(c_FullSim.Photon_pt[iphoton], c_FullSim.Photon_eta[iphoton], c_FullSim.Photon_phi[iphoton], 0)
                   dr = photontlv.DeltaR(gtlv)
                   if not (dr<0.01 and dr<drmax): continue
                   drmax = dr                                       
                   isfullmatched = True                    
                   container_PhotonDrGenRec_FullSim[0] = photontlv.DeltaR(gtlv)
                   for varkey in container_photonvars_full.keys(): container_photonvars_full[varkey][0] = getattr(c_FullSim, varkey)[iphoton]  
                   container_PhotonResponse_FullSim[0] = photontlv.Pt()/gtlv.Pt()
               if not isfullmatched: continue
               tPhoton.Fill()                  
               
           for ig, gtlv in enumerate(gentaus):
               if not (c_FastSim.GenPart_pt[ig]==c_FullSim.GenPart_pt[ig]):
                   print ('fail!', c_FastSim.GenPart_pt[ig], c_FullSim.GenPart_pt[ig])    
               container_GenTau_pt[0] = gtlv.Pt()
               container_GenTau_eta[0] = gtlv.Eta()
               container_GenTau_phi[0] = gtlv.Phi()
               container_TauDrGenRec_FastSim[0] = -1.0
               container_TauResponse_FastSim[0] = -1.0
               container_TauDrGenRec_FullSim[0] = -1.0
               container_TauResponse_FullSim[0] = -1.0        
               for varkey in container_jetvars_fast.keys():
                   container_jetvars_fast[varkey][0] = -1
                   container_jetvars_full[varkey][0] = -1
               isfastmatched, isfullmatched = False, False
               drmax = 99
               closestRecoTau = TLorentzVector(0,0,0,0)
               for itau in range(c_FastSim.nTau):
                   ##check status or something?if not c_FastSim.Tau_tauId[itau]==6: continue
                   tautlv = TLorentzVector()
                   tautlv.SetPtEtaPhiM(c_FastSim.Tau_pt[itau], c_FastSim.Tau_eta[itau], c_FastSim.Tau_phi[itau], c_FastSim.Tau_mass[itau])
                   dr = tautlv.DeltaR(gtlv)
                   drmax = dr
                   if not drmax<0.01: continue
                   isfastmatched = True
                   container_TauDrGenRec_FastSim[0] = tautlv.DeltaR(gtlv)
                   for varkey in container_tauvars_fast.keys(): container_tauvars_fast[varkey][0] = getattr(c_FastSim, varkey)[itau]             
                   container_TauResponse_FastSim[0] = tautlv.Pt()/gtlv.Pt()
               if not isfastmatched: continue
               drmax = 99                
               for itau in range(c_FullSim.nTau):
                   tautlv = TLorentzVector()
                   tautlv.SetPtEtaPhiM(c_FullSim.Tau_pt[itau], c_FullSim.Tau_eta[itau], c_FullSim.Tau_phi[itau], c_FullSim.Tau_mass[itau])
                   dr = tautlv.DeltaR(gtlv)
                   if not (dr<0.01 and dr<drmax): continue
                   drmax = dr                                       
                   isfullmatched = True                    
                   container_TauDrGenRec_FullSim[0] = tautlv.DeltaR(gtlv)
                   for varkey in container_tauvars_full.keys(): container_tauvars_full[varkey][0] = getattr(c_FullSim, varkey)[itau]  
                   container_TauResponse_FullSim[0] = tautlv.Pt()/gtlv.Pt()
               if not isfullmatched: continue
               tTau.Fill()                  
               
      fFast.Close()
      fFull.Close()   
      if ifname>10: break   
    fnew.cd()
    tJet.Write()
    tMuon.Write()
    tElectron.Write()    
    tPhoton.Write()    
    tTau.Write()    
    tEvent.Write()
    print ('just created', fnew.GetName())
    fnew.Close()
main()
