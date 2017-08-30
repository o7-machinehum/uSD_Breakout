# -*- coding: utf-8 -*-
#
# A script to check for annular ring violations
# both for pads and vias
#
## todo
# add colors to print

import sys
import pcbnew
from pcbnew import *

___version___="1.4"

mm_ius = 1000000.0
# (consider always drill +0.1)
DRL_EXTRA=0.1
DRL_EXTRA_ius=DRL_EXTRA * mm_ius

AR_SET = 0.150   #minimum annular accepted for pads
MIN_AR_SIZE = AR_SET * mm_ius

AR_SET_V = 0.150  #minimum annular accepted for vias
MIN_AR_SIZE_V = AR_SET_V * mm_ius

def annring_size(pad):
    # valid for oval pad/drills
    annrX=(pad.GetSize()[0] - (pad.GetDrillSize()[0]+DRL_EXTRA_ius))/2
    annrY=(pad.GetSize()[1] - (pad.GetDrillSize()[1]+DRL_EXTRA_ius))/2
    #annr=min(pad.GetSize()) - max(pad.GetDrillSize())
    #if annr < MIN_AR_SIZE:
    #print pad.GetSize()[0]/mm_ius
    #print pad.GetDrillSize()[0]/mm_ius
    #print (pad.GetDrillSize()[0]+DRL_EXTRA_ius)/mm_ius
    #print annrX/mm_ius
    return min(annrX,annrY)

def vias_annring_size(via):
    # calculating via annular
    annr=(via.GetWidth() - (via.GetDrillValue()+DRL_EXTRA_ius))/2
    #print via.GetWidth()
    #print via.GetDrillValue()
    return annr
    
def f_mm(raw):
    return repr(raw/mm_ius)

board = pcbnew.GetBoard()
PassC=FailC=0
PassCV=FailCV=0

print("annular.py Testing PCB for Annular Ring Pads >= "+repr(AR_SET)+" Vias >= "+repr(AR_SET_V))
print("version = "+___version___)

# print "LISTING VIAS:"
for item in board.GetTracks():
    if type(item) is pcbnew.VIA:
        pos = item.GetPosition()
        drill = item.GetDrillValue()
        width = item.GetWidth()
        ARv = vias_annring_size(item)
        if ARv  < MIN_AR_SIZE_V:
        #            print("AR violation at %s." % (pad.GetPosition() / mm_ius ))  Raw units, needs fixing
            XYpair =  item.GetPosition()
            print("AR violation of "+f_mm(ARv)+" at XY "+f_mm(XYpair[0])+","+f_mm(XYpair[1]) )
            FailCV = FailCV+1
        else:
            PassCV = PassCV+1
    #print type(item)
print("VIAS that Pass = "+repr(PassCV)+" Fails = "+repr(FailCV))

for module in board.GetModules():
    for pad in module.Pads():
        ARv = annring_size(pad)
        #print(f_mm(ARv))
        if ARv  < MIN_AR_SIZE:
#            print("AR violation at %s." % (pad.GetPosition() / mm_ius ))  Raw units, needs fixing
            XYpair =  pad.GetPosition()
            print("AR violation of "+f_mm(ARv)+" at XY "+f_mm(XYpair[0])+","+f_mm(XYpair[1]) )
            FailC = FailC+1
        else:
            PassC = PassC+1
print("PADS that Pass = "+repr(PassC)+" Fails = "+repr(FailC))


#  execfile("annular.py")
# annular.py Testing PCB for Annular Ring >= 0.15
# AR violation of 0.1 at XY 172.974,110.744
# VIAS that Pass = 100 Fails = 1
# AR violation of 0.1 at XY 172.212,110.744
# AR violation of 0.0 at XY 154.813,96.52
# PADS that Pass = 49 Fails = 2

