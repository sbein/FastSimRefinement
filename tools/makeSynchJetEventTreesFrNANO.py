'''
cd /nfs/dust/cms/user/beinsam/FastSim/Refinement/CMSSW_12_2_3/src/
cmsenv 
python3 -m pip install torch===1.10.2
python3 -m pip install scikit-learn
python3 -m pip install --upgrade scikit-learn==0.24.2
python3 -m pip install --upgrade pandas==1.4.1
cd ../../
python3 tools/makeSynchTreesFromNANO.py --fnamekeyword "/nfs/dust/cms/user/beinsam/FastSim/VisitCaloResponse/CMSSW_12_2_3/src/TTbar/Fast/1485/step3_inNANOAODSIM.root"
#source /cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc8-opt/setup.sh
#export PYTHONPATH=$HOME/.local/lib/python3.8/site-packages:$PYTHONPATH
python3 -m pip install torch===1.10.2
python3 -m pip install scikit-learn
python3 -m pip install --upgrade scikit-learn==0.24.2
export PYTHONPATH=$HOME/.local/lib/python3.8/site-packages:$PYTHONPATH
'''


#! /usr/bin/env python
from shared_utils import *
import sys
from glob import glob
import os, sys
import numpy as np
from random import uniform
from DataFormats.FWLite import Events, Handle
from ROOT import *
import torch
import torch.nn as nn

class BinaryClassification(nn.Module):
    def __init__(self):
        super(BinaryClassification, self).__init__()
        # Number of input features is 3.
        self.layer_1 = nn.Linear(3, 128) 
        self.layer_2 = nn.Linear(128,1024)
        self.layer_3 = nn.Linear(1024, 8)
        self.layer_out = nn.Linear(8, 1) 
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.0003)
        self.batchnorm1 = nn.BatchNorm1d(128)
        self.batchnorm2 = nn.BatchNorm1d(1024)
        self.batchnorm3 = nn.BatchNorm1d(8)
        
    def forward(self, inputs):
        x = self.relu(self.layer_1(inputs))
        x = self.batchnorm1(x)
        x = self.relu(self.layer_2(x))
        x = self.batchnorm2(x)   
        x = self.relu(self.layer_3(x))
        x = self.batchnorm3(x)
        x = self.dropout(x)
        x = self.layer_out(x)
        return x
        
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

fullsimlist = glob(fnamekeyword.replace('/Fast/','/Full/'))
sorted(fullsimlist)
      



##The following 2 lines are absolutely necessary to avoid a terrible seg fault. thank goodness I found them after
#weeks of wandering in the desert. 
fTest = TFile('/nfs/dust/cms/user/beinsam/FastSim/CMSSW_10_6_22/src/TTbar/Fast/705/step3_inNANOAODSIM.root')

fTest.Close()

import torch




import pandas as pd
import numpy as np



from pickle import load
if torch.cuda.is_available():
    device = torch.device("cuda:0")
    print("running on the GPU")
else:
    device = torch.device("cpu")
    print("running on the CPU")
    


#device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#model = load(open('Model_80ep_15e_minus_4.pkl','rb'))
#scaler = load(open('scaler.pkl', 'rb'))
print('made it here to A0.7')
model = load(open('5E_model_split.pkl','rb'))
scaler = load(open('5E_scaler_split.pkl', 'rb'))

print('made it here to A0.75')


df_np = np.array([[30,0,1]])
df_C = pd.DataFrame(data=df_np, columns = ["GenJetPt", "GenJetEta", "RecJetPt_FullSim"])


#device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = load(open('5E_model_split.pkl','rb'))
scaler = load(open('5E_scaler_split.pkl', 'rb'))
df_np = np.array([[30,0,1]])
df_C = pd.DataFrame(data=df_np, columns = ["GenJetPt", "GenJetEta", "RecJetPt_FullSim"])



methodTMVA = 'MLPBNN'
reader = TMVA.Reader("")
reader.SetName('reader')
from array import array
_GenJetPt_ = array('f',[50])
_GenJetEta_ = array('f',[1])
_JetResponse_ = array('f',[0.0])


thingy = 'Lr10m3Tanh512HiddenLayers7NCycles600NTrain5000000'
reader.AddVariable("GenJetPt",_GenJetPt_)          
reader.AddVariable("abs(GenJetEta)",_GenJetEta_)
reader.AddVariable("JetResponse",_JetResponse_)
reader.BookMVA(methodTMVA, 'datasets/dataset'+thingy+'/weights/TMVAClassification_'+methodTMVA+'.weights.xml')



