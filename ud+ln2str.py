from __future__ import print_function
import io
import os
import numpy
from collections import OrderedDict
from conllu import parse, parse_tree
# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')


testfile = "test-listnet-test-it.txt" #test-02.conll"#
HVRPredFile = "it-test-HVR-PoSDeP.txt.pred"
fileHVRPredFile = open(HVRPredFile)

def augmentTree(tn):
    if(tn.children):
        i = 0
        while ((i < len(tn.children)) and (tn.children[i].data.get("id") < tn.data.get("id")) ):
            tn.children[i].data["predictedIslandPosition"] = int(fileHVRPredFile.readline())
            i+=1
        tn.data["predictedIslandPosition"] = int(fileHVRPredFile.readline())
        while (i < len(tn.children)):
            tn.children[i].data["predictedIslandPosition"] = int(fileHVRPredFile.readline())
            i+=1
        for c in tn.children:
            augmentTree(c)

def visitNewPositionTree(tn):
    tn.children.sort(key = lambda x : x.data["predictedIslandPosition"])
    if(not(tn.children)):
        print(tn.data.get("form") +"-"+ str(tn.data.get("predictedIslandPosition"))+"-"+str(tn.data.get("id")))
    else:
        i = 0
        while ((i < len(tn.children)) and (tn.children[i].data.get("predictedIslandPosition") < tn.data.get("predictedIslandPosition"))):
            visitNewPositionTree(tn.children[i])
            i+=1
        print(tn.data.get("form")+"-"+ str(tn.data.get("predictedIslandPosition"))+"-"+str(tn.data.get("id")))
        while (i < len(tn.children)):
            #print("Sono qui!!!")
            visitNewPositionTree(tn.children[i])
            i+=1

        
#read the conll file and process the tree one-by-one
file = open(testfile)
stringTree =""
for line in file:
    if(line != '\n'):        
        #print line#DEBUG
        stringTree += line
    else:
        #print(stringTree)#DEBUG
        tree = parse_tree(stringTree)[0]
        #print(tree)
        augmentTree(tree)
        #print(tree)
        visitNewPositionTree(tree)
        print("\n")
        stringTree = ""
