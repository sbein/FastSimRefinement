from ROOT import *
from array import array
from math import floor


tl = TLatex()
tl.SetNDC()
cmsTextFont = 61
extraTextFont = 50
lumiTextSize = 0.6
lumiTextOffset = 0.2
cmsTextSize = 0.75
cmsTextOffset = 0.1
regularfont = 42
originalfont = tl.GetTextFont()
epsi = "#scale[1.3]{#font[122]{e}}"
epsilon = 0.00001


def histoStyler(h,color=kBlack):
    h.SetLineWidth(2)
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    #h.SetFillColor(color)
    size = 0.075
    font = 132
    h.GetXaxis().SetLabelFont(font)
    h.GetYaxis().SetLabelFont(font)
    h.GetXaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleSize(size)
    h.GetXaxis().SetTitleSize(size*1.3)
    h.GetXaxis().SetLabelSize(size*1.3)   
    h.GetYaxis().SetLabelSize(size)
    h.GetXaxis().SetTitleOffset(1.0)
    h.GetYaxis().SetTitleOffset(0.8)
    if not h.GetSumw2N(): h.Sumw2()
    
def histoStylerBigLabels(h,color=kBlack):
    h.SetLineWidth(2)
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    #h.SetFillColor(color)
    size = 0.11
    font = 132
    h.GetXaxis().SetLabelFont(font)
    h.GetYaxis().SetLabelFont(font)
    h.GetXaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleSize(size)
    h.GetXaxis().SetTitleSize(size*1.3)
    h.GetXaxis().SetLabelSize(size*1.2)   
    h.GetYaxis().SetLabelSize(size)
    h.GetXaxis().SetTitleOffset(1.0)
    h.GetYaxis().SetTitleOffset(0.6)
    if not h.GetSumw2N(): h.Sumw2()
    

def makeHist(name, title, nb, low, high, color):
    h = TH1F(name,title,nb,low,high)
    histoStyler(h,color)
    return h

def makeTh1(name, title, nbins, low, high, color=kBlack): 
    h = TH1F(name, title, nbins, low, high)
    histoStyler(h, color)
    return h


def makeTh1VB(name, title, nbins, arrayOfBins): 
    h = TH1F(name, title, nbins, np.asarray(arrayOfBins, 'd'))
    histoStyler(h, 1)
    return h

def makeTh2(name, title, nbinsx, lowx, highx, nbinsy, lowy, highy): 
    h = TH2F(name, title, nbinsx, lowx, highx, nbinsy, lowy, highy)
    histoStyler(h)
    return h

def makeTh2VB(name, title, nbinsx, arrayOfBinsx, nbinsy, arrayOfBinsy):
    h = TH2F(name, title, nbinsx, np.asarray(arrayOfBinsx, 'd'), nbinsy, np.asarray(arrayOfBinsy, 'd'))
    histoStyler(h)
    return h

def graphStyler(g,color):
    g.SetLineWidth(2)
    g.SetLineColor(color)
    g.SetMarkerColor(color)
    #g.SetFillColor(color)
    size = 0.055
    font = 132
    g.GetXaxis().SetLabelFont(font)
    g.GetYaxis().SetLabelFont(font)
    g.GetXaxis().SetTitleFont(font)
    g.GetYaxis().SetTitleFont(font)
    g.GetYaxis().SetTitleSize(size)
    g.GetXaxis().SetTitleSize(size)
    g.GetXaxis().SetLabelSize(size)   
    g.GetYaxis().SetLabelSize(size)
    g.GetXaxis().SetTitleOffset(1.0)
    g.GetYaxis().SetTitleOffset(1.05)

def mkcanvas(name='c1'):
    c1 = TCanvas(name,name,750,700)
    c1.SetBottomMargin(.15)
    c1.SetLeftMargin(.14)
    #c1.SetTopMargin(.13)
    #c1.SetRightMargin(.04)
    return c1

def mkcanvas_wide(name):
    c1 = TCanvas(name,name,1200,700)
    c1.Divide(2,1)
    c1.GetPad(1).SetBottomMargin(.14)
    c1.GetPad(1).SetLeftMargin(.1)
    c1.GetPad(2).SetBottomMargin(.14)
    c1.GetPad(2).SetLeftMargin(.1)    
    c1.GetPad(1).SetGridx()
    c1.GetPad(1).SetGridy()
    c1.GetPad(2).SetGridx()
    c1.GetPad(2).SetGridy()    
    #c1.SetTopMargin(.13)
    #c1.SetRightMargin(.04)
    return c1