#https://stackoverflow.com/questions/41470070/python-random-sampling-from-self-defined-probability-function/41471082
fv = np.array([0,0,0],'d')
def mlpresponse(x, pt, eta):
    _JetResponse_[0] = x   
    _GenJetPt_[0] = pt
    _GenJetEta_[0] = eta
    mlp = reader.EvaluateMVA(methodTMVA)
    calib = 1#gcalib.Eval(mlp) 
    out = mlp*calib
    return out/(1-out)

def nnresponse(x):##can move the initiallizations to the sample code
    df_C.at[0, 'RecJetPt_FullSim'] = x
    test_data = torch.FloatTensor(scaler.transform(df_C))
    test_data = test_data.to(device)
    y_test_pred = model(test_data)
    y_test_pred = torch.sigmoid(y_test_pred)
    #y = min(y_test_pred.tolist()[0][0],.999)
    y = y_test_pred.tolist()[0][0]
    #print ("df_C.at[0, 'GenJetPt']", df_C.at[0, 'GenJetPt'], df_C.at[0, 'GenJetEta'], 'y is', y, 'x is', df_C.at[0, 'RecJetPt_FullSim'])
    return y/(1-y)
        

print (mlpresponse(1.2, 50.0, 2.1))

df_C.at[0, 'GenJetEta'] = 2.1
df_C.at[0, 'GenJetPt'] = 50
print (nnresponse(1.2))


def rejection_sampler(p, pt, eta, xbounds):
    df_C.at[0, 'GenJetEta'] = eta
    df_C.at[0, 'GenJetPt'] = pt
    pmax = 1.05*nnresponse(1)
    width = xbounds[1]-xbounds[0]
    while True:
        x = np.random.rand(1)*width+xbounds[0]
        y = np.random.rand(1)*pmax
        if y<=p(x):
            return x
        
####the above is a work in progress, trying to add NN to the master trees


_GenJetPt2_ = array('f',[0])
_GenJetEta2_ = array('f',[0])
_JetResponse2_ = array('f',[0])
_JetResponse2_[0] = 1
_GenJetPt2_[0] = 50
_GenJetEta2_[0] = 0.1

def func2(x,par):
    #_JetResponse2_[0] = x[0]
    #mlp = reader2.EvaluateMVA(method)
    #calib = gcalib.Eval(mlp)
    #out = calib*mlp
    #return out/(1-out)
    ##return par[0]*x[0]
    df_C.at[0, 'RecJetPt_FullSim'] = x[0]
    df_C.at[0, 'GenJetPt'] = _GenJetPt2_[0]
    df_C.at[0, 'GenJetEta'] = _GenJetEta2_[0]    
    test_data = torch.FloatTensor(scaler.transform(df_C))
    test_data = test_data.to(device)
    y_test_pred = model(test_data)
    y_test_pred = torch.sigmoid(y_test_pred)
    y = y_test_pred.tolist()[0][0]
    return y/(1-y)

    

innstub = '_'.join(fastsimlist[0].split('/')[-2:]).replace('.root','')


