from ROOT import *
from utils import *
gStyle.SetOptStat(0)

thingy = 'HiddenLayers3NCycles400NTrain5000'
thingy = 'HiddenLayers7NCycles1000NTrain50000'
#thingy = 'HiddenLayers5NCycles600NTrain10000'
#thingy = 'HiddenLayers5NCycles600NTrain50000'
#thingy = 'HiddenLayers8NCycles400NTrain200000'

thingy = 'HiddenLayers7NCycles600NTrain50000'
thingy = 'HiddenLayers7NCycles600NTrain200000'
thingy = 'DnnMore1HiddenLayers7NCycles600NTrain50000'
thingy = '4TanhHiddenLayers7NCycles600NTrain200000'
thingy = '2TanhHiddenLayers7NCycles600NTrain200000'
thingy = '4TanhHiddenLayers7NCycles600NTrain200000'
thingy = 'Lr1em44TanhHiddenLayers7NCycles600NTrain200000'
thingy = 'Lr1em24TanhHiddenLayers7NCycles600NTrain200000'
thingy = 'HiddenLayers7NCycles600NTrain200000'
thingy = 'Lr10tm4HiddenLayers7NCycles600NTrain200000'
thingy = 'Lr10m3Tanh512HiddenLayers7NCycles600NTrain5000000'#this looks real great but missed the peak
#thingy = 'Lr10m5Tanh512HiddenLayers7NCycles600NTrain50000'
#thingy = 'Lr10m2Tanh512HiddenLayers7NCycles600NTrain50000'


thingyNils = '80ep_15e_minus_4'

#treefile = TFile('rootfiles/augtree_NoRegulator_'+thingy+'_littletreestep3_inMINIAODSIM_FullCMSSW_10_6.root')
treefile = TFile('rootfiles/augmented/augtree_mlp_nn'+thingyNils+'_'+thingy+'_littletreestep3_inMINIAODSIM_FullCMSSW_10_6.root')
treefile = TFile('rootfiles/augtree_mlp_nn_Lr10m3Tanh512HiddenLayers7NCycles600NTrain5000000_littletreestep3_inMINIAODSIM_FullCMSSW_10_6.root')
tJet = treefile.Get('tJet')

PtRanges = [30,40,60,100,200,1000]
EtaRanges =[0,1.4,1.55,2.4]
EtaRanges =[0,1.45,2.4]

PtRanges = [30,100]
EtaRanges =[0,2.4]

#PtRanges = [30,1000]
#EtaRanges =[0,2.4]

method = 'MLPBNN'

reader = TMVA.Reader("")
reader.SetName('reader')

from array import array
_GenJetPt_ = array('f',[0])
_GenJetEta_ = array('f',[0])
_JetResponse_ = array('f',[0])

reader.AddVariable("GenJetPt",_GenJetPt_)          
reader.AddVariable("abs(GenJetEta)",_GenJetEta_)
reader.AddVariable("JetResponse",_JetResponse_)

reader.BookMVA(method, 'datasets/dataset'+thingy+'/weights/TMVAClassification_'+method+'.weights.xml')

reader2 = TMVA.Reader("")
reader2.SetName('reader')
_GenJetPt2_ = array('f',[0])
_GenJetEta2_ = array('f',[0])
_JetResponse2_ = array('f',[0])
reader2.AddVariable("GenJetPt",_GenJetPt2_)          
reader2.AddVariable("abs(GenJetEta)",_GenJetEta2_)
reader2.AddVariable("JetResponse",_JetResponse2_)
reader2.BookMVA(method, 'datasets/dataset'+thingy+'/weights/TMVAClassification_'+method+'.weights.xml')

#fcalib = TFile('calibration_mlp.root')
fcalib = TFile('calibfiles/calibration_mlp_'+thingy+'.root')
gcalib = fcalib.Get('g_calib')

_JetResponse_[0] = 1
_GenJetPt_[0] = 50
_GenJetEta_[0] = 0.0


def func(x,par):
    _JetResponse_[0] = x[0]
    mlp = reader.EvaluateMVA(method)
    calib = gcalib.Eval(mlp)
    out = calib*mlp
    return out/(1-out)/3
    #return par[0]*x[0]


c1 = mkcanvas()
c1.SetLogy()

print ('d')


import torch
import pandas as pd
import numpy as np
from pickle import load
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#model = load(open('newpickle.pkl','rb'))
model = load(open('Model_80ep_15e_minus_4.pkl','rb'))

#scaler = load(open('scaler.pkl', 'rb'))
scaler = load(open('Scaler.pkl', 'rb'))

df_np = np.array([[30,0,1]])
df_C = pd.DataFrame(data=df_np, columns = ["GenJetPt", "GenJetEta", "RecJetPt_FullSim"])

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
    return y/(1-y)/3


hSkeleton = TH1F('hSkeleton','FastSim',35,0,3.5)
histoStyler(hSkeleton, kBlack)
hSkeleton.GetYaxis().SetRangeUser(0.001, 1000000)





hSkeleton.Draw()
print (reader.EvaluateMVA(method))