def mklegend(x1=.22, y1=.66, x2=.69, y2=.82, color=kWhite):
    lg = TLegend(x1, y1, x2, y2)
    lg.SetFillColor(color)
    lg.SetTextFont(42)
    lg.SetBorderSize(0)
    lg.SetShadowColor(kWhite)
    lg.SetFillStyle(0)
    return lg

def mklegend_(x1=.22, y1=.66, x2=.69, y2=.82, color=kWhite):
    lg = TLegend(x1, y1, x2, y2)
    lg.SetFillColor(color)
    lg.SetTextFont(42)
    lg.SetBorderSize(0)
    lg.SetShadowColor(kWhite)
    lg.SetFillStyle(0)
    return lg

def fillth1(h,x,weight=1):
    h.Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon),weight)

def fillth2(h,x,y,weight=1):
    h.Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon), min(max(y,h.GetYaxis().GetBinLowEdge(1)+epsilon),h.GetYaxis().GetBinLowEdge(h.GetYaxis().GetNbins()+1)-epsilon),weight)

def findbin(thebins, value):
    for bin in thebins:
        if value>=bin[0] and value<=bin[1]:
            return bin
    if value>thebins[-1]: return thebins[-1]
    if value<thebins[0]: return thebins[0]	



def Struct(*args, **kwargs):
    def init(self, *iargs, **ikwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
        for i in range(len(iargs)):
            setattr(self, args[i], iargs[i])
        for k,v in ikwargs.items():
            setattr(self, k, v)

    name = kwargs.pop("name", "MyStruct")
    kwargs.update(dict((k, None) for k in args))
    return type(name, (object,), {'__init__': init, '__slots__': kwargs.keys()})


def writeHistoStruct(hStructDict, opt = 'truthcontrolmethod'):
    keys = sorted(hStructDict.keys())
    for key in keys:
        #print 'writing histogram structure:', key
        if 'truth' in opt: hStructDict[key].Truth.Write()
        if 'control' in opt: hStructDict[key].Control.Write()
        if 'method' in opt: hStructDict[key].Method.Write()

def mkEfficiencyRatio(hPassList, hAllList,hName = 'hRatio'):#for weighted MC, you need TEfficiency!
    hEffList = []
    for i in range(len(hPassList)):
        hPassList[i].Sumw2()
        hAllList[i].Sumw2()    
        g = TGraphAsymmErrors(hPassList[i],hAllList[i],'cp')
        FixEfficiency(g,hPassList[i])
        hEffList.append(hPassList[i].Clone('hEff'+str(i)))
        hEffList[-1].Divide(hAllList[i])
        cSam1 = TCanvas('cSam1')
        hEffList[-1].Draw()
        cSam1.Update()

        for ibin in range(1,hEffList[-1].GetXaxis().GetNbins()+1):
            hEffList[-1].SetBinError(ibin,1*g.GetErrorY(ibin-1))
        #histoStyler(hEffList[-1],hPassList[i].GetLineColor())

        cSam2 = TCanvas('cSam2')
        hEffList[-1].Draw()
        cSam2.Update()


        hEffList[-1].Draw()
    hRatio = hEffList[0].Clone(hName)
    hRatio.Divide(hEffList[1])
    hRatio.GetYaxis().SetRangeUser(0.95,1.05)
    c3 = TCanvas()
    hRatio.Draw()
    c3.Update()
    return hRatio


def pause(str_='push enter key when ready'):
        import sys
        print (str_)
        sys.stdout.flush() 
        input('')

datamc = 'Data'
def stamp(lumi='35.9', showlumi = False, WorkInProgress = True):
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(0.98*tl.GetTextSize())
    tl.DrawLatex(0.135,0.915, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.SetTextSize(1.0/0.98*tl.GetTextSize())
    xlab = 0.213
    if WorkInProgress: tl.DrawLatex(xlab,0.915, ' Preliminary')
    else: tl.DrawLatex(xlab,0.915, ('MC' in datamc)*' simulation '+'preliminary')
    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.81*tl.GetTextSize())    
    thingy = ''
    if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
    xthing = 0.6202
    if not showlumi: xthing+=0.13
    tl.DrawLatex(xthing,0.915,thingy)
    tl.SetTextSize(1.0/0.81*tl.GetTextSize())  


def stamp2(lumi,datamc='MC'):
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(1.6*tl.GetTextSize())
    tl.DrawLatex(0.152,0.82, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.DrawLatex(0.14,0.74, ('MC' in datamc)*' simulation'+' internal')
    tl.SetTextFont(regularfont)
    if lumi=='': tl.DrawLatex(0.62,0.82,'#sqrt{s} = 13 TeV')
    else: tl.DrawLatex(0.47,0.82,'#sqrt{s} = 13 TeV, L = '+str(lumi)+' fb^{-1}')
    #tl.DrawLatex(0.64,0.82,'#sqrt{s} = 13 TeV')#, L = '+str(lumi)+' fb^{-1}')	
    tl.SetTextSize(tl.GetTextSize()/1.6)


#------------------------------------------------------------------------------
def mkcdf(hist, minbin=1):
    hist.Scale(1.0/hist.Integral(1,hist.GetXaxis().GetNbins()))
    c = [0.0]*(hist.GetNbinsX()-minbin+2+1)
    j=1
    for ibin in xrange(minbin, hist.GetNbinsX()+1):
        c[j] = c[j-1] + hist.GetBinContent(ibin)
        j += 1
    c[j] = hist.Integral()
    return c


def FabDraw(cGold,leg,hTruth,hComponents,datamc='MC',lumi=35.9, title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
    cGold.cd()
    pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
    pad1.SetBottomMargin(0.0)
    pad1.SetLeftMargin(0.13)
    if not LinearScale:
        pad1.SetLogy()

    pad1.SetGridx()
    #pad1.SetGridy()
    pad1.Draw()
    pad1.cd()
    for ih in range(1,len(hComponents[1:])+1):
        hComponents[ih].Add(hComponents[ih-1])
        hComponents[ih].SetFillStyle(1001)
        hComponents[ih].SetFillColor(hComponents[ih].GetLineColor())
    hComponents.reverse()        
    if abs(hComponents[0].Integral(-1,999)-1)<0.001:
        hComponents[0].GetYaxis().SetTitle('Normalized')
    else: hComponents[0].GetYaxis().SetTitle('Events/bin')
    cGold.Update()
    hTruth.GetYaxis().SetTitle('Normalized')
    hTruth.GetYaxis().SetTitleOffset(1.15)
    hTruth.SetMarkerStyle(20)
    histheight = 1.5*max(hComponents[0].GetMaximum(),hTruth.GetMaximum())
    if LinearScale: low, high = 0, histheight
    else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hTruth.GetMinimum())), 1000*histheight

    title0 = hTruth.GetTitle()
    if datamc=='MC':
        for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
        leg.AddEntry(hTruth,hTruth.GetTitle(),'lpf')        
    else:
        for ihComp, hComp in enumerate(hComponents):
            leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
        leg.AddEntry(hTruth,title0,'lp')    
    hTruth.SetTitle('')
    hComponents[0].SetTitle('')
    if LinearScale: hComponents[0].GetYaxis().SetRangeUser(0, 1.5*hTruth.GetMaximum())
    else: hComponents[0].GetYaxis().SetRangeUser(0.06*hTruth.GetMinimum(0.01), 100*hTruth.GetMaximum())
    hComponents[0].SetFillStyle(1001)
    hComponents[0].SetFillColor(hComponents[0].GetLineColor())   
    hComponents[0].Draw('hist')
    for h in hComponents[1:]: 
        h.Draw('hist same')
        cGold.Update()
    hComponents[0].Draw('same') 
    hTruth.Draw('p same')
    hTruth.Draw('e same')    
    cGold.Update()
    hComponents[0].Draw('axis same') 
    leg.Draw()        
    cGold.Update()
    #stamp2(lumi,datamc)
    cGold.Update()
    cGold.cd()
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.45)
    pad2.SetLeftMargin(0.13)
    pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    hTruthCopy = hTruth.Clone('hTruthClone'+hComponents[0].GetName())
    hRatio = hTruthCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
    hRatio.SetMarkerStyle(20)
    #hFracDiff = hComponents[0].Clone('hFracDiff')
    #hFracDiff.SetMarkerStyle(20)
    hTruthCopy.SetMarkerStyle(20)
    hTruthCopy.SetMarkerColor(1) 
    #histoStyler(hFracDiff, 1)
    histoStyler(hTruthCopy, 1)
    #hFracDiff.Add(hTruthCopy,-1)
    #hFracDiff.Divide(hTruthCopy)
    #hRatio.Divide(hTruthCopy)
    hRatio.Divide(hComponents[0])
    hRatio.GetYaxis().SetRangeUser(0.2,1.7)
    hRatio.SetTitle('')
    if 'prediction' in title0: hRatio.GetYaxis().SetTitle('(RS-#Delta#phi)/#Delta#phi')
    else: hRatio.GetYaxis().SetTitle(fractionthing)
    hRatio.GetXaxis().SetTitleSize(0.12)
    hRatio.GetXaxis().SetLabelSize(0.11)
    hRatio.GetYaxis().SetTitleSize(0.12)
    hRatio.GetYaxis().SetLabelSize(0.12)
    hRatio.GetYaxis().SetNdivisions(5)
    hRatio.GetXaxis().SetNdivisions(10)
    hRatio.GetYaxis().SetTitleOffset(0.5)
    hRatio.GetXaxis().SetTitleOffset(1.0)
    hRatio.GetXaxis().SetTitle(hTruth.GetXaxis().GetTitle())
    hRatio.Draw()
    hRatio.Draw('e0')    
    pad1.cd()
    hComponents.reverse()
    hTruth.SetTitle(title0)
    return hRatio, [pad1, pad2]