def main():

        
    name = 'mc_fullfastnn_'+innstub+'_fromNANO.root'
    name = name.replace('.root.root','.root')

      
    if 'EstatMean' in fnamekeyword: name = name.replace('.root','_EstatMean.root')
    else: name = name.replace('.root','_Ootb.root')
    if emod2==1: name = name.replace('.root','_ForTraining.root')
    if emod2==2: name = name.replace('.root','_ForTesting.root')    
    fnew = TFile(name,'recreate')
        
    tJet = TTree('tJet','tJet')
    
    

    container_GenJetPt = np.zeros(1,dtype=float)    
    tJet.Branch('GenJetPt', container_GenJetPt,'GenJetPt/D')
    container_GenJetEta = np.zeros(1,dtype=float)
    tJet.Branch('GenJetEta', container_GenJetEta,'GenJetEta/D')
    container_GenJet_hadronFlavour = np.zeros(1,dtype=int)
    tJet.Branch('GenJet_hadronFlavour', container_GenJet_hadronFlavour,'GenJet_hadronFlavour/I')
    container_GenJet_partonFlavour = np.zeros(1,dtype=int)
    tJet.Branch('GenJet_partonFlavour', container_GenJet_partonFlavour,'GenJet_partonFlavour/I')
    container_JetDrGenRec = np.zeros(1,dtype=float)    
    tJet.Branch('JetDrGenRec', container_JetDrGenRec,'JetDrGenRec/D')
    
    #nanovars = ["Jet_area", "Jet_btagCMVA", "Jet_btagCSVV2", "Jet_btagDeepB", "Jet_btagDeepC", "Jet_btagDeepCvB", "Jet_btagDeepCvL", "Jet_btagDeepFlavB", "Jet_btagDeepFlavC", "Jet_btagDeepFlavCvB", "Jet_btagDeepFlavCvL", "Jet_btagDeepFlavQG", "Jet_chEmEF", "Jet_chFPV0EF", "Jet_chFPV1EF", "Jet_chFPV2EF", "Jet_chFPV3EF", "Jet_chHEF", "Jet_eta", "Jet_hfsigmaEtaEta", "Jet_hfsigmaPhiPhi", "Jet_mass", "Jet_muEF", "Jet_muonSubtrFactor", "Jet_neEmEF", "Jet_neHEF", "Jet_phi", "Jet_pt", "Jet_puIdDisc", "Jet_qgl", "Jet_rawFactor", "Jet_bRegCorr", "Jet_bRegRes", "Jet_cRegCorr", "Jet_cRegRes", "Jet_electronIdx1", "Jet_electronIdx2", "Jet_hfadjacentEtaStripsSize", "Jet_hfcentralEtaStripSize", "Jet_jetId", "Jet_muonIdx1", "Jet_muonIdx2", "Jet_nConstituents", "Jet_nElectrons", "Jet_nMuons", "Jet_puId"]
    nanovars = []#
    nanovars = ["Jet_btagCSVV2", "Jet_btagDeepB", "Jet_btagDeepCvB", "Jet_btagDeepCvL", "Jet_btagDeepFlavB", "Jet_btagDeepFlavCvB", "Jet_btagDeepFlavCvL", "Jet_btagDeepFlavQG", "Jet_chEmEF", "Jet_chHEF", "Jet_eta", "Jet_mass", "Jet_muEF", "Jet_muonSubtrFactor", "Jet_neEmEF", "Jet_neHEF", "Jet_phi", "Jet_pt", "Jet_puIdDisc", "Jet_qgl", "Jet_rawFactor", "Jet_bRegCorr", "Jet_bRegRes", "Jet_jetId", "Jet_nConstituents", "Jet_nElectrons", "Jet_nMuons", "Jet_puId"]
    

    container_nanovars_full = {}    
    container_nanovars_fast = {}
    for nanovar in nanovars:
        if '_n' in nanovar and not '_ne' in nanovar:
            container_nanovars_full[nanovar] = np.zeros(1,dtype=int)            
            container_nanovars_fast[nanovar] = np.zeros(1,dtype=int)        
            tJet.Branch('Rec'+nanovar+'_FullSim', container_nanovars_full[nanovar], 'Rec'+nanovar+'_FullSim'+'/I')
        else:
            container_nanovars_full[nanovar] = np.zeros(1,dtype=float)
            container_nanovars_fast[nanovar] = np.zeros(1,dtype=float)
            tJet.Branch('Rec'+nanovar+'_FullSim', container_nanovars_full[nanovar] ,'Rec'+nanovar+'_FullSim'+'/D')
            tJet.Branch('Rec'+nanovar+'_FastSim', container_nanovars_fast[nanovar] ,'Rec'+nanovar+'_FastSim'+'/D')
            tJet.Branch('Rec'+nanovar+'_Nn', container_nanovars_fast[nanovar] ,'Rec'+nanovar+'_Nn'+'/D')            
        

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

      
      FULLNAME = fastsimlist[ifname].replace('/Fast/','/Full/').replace('/FastEstatMean/','/Full/')
      print ('main file:', fastsimlist[ifname])
      print ('tagging along is', FULLNAME)
      if not os.path.exists(FULLNAME):
          print ('fullsim doesnt exist yet')
          continue
            
      fFast = TFile(str(fastsimlist[ifname]))
      c_FastSim = fFast.Get('Events')
      c_FastSim.Show(0)
      #c_FastSim = TChain('Events')
      #c_FastSim.Add(fastsimlist[ifname])

      fFull = TFile(FULLNAME)
      c_FullSim = fFull.Get('Events')

      nevents = c_FastSim.GetEntries()
      
      if not nevents==c_FullSim.GetEntries():
        print ('not the same number of events in Fast/Full')
        continue
      
      print ('going to analyze ', nevents, 'events')

      for ievent in range(nevents):

        if evcounter%200==0: print ('analyzing file %d of %d, having counted %d events' % (ifname, nfiles, evcounter))
        
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
            for ig in range(c_FastSim.nGenJet):
                gtlv = TLorentzVector()
                gtlv.SetPtEtaPhiM(c_FastSim.GenJet_pt[ig], c_FastSim.GenJet_eta[ig], c_FastSim.GenJet_phi[ig], c_FastSim.GenJet_mass[ig])
                dr = jettlv.DeltaR(gtlv)
                if not (dr<0.2 and dr < drmax): continue
                drmax = dr
                gtlvbest.SetPtEtaPhiM(c_FastSim.GenJet_pt[ig], c_FastSim.GenJet_eta[ig], c_FastSim.GenJet_phi[ig], c_FastSim.GenJet_mass[ig])
            if drmax<0.2:
                metgensplice+=jettlv
                metgensplice-=gtlvbest
                mhtgensplice+=jettlv
                mhtgensplice-=gtlvbest                
                nnjettlv = gtlvbest.Clone()
                nnjettlv*= rejection_sampler(nnresponse,gtlvbest.Pt(), min(2.4,abs(gtlvbest.Eta())), [0,2.5])
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
            
        
        for ig in range(c_FastSim.nGenJet):
            gtlv = TLorentzVector()
            gtlv.SetPtEtaPhiM(c_FastSim.GenJet_pt[ig], c_FastSim.GenJet_eta[ig], c_FastSim.GenJet_phi[ig], c_FastSim.GenJet_mass[ig])

            if not (c_FastSim.GenJet_pt[ig]==c_FullSim.GenJet_pt[ig]):
            	print ('fail!', c_FastSim.GenJet_pt[ig], c_FullSim.GenJet_pt[ig])
            if not gtlv.Pt()>20: continue
            resp = rejection_sampler(nnresponse,gtlv.Pt(), min(2.4,abs(gtlv.Eta())), [0,2.5])    
            if gtlv.Pt()>30 and abs(gtlv.Eta())<5.0:
                mhtgen-=gtlv
                gtlvSmear = gtlv.Clone()
                gtlvSmear*=resp
                mhtgensmear-=gtlvSmear
                metgensmear+=gtlv
                metgensmear-=gtlvSmear
            
            if not abs(gtlv.Eta())<2.4: continue

            container_GenJetPt[0] = gtlv.Pt()
            container_GenJetEta[0] = gtlv.Eta()
            container_GenJet_hadronFlavour[0] = c_FastSim.GenJet_hadronFlavour[ig]
            container_GenJet_partonFlavour[0] = c_FastSim.GenJet_partonFlavour[ig]
            container_JetDrGenRec_FastSim[0] = -1.0
            container_JetResponse_FastSim[0] = -1.0
            container_JetDrGenRec_FullSim[0] = -1.0
            container_JetResponse_FullSim[0] = -1.0
            
            for varkey in container_nanovars_fast.keys():
                container_nanovars_fast[varkey][0] = -1
                container_nanovars_full[varkey][0] = -1

            isfastmatched, isfullmatched = False, False
            drmax = 99
            closestRecoJet = TLorentzVector(0,0,0,0)
            for ijet in range(c_FastSim.nJet):
                jettlv = TLorentzVector()
                jettlv.SetPtEtaPhiM(c_FastSim.Jet_pt[ijet], c_FastSim.Jet_eta[ijet], c_FastSim.Jet_phi[ijet], c_FastSim.Jet_mass[ijet])
                dr = jettlv.DeltaR(gtlv)
                if not (dr<0.2 and dr < drmax): continue
                drmax = dr
                closestRecoJet = jettlv.Clone()
                isfastmatched = True
                container_JetDrGenRec_FastSim[0] = jettlv.DeltaR(gtlv)
                for varkey in container_nanovars_fast.keys(): container_nanovars_fast[varkey][0] = getattr(c_FastSim, varkey)[ijet]             
                container_JetResponse_FastSim[0] = jettlv.Pt()/gtlv.Pt()
                break
            nnjettlv = gtlv.Clone()
            nnjettlv*= resp
            container_JetResponse_Nn[0] = nnjettlv.Pt()/gtlv.Pt()
            if not isfastmatched: continue
            drmax = 99                
            for ijet in range(c_FullSim.nJet):
                jettlv = TLorentzVector()
                jettlv.SetPtEtaPhiM(c_FullSim.Jet_pt[ijet], c_FullSim.Jet_eta[ijet], c_FullSim.Jet_phi[ijet], c_FullSim.Jet_mass[ijet])
                dr = jettlv.DeltaR(gtlv)
                if not (dr<0.2 and dr < drmax): continue
                drmax = dr                    
                isfullmatched = True                    
                container_JetDrGenRec_FullSim[0] = jettlv.DeltaR(gtlv)
                for varkey in container_nanovars_full.keys(): container_nanovars_full[varkey][0] = getattr(c_FullSim, varkey)[ijet]                
                container_JetResponse_FullSim[0] = jettlv.Pt()/gtlv.Pt()
                break
            if not isfullmatched: continue
            tJet.Fill()
            
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

        
      fFast.Close()
      fFull.Close()   
      if ifname>10: break   
    fnew.cd()
    tJet.Write()
    tEvent.Write()

    print ('just created', fnew.GetName())
    fnew.Close()


main()
