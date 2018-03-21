import os
import numpy
from collections import OrderedDict
from conllu import parse, parse_tree

globalInteger = 1;


#print numpy.eye(5, dtype=int)[4]



def myprint(d):    
    for k, v in d.iteritems():
        if isinstance(v, dict):
            myprint(v)
        else:
            print "{0} : {1}".format(k, v)


def myPrintNode(tn):
    d = tn.data
    print d.get("id"), d.get("form")

def myVisit(l):
    num = 0
    print num
    num = num + 1
    for tn in l:
        d = {tn.data.get("id") : tn.data}
        myPrintNode(tn)
        for c in tn.children:
            d[c.data.get("id")] = c.data
            myPrintNode(c)
        od = OrderedDict(sorted(d.items(), key=lambda t: t[0]))


def exploreTree(tn):
    global globalInteger
    if(tn.children):
        print globalInteger , "---------" , globalInteger
        d = {"depRel" :  tn.data.get("deprel") , "uPoS" :  tn.data.get("upostag") , "groupId" : globalInteger, "originalPosition" : tn.data.get("id") , "form" : tn.data.get("form"), "isHead" : True}
        l=[d]
        for c in tn.children:
            dc = {"depRel" :  c.data.get("deprel") , "uPoS" :  c.data.get("upostag") , "groupId" : globalInteger, "originalPosition" : c.data.get("id") , "form" : c.data.get("form"), "isHead" : False}
            l.append(dc)
        newL = sorted (l,key = lambda x : x['originalPosition'])
        i = 1
        for el in newL:
            el["newPosition"]=i
            i += 1
        print newL
        #print l
        globalInteger = globalInteger + 1
        for c in tn.children:            
            exploreTree(c)


#read the PoSs in the train file and convert into a hot-vector representation by using a dictionary
f = os.popen('cut  -f 4 it-ud-dev.conll | sort | uniq')
PoSList = filter(None,f.read().split("\n"))
print PoSList #DEBUG
PoS2HVRPoS = {}
for PoS,i in zip (PoSList,range(len(PoSList)) ):
    PoS2HVRPoS[PoS] = ",".join(map(str, numpy.eye(len(PoSList), dtype=int)[i]))
print 'AUX=',PoS2HVRPoS['AUX'] #DEBUG

#read the deps the train file and convert into a hot-vector representation by using a dictionary
f = os.popen('cut  -f 8 it-ud-dev.conll | sort | uniq')
depList = filter(None,f.read().split("\n"))
print depList #DEBUG
dep2HVRPoS = {}
for dep,i in zip (depList,range(len(depList)) ):
    dep2HVRPoS[dep] = ",".join(map(str, numpy.eye(len(depList), dtype=int)[i]))
print 'xcomp=',dep2HVRPoS['xcomp'] #DEBUG


    
        

data = """
1   The     the    DET    DT   Definite=Def|PronType=Art   4   det     _   _
2   quick   quick  ADJ    JJ   Degree=Pos                  4   amod    _   _
3   brown   brown  ADJ    JJ   Degree=Pos                  4   amod    _   _
4   fox     fox    NOUN   NN   Number=Sing                 5   nsubj   _   _
5   jumps   jump   VERB   VBZ  Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin   0   root    _   _
6   over    over   ADP    IN   _                           9   case    _   _
7   the     the    DET    DT   Definite=Def|PronType=Art   9   det     _   _
8   lazy    lazy   ADJ    JJ   Degree=Pos                  9   amod    _   _
9   dog     dog    NOUN   NN   Number=Sing                 5   nmod    _   SpaceAfter=No
10  .       .      PUNCT  .    _                           5   punct   _   _

"""

pt = parse_tree(data)

#print pt
#print "----------\n"
#myprint (pt[0][1][0][0])
#myVisit(pt)
exploreTree(pt[0])


