from ROOT import *
from shared_utils import *
'''
source /cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc8-opt/setup.sh
cd /nfs/dust/cms/user/beinsam/FastSim/Refinement/CMSSW_12_2_3/src
cmsenv 
cd ActOnGen
python3 python/testdraw.py


source /cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc8-opt/setup.sh
cd /nfs/dust/cms/user/beinsam/FastSim/Refinement/CMSSW_12_2_3/src/ActOnGen
cmsenv 
python3 -m pip install --upgrade pandas==1.4.1
python3 -m pip install --upgrade scikit-learn==0.24.2
export PYTHONPATH=$HOME/.local/lib/python3.8/site-packages:$PYTHONPATH
python3 python/testdraw.py



cd /nfs/dust/cms/user/beinsam/FastSim/Refinement/CMSSW_12_2_3/src/ActOnGen
cmsenv 
python3 -m pip install torch===1.10.2
python3 -m pip install scikit-learn
python3 -m pip install --upgrade scikit-learn==0.24.2
python3 -m pip install --upgrade pandas==1.4.1
python3 python/testdraw.py



python3 -m pip install torch===1.10.2
python3 -m pip install scikit-learn
python3 -m pip install --upgrade scikit-learn==0.24.2
export PYTHONPATH=$HOME/.local/lib/python3.8/site-packages:$PYTHONPATH
python3 python/testdraw.py
'''

import torch
import pandas as pd
import numpy as np
from pickle import load
'''
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#model = load(open('newpickle.pkl','rb'))
model = load(open('Model_80ep_15e_minus_4.pkl','rb'))
#scaler = load(open('scaler.pkl', 'rb'))
scaler = load(open('Scaler.pkl', 'rb'))
'''
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

df_np = np.array([[30,0,1]])
df_C = pd.DataFrame(data=df_np, columns = ["GenJetPt", "GenJetEta", "RecJetPt_FullSim"])

_GenJetPt2_ = array('f',[0])
_GenJetEta2_ = array('f',[0])
_JetResponse2_ = array('f',[1])

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
    
c1 = TCanvas()
c1.SetLogy()
c1.SetGridx()
c1.SetGridy()
#hSkeleton = TH1F('hSkeleton','FastSim',25,0,2.5)
#histoStyler(hSkeleton, kBlack)
#hSkeleton.GetYaxis().SetRangeUser(0.001, 1000000)
_JetResponse2_[0] = 1
_GenJetPt2_[0] = 15
_GenJetEta2_[0] = 0.1
#crashes#_GenJetPt2_[0] = 777.308349609375
#crashes#_GenJetEta2_[0] = 0.024646759033203167
f2 = TF1('f2', func2, 0,3,2)
f2.SetNpx(1000)
f2.Draw('l')

c1.Update()
pause()

_JetResponse2_[0] = 1
_GenJetPt2_[0] = 15
_GenJetEta2_[0] = 1.1
f3 = TF1('f3', func2, 0,3,2)
f3.SetLineColor(kBlue)
f3.SetNpx(1000)
f3.Draw('l same')

c1.Update()
pause()

_JetResponse2_[0] = 1
_GenJetPt2_[0] = 15
_GenJetEta2_[0] = 2.1
f4 = TF1('f4', func2, 0,3,2)
f4.SetLineColor(kGreen)
f4.SetNpx(1000)
f4.Draw('l same')

c1.Update()
pause()

_JetResponse2_[0] = 1
_GenJetPt2_[0] = 700
_GenJetEta2_[0] = 0.1
f5 = TF1('f5', func2, 0,3,2)
f5.SetLineColor(kViolet)
f5.SetNpx(1000)
f5.Draw('l same')

c1.Update()
pause()

_JetResponse2_[0] = 1
_GenJetPt2_[0] = 900
_GenJetEta2_[0] = 0.1
f6 = TF1('f6', func2, 0,3,2)
f6.SetLineColor(kOrange)
f6.SetNpx(1000)
f6.Draw('l same')

c1.Update()
pause()

    