tJet.Show(0)

for ipt in range(len(PtRanges)-1):
    for ieta in range(len(EtaRanges)-1):
            eta1, eta2 = EtaRanges[ieta], EtaRanges[ieta+1]
            pt1, pt2 = PtRanges[ipt], PtRanges[ipt+1]     
            constraint = 'GenJetPt>=%3f && GenJetPt<%3f && abs(GenJetEta)>=%3f && abs(GenJetEta)<%3f' % (pt1, pt2, eta1, eta2)
            tJet.Draw('JetResponse>>'+hSkeleton.GetName(), constraint)
            hFull = tJet.GetHistogram().Clone('full')
            histoStyler(hFull, kBlack)
            hFull.SetLineWidth(3)
            hFull.Scale(1.0/hFull.Integral(),'width')
            tJet.Draw('FastResponse>>'+hSkeleton.GetName(), constraint)
            hFast = tJet.GetHistogram().Clone('fast')
            histoStyler(hFast, kGray+1)
            hFast.SetLineWidth(4)
            hFast.Scale(1.0/hFast.Integral(),'width')

            tJet.Draw('NnResponse>>'+hSkeleton.GetName(), constraint)
            hNn = tJet.GetHistogram().Clone('fast')
            histoStyler(hNn, kGreen+2)
            hNn.SetLineWidth(4)
            hNn.Scale(1.0/hNn.Integral(),'width')
            
            tJet.Draw('MlpResponse>>'+hSkeleton.GetName(), constraint)
            hMlp = tJet.GetHistogram().Clone('mlp') 
            histoStyler(hMlp, kAzure)
            hMlp.SetLineWidth(3)
            hMlp.Scale(1.0/hMlp.Integral(),'width')
            hFull.SetTitle('FullSim')
            hFull.Draw("hist")
            #hFast.SetTitle('')
            
            leg = mklegend(x1=.56, y1=.46, x2=.93, y2=.71, color=kWhite)
            hratio, hmethodsyst = FabDraw(c1,leg,hFull,[hFast],datamc='MC',lumi=str('x'), title = '',LinearScale=False,fractionthing='attempt/Geant4')
            for ibin in range(1, hratio.GetXaxis().GetNbins()+1): hratio.SetBinError(ibin, 0)
            hratio.SetLineWidth(4)
            #histoStyler(hratio, hFast.GetLineColor())
            hratio.GetXaxis().SetTitle('pT(reco)/pT(gen)')
            hratio.GetYaxis().SetRangeUser(0,2.5)
            pad1, pad2 = hmethodsyst

            pad1.cd()

            hFast.Draw("histsame")
            hMlp.Draw('histsame')
            hNn.Draw('histsame')
            _GenJetPt_[0] = 0.5*(pt1+pt2)
            _GenJetEta_[0] = 0.5*(eta1+eta2)
            f1 = TF1('f1', func, -2,5,2)
            #f1.SetNormalized(True)
            f1.SetNpx(1000)
            f1.SetLineColor(kAzure)
            f1.SetLineWidth(3)
            f1.SetLineStyle(kDashed)
            f1.Draw('same')
            tl.DrawLatex(0.14, 0.93, 'pT#in['+str(round(pt1,0))+','+str(round(pt2,0))+') GeV, |#eta|#in['+str(round(eta1,1))+','+str(round(eta2,1))+')')
            
            _GenJetPt2_[0] = 0.5*(pt1+pt2)
            _GenJetEta2_[0] = 0.5*(eta1+eta2)
            f2 = TF1('f2', func2, -2,5,2)
            #f2.SetNormalized(True)
            f2.SetLineColor(kGreen+2)
            f2.SetLineWidth(3)
            f2.SetLineStyle(kDashed)
            f2.SetNpx(1000)
            f2.Draw('same')

        
            leg.AddEntry(hMlp, 'MLP Monte Carlo')
            leg.AddEntry(hNn, 'DNN Monte Carlo')


            leg2 = mklegend(x1=.14, y1=.57, x2=.57, y2=.72, color=kWhite)
            leg2.AddEntry(f1, 'MLP model p_{T}='+str(round(_GenJetPt_[0],0))+' GeV, #eta='+str(round(_GenJetEta_[0],1)))
            leg2.AddEntry(f2, 'DNN model p_{T}='+str(round(_GenJetPt_[0],0))+' GeV, #eta='+str(round(_GenJetEta_[0],1)))
            leg2.Draw()
            pad2.cd()

            hmlpratio = hMlp.Clone('hmlpratio')
            hmlpratio.Divide(hFull)
            hmlpratio.Draw('hist same')
            hmlpratio.SetLineWidth(4)

            hnnratio = hNn.Clone('hnnratio')
            hnnratio.Divide(hFull)
            hnnratio.Draw('hist same')            
            hnnratio.SetLineWidth(4)            
                        
            c1.Update()
            c1.Print('pdfs/responses_nn/'+constraint.replace('000000','').replace(' && ','').replace('>','gt').replace('<','lt').replace('(','').replace(')','')+'.png')
            pause()
