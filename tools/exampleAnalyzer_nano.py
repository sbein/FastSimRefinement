#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class ExampleAnalysis(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)

        self.h_vpt = ROOT.TH1F('sumpt', 'sumpt', 100, 0, 1000)
        self.addObject(self.h_vpt)

    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        eventSum = ROOT.TLorentzVector()

        # select events with at least 2 muons
        if len(muons) >= 1:
            for lep in muons:  # loop on muons
                eventSum += lep.p4()
            for lep in electrons:  # loop on electrons
                eventSum += lep.p4()
            for j in jets:  # loop on jets
                eventSum += j.p4()
            self.h_vpt.Fill(eventSum.Pt())  # fill histogram

        return True


preselection = "Jet_pt[0] > 30"
preselection = '1==1'
files = [" file:/nfs/dust/cms/user/beinsam/FastSim/CMSSW_10_6_22/src/TTbar/Fast/1668/step3_inNANOAODSIM.root"]
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[
                  ExampleAnalysis()], noOut=True, histFileName="histOut.root", histDirName="plots")
p.run()
