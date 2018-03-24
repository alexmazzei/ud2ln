from __future__ import print_function
import io
import os
import numpy
from sets import Set
from collections import OrderedDict
from conllu import parse, parse_tree



# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

debugfile = "test-02.conll"
devfile = "test-listnet-dev-it.txt"
trainfile = "test-listnet-train-it.txt"
testfile = "test-listnet-test-it.txt"
learnfile = trainfile

globalInteger = 1;

def exploreTree(tn):
    global globalInteger
    if(tn.children):
        #print globalInteger , "---------" , globalInteger#DEBUG
        d = {"depRel" :  tn.data.get("deprel") , "uPoS" :  tn.data.get("upostag"), "xPoS" :  tn.data.get("xpostag") , "lemma" :  tn.data.get("lemma"), "groupId" : globalInteger, "originalPosition" : tn.data.get("id") , "form" : tn.data.get("form"), "isHead" : True}
        l=[d]
        for c in tn.children:
            dc = {"depRel" :  c.data.get("deprel") , "uPoS" :  c.data.get("upostag") ,"xPoS" :  tn.data.get("xpostag") , "lemma" :  tn.data.get("lemma"), "groupId" : globalInteger, "originalPosition" : c.data.get("id") , "form" : c.data.get("form"), "isHead" : False}
            l.append(dc)
        newL = sorted (l,key = lambda x : x['originalPosition'])
        i = 1
        for el in newL:
            el["newPosition"]=i
            i += 1
        out = "" #groupId,uPoS,xPos,dep,isHead,newPosition
        for node in newL:
            out = out + str (node.get('groupId')) + ','
            if(uPoS2HVRuPoS.has_key(node.get('uPoS'))):
                out = out + uPoS2HVRuPoS.get(node.get('uPoS'))  + ","
            else:
                out = out + uPoS2HVRuPoS.get('UNK')
            if(xPoS2HVRxPoS.has_key(node.get('xPoS'))):
                out = out + xPoS2HVRxPoS.get(node.get('xPoS'))  + ","
            else:
                out = out + xPoS2HVRxPoS.get('UNK')
            if(dep2HVRdep.has_key(node.get('depRel'))):
                out = out + dep2HVRdep.get(node.get('depRel'))  + ","
            else:
                out = out + dep2HVRdep.get('UNK')  + ","
            if node.get('isHead'):
                out = out + "1,"
            else:
                out = out + "0,"
            out = out + str( node.get('newPosition')) + "\n"
        print(out,end="")
        globalInteger = globalInteger + 1
        
        for c in tn.children:            
            exploreTree(c)
            
#read the PoSs in the train file and convert into a hot-vector representation by using a dictionary

# old method using the shell
#f = os.popen("cut  -f 4 " + trainfile + " | sort | uniq")
#PoSList = filter(None,f.read().split("\n"))
#f = os.popen("cut  -f 8 " + trainfile + " | sort | uniq")
#depList = filter(None,f.read().split("\n"))



# read the entire learn file to extract features and convert to binary string
lemmaSet =  Set([u'UNK',u'PropName'])
upostagList = [u'UNK']
xpostagList = [u'UNK']
deprelList = [u'UNK']

file1 = open(learnfile)
stringTree =""
for line in file1:
    if(line != '\n'):        
        stringTree += line
    else:
        flatTree = parse(stringTree)
        for node in flatTree[0]:
            # if ((node.get("upostag") !=  "PROPN") and (node.get("lemma") not in lemmaSet) ):
            #     lemmaSet.add(node.get("lemma"))
            if (node.get("upostag") not in upostagList):
                upostagList.append(node.get("upostag"))
            if (node.get("xpostag") not  in xpostagList):
                xpostagList.append(node.get("xpostag"))
            if (node.get("deprel") not in deprelList):
                deprelList.append(node.get("deprel"))
        stringTree = ""
lemmaList = list(lemmaSet)

# We should use lemma??
# lemma2HVRlemma = {}
# for lemma,i in zip (lemmaList,range(len(lemmaList)) ):
#     lemma2HVRlemma[lemma] = ",".join(map(str, numpy.eye(len(lemma), dtype=int)[i]))
uPoS2HVRuPoS = {}
for uPoS,i in zip (upostagList,range(len(upostagList)) ):
    uPoS2HVRuPoS[uPoS] = ",".join(map(str, numpy.eye(len(upostagList), dtype=int)[i]))
xPoS2HVRxPoS = {}
for xPoS,i in zip (xpostagList,range(len(xpostagList)) ):
    xPoS2HVRxPoS[xPoS] = ",".join(map(str, numpy.eye(len(xpostagList), dtype=int)[i]))
dep2HVRdep = {}
for dep,i in zip (deprelList,range(len(deprelList)) ):
    dep2HVRdep[dep] = ",".join(map(str, numpy.eye(len(deprelList), dtype=int)[i]))


#read the conll file and process the tree one-by-one
file = open(learnfile)
stringTree =""
for line in file:
    if(line != '\n'):        
        stringTree += line
    else:
        #print(stringTree)#DEBUG
        exploreTree(parse_tree(stringTree)[0])
        stringTree = ""



        
