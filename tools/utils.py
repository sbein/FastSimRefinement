import sys
from ROOT import *
from array import array
import numpy as np

tl = TLatex()
tl.SetNDC()
cmsTextFont = 61
extraTextFont = 52
lumiTextSize = 0.6
lumiTextOffset = 0.2
cmsTextSize = 0.75
cmsTextOffset = 0.1
regularfont = 42
originalfont = tl.GetTextFont()

def histoStyler(h,color):
    h.SetLineWidth(2)
    h.SetLineColor(color)
    size = 0.045
    font = 132
    h.GetXaxis().SetLabelFont(font)
    h.GetYaxis().SetLabelFont(font)
    h.GetXaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleSize(size)
    h.GetXaxis().SetTitleSize(size)
    h.GetXaxis().SetLabelSize(size)   
    h.GetYaxis().SetLabelSize(size)
    h.GetXaxis().SetTitleOffset(0.95)
    h.GetYaxis().SetTitleOffset(1.1)
    h.Sumw2()

def mkcanvas(name='canvas'):
    c = TCanvas(name,name, 800, 800)
    c.SetTopMargin(0.07)
    c.SetBottomMargin(0.15)
    c.SetLeftMargin(0.19)
    return c

def mklegend(x1=.22, y1=.66, x2=.69, y2=.82, color=kWhite):
	lg = TLegend(x1, y1, x2, y2)
	lg.SetFillColor(color)
	lg.SetTextFont(42)
	lg.SetBorderSize(0)
	lg.SetShadowColor(kWhite)
	lg.SetFillStyle(0)
	return lg

def mk6canvas(name='canvas'):
    c = TCanvas(name,name, 1200, 800)
    c.Divide(3,2)
    for ipad in range(1, 6+1):
        pad = c.GetPad(ipad)
        pad.SetTopMargin(0.07)
        pad.SetBottomMargin(0.07)
        pad.SetLeftMargin(0.07)
    return c

def mk9canvas(name='canvas'):
    c = TCanvas(name,name, 1350, 850)
    c.Divide(3,3)
    for ipad in range(1, 9+1):
        pad = c.GetPad(ipad)
        pad.SetTopMargin(0.02)
        pad.SetBottomMargin(0.12)
        pad.SetLeftMargin(0.12)
    return c

def fillth1(h,x,weight=1):
	h.Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon),weight)

def fillth2(h,x,y,weight=1):
	h.Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon), min(max(y,h.GetYaxis().GetBinLowEdge(1)+epsilon),h.GetYaxis().GetBinLowEdge(h.GetYaxis().GetNbins()+1)-epsilon),weight)
    
def mkmet(metPt, metPhi):
    met = TLorentzVector()
    met.SetPtEtaPhiE(metPt, 0, metPhi, metPt)
    return met

def pause(thingy='please push enter'):
    import sys
    print (thingy)
    sys.stdout.flush()
    input('')




def FabDraw(cGold,leg,hTruth,hComponents,datamc='MC',lumi=35.9, title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
	print ('datamc in FabDraw')
	cGold.cd()
	pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
	pad1.SetBottomMargin(0.0)
	pad1.SetLeftMargin(0.12)
	if not LinearScale:
		pad1.SetLogy()

	pad1.SetGridx()
	#pad1.SetGridy()
	pad1.Draw()
	pad1.cd()
	for ih in range(1,len(hComponents[1:])+1):
		hComponents[ih].Add(hComponents[ih-1])
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
	else: hComponents[0].GetYaxis().SetRangeUser(0.001, 100*hTruth.GetMaximum())
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
	stamp2(lumi,datamc)
	cGold.Update()
	cGold.cd()
	pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
	pad2.SetTopMargin(0.0)
	pad2.SetBottomMargin(0.3)
	pad2.SetLeftMargin(0.12)
	pad2.SetGridx()
	pad2.SetGridy()
	pad2.Draw()
	pad2.cd()
	hTruthCopy = hComponents[0].Clone('hTruthClone'+hComponents[0].GetName())
	hRatio = hTruthCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
	#hRatio.SetMarkerStyle(20)
	#hFracDiff = hComponents[0].Clone('hFracDiff')
	#hFracDiff.SetMarkerStyle(20)
	#hTruthCopy.SetMarkerStyle(20)
	#hTruthCopy.SetMarkerColor(1) 
	#histoStyler(hFracDiff, 1)
	#histoStyler(hTruthCopy, 1)
	#hFracDiff.Add(hTruthCopy,-1)
	#hFracDiff.Divide(hTruthCopy)
	#hRatio.Divide(hTruthCopy)
	hRatio.Divide(hTruth)
	hRatio.GetYaxis().SetRangeUser(0.0,2.0)###
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
	hRatio.Draw('e0 hist')    
	pad1.cd()
	hComponents.reverse()
	hTruth.SetTitle(title0)
	return hRatio, [pad1, pad2]


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


    