def FabDrawSystyRatio(cGold,leg,hTruth,hComponents,datamc='MC',lumi=35.9, title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
    cGold.cd()
    pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
    pad1.SetBottomMargin(0.0)
    pad1.SetLeftMargin(0.12)

    if not LinearScale:
        pad1.SetLogy()

    #pad1.SetGridx()
    #pad1.SetGridy()
    pad1.Draw()
    pad1.cd()
    for ih in range(1,len(hComponents[1:])+1):
        hComponents[ih].Add(hComponents[ih-1])
    hComponents.reverse()        
    if abs(hComponents[0].Integral(-1,999)-1)<0.001:
        hComponents[0].GetYaxis().SetTitle('Normalized')
    else: hComponents[0].GetYaxis().SetTitle('Events/bin')
    #hComponents[0].GetYaxis().SetTitleSize(0.19)
    cGold.Update()
    hTruth.GetYaxis().SetTitle('Normalized')
    hTruth.GetYaxis().SetTitleOffset(1.15)
    hTruth.SetMarkerStyle(20)
    title0 = hTruth.GetTitle()
    if datamc=='MC':
        for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
        leg.AddEntry(hTruth,hTruth.GetTitle(),'p')        
    else:
        for ihComp, hComp in enumerate(hComponents):
            leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
        leg.AddEntry(hTruth,title0,'p')    
    hTruth.SetTitle('')
    hComponents[0].SetTitle('')	
    xax = hComponents[0].GetXaxis()
    hComponentsUp = hComponents[0].Clone(hComponents[0].GetName()+'UpVariation')
    hComponentsUp.SetLineColor(kWhite)	
    hComponentsDown = hComponents[0].Clone(hComponents[0].GetName()+'DownVariation')	
    hComponentsDown.SetFillColor(10)
    hComponentsDown.SetFillStyle(1001)
    hComponentsDown.SetLineColor(kWhite)
    for ibin in range(1, xax.GetNbins()+1):
        hComponentsUp.SetBinContent(ibin, hComponents[0].GetBinContent(ibin)+hComponents[0].GetBinError(ibin))
        hComponentsDown.SetBinContent(ibin, hComponents[0].GetBinContent(ibin)-hComponents[0].GetBinError(ibin))		

    #hComponents[0].Draw('hist')
    hComponentsUp.Draw('hist')
    hComponents[0].Draw('hist same')
    hComponentsDown.Draw('hist same')
    for h in hComponents[1:]: 
        h.Draw('hist same')
        cGold.Update()
    #hComponents[0].Draw('same') 
    hTruth.Draw('hist p same')
    hTruth.Draw('e same')    
    cGold.Update()
    hComponents[0].Draw('axis same')           
    leg.Draw()        
    cGold.Update()
    stampFab(lumi,datamc)
    cGold.Update()
    cGold.cd()
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.42)
    pad2.SetLeftMargin(0.12)
    #pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    hTruthCopy = hTruth.Clone('hTruthClone'+hComponents[0].GetName())
    hRatio = hTruthCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
    hRatio.SetMarkerStyle(20)
    #hFracDiff = hComponents[0].Clone('hFracDiff')
    #hFracDiff.SetMarkerStyle(20)
    hTruthCopy.SetMarkerStyle(20)
    hTruthCopy.SetMarkerColor(1) 
    #histoStyler(hFracDiff, 1)
    histoStyler(hTruthCopy, 1)
    #hFracDiff.Add(hTruthCopy,-1)
    #hFracDiff.Divide(hTruthCopy)
    #hRatio.Divide(hTruthCopy)
    histoByWhichToDivide = hComponents[0].Clone()
    for ibin in range(1, xax.GetNbins()+1): histoByWhichToDivide.SetBinError(ibin, 0)
    hRatio.Divide(histoByWhichToDivide)
    hRatio.GetYaxis().SetRangeUser(0.0,.1)###
    hRatio.SetTitle('')
    if 'prediction' in title0: hFracDiff.GetYaxis().SetTitle('(RS-#Delta#phi)/#Delta#phi')
    else: hRatio.GetYaxis().SetTitle(fractionthing)
    hRatio.GetXaxis().SetTitleSize(0.12)
    hRatio.GetXaxis().SetLabelSize(0.11)
    hRatio.GetYaxis().SetTitleSize(0.12)
    hRatio.GetYaxis().SetLabelSize(0.12)
    hRatio.GetYaxis().SetNdivisions(5)
    hRatio.GetXaxis().SetNdivisions(10)
    hRatio.GetYaxis().SetTitleOffset(0.5)
    hRatio.GetXaxis().SetTitleOffset(1.0)
    hRatio.GetXaxis().SetTitle(hTruth.GetXaxis().GetTitle())
    hRatio.Draw()


    histoMethodFracErrorNom = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystNom')
    histoMethodFracErrorNom.SetLineColor(kBlack)
    histoMethodFracErrorNom.SetFillStyle(1)
    histoMethodFracErrorUp = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystUp')
    histoMethodFracErrorUp.SetFillStyle(3001)
    histoMethodFracErrorUp.SetLineColor(kWhite)	
    histoMethodFracErrorUp.SetFillColor(hComponents[0].GetFillColor())	
    histoMethodFracErrorDown = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystDown')
    histoMethodFracErrorDown.SetLineColor(kWhite)
    #histoMethodFracErrorDown.SetFillStyle(1001)
    histoMethodFracErrorDown.SetFillColor(10)
    for ibin in range(1, xax.GetNbins()+1): 
        content = histoMethodFracErrorUp.GetBinContent(ibin)
        if content>0: err = histoMethodFracErrorUp.GetBinError(ibin)/content
        else: err = 0
        histoMethodFracErrorUp.SetBinContent(ibin, 1+err)
        histoMethodFracErrorUp.SetBinError(ibin, 0)
        histoMethodFracErrorDown.SetBinContent(ibin, 1-err)
        histoMethodFracErrorDown.SetBinError(ibin, 0)		
        histoMethodFracErrorNom.SetBinContent(ibin, 1)		
        histoMethodFracErrorNom.SetBinError(ibin, 0)
    #hRatio.GetYaxis().SetRangeUser(-0.2,2.7)
    hRatio.GetYaxis().SetRangeUser(0.2,1.7)
    hRatio.Draw('e0')    
    histoMethodFracErrorUp.Draw('same hist')	
    histoMethodFracErrorNom.Draw('same')
    histoMethodFracErrorDown.Draw('same hist')
    hRatio.Draw('e0 same')
    hRatio.Draw('axis same')
    pad1.cd()
    hComponents.reverse()
    hTruth.SetTitle(title0)
    pad1.Update()

    return hRatio, [histoMethodFracErrorNom, histoMethodFracErrorUp, histoMethodFracErrorDown, hComponentsUp, hComponentsDown, pad1, pad2]

def stampFab(lumi,datamc='MC'):
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(1.6*tl.GetTextSize())
    tl.DrawLatex(0.152,0.82, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.DrawLatex(0.14,0.74, ('MC' in datamc)*' simulation'+' internal')
    tl.SetTextFont(regularfont)
    if lumi=='': tl.DrawLatex(0.58,0.82,'#sqrt{s} = 13 TeV')
    else: tl.DrawLatex(0.46,0.82,'#sqrt{s} = 13 TeV, L = '+str(lumi)+' fb^{-1}')
    #tl.DrawLatex(0.64,0.82,'#sqrt{s} = 13 TeV')#, L = '+str(lumi)+' fb^{-1}')	
    tl.SetTextSize(tl.GetTextSize()/1.6)


def stampE(energy):
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(.8*tl.GetTextSize())
    tl.SetTextFont(regularfont)
    tl.DrawLatex(0.68,.91,'#sqrt{s} = 13 TeV')#(L = '+str(lumi)+' '#fb^{-1}')##from Akshansh

