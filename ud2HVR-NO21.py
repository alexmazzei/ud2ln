#!/home/ubuntu/venv/bin/python


#from __future__ import print_function
import io
import os
import numpy
#from sets import Set
from collections import OrderedDict
from conllu import parse, parse_tree
# encoding=utf8  
import sys  
#reload(sys)  
#sys.setdefaultencoding('utf8')

#from polyglot.mapping import Embedding #there are other embeddings to test, for instance glove
import fasttext

#Algorithm
#1. read the feature file to find the feature set and prepare the datastructures
#2. read the content file by using the recursive function exploreTree


featuresFile = sys.argv[1]  #File UD used only to create the "feature
                            #set". The features values will be
                            #numeric: 0/1 or real
encodeFile   = sys.argv[2]  #File UD that will be encoded into a
                            #numeric CSV file representing the feature
                            #values
emb_lang     = sys.argv[3]  ##The code language for the embeddings to use 
                            
globalInteger = 1;          #global index




#NOTE: exploreTree is a recursive function that explore top-down the tree and prints to the console

def exploreTree(tn):
    global globalInteger
    if(tn.children):
        if (tn.token.get("feats") is not None and tn.token.get("feats").get("original_id") is not None):
            new_position =  tn.token.get("feats").get("original_id")
        else:
            new_position =  tn.token.get("id") 
        #print globalInteger , "---------" , globalInteger#DEBUG
        d = {"depRel" :  tn.token.get("deprel") , "uPoS" :  tn.token.get("upostag"), "xPoS" :  tn.token.get("xpostag") , "lemma" :  tn.token.get("lemma"), "groupId" : globalInteger, "originalPosition" : new_position , "form" : tn.token.get("form"), "feats" : tn.token.get("feats"), "isHead" : True}
        l=[d]
        for c in tn.children:
            if (c.token.get("feats") is not None and c.token.get("feats").get("original_id") is not None):
                new_position =  c.token.get("feats").get("original_id")
            else:
                new_position =  c.token.get("id")                                    
            dc = {"depRel" :  c.token.get("deprel") , "uPoS" :  c.token.get("upostag") ,"xPoS" :  c.token.get("xpostag") , "lemma" :  c.token.get("lemma"), "groupId" : globalInteger, "originalPosition" : new_position , "form" : c.token.get("form"), "feats" : c.token.get("feats"), "isHead" : False}
            l.append(dc)
        newL = sorted (l,key = lambda x : x['originalPosition'])
        i = 1
        for el in newL:
            el["newPosition"]=i
            i += 1
        out = ""#groupId,lemma,uPoS,xPos,dep,isHead,newPosition
        for node in newL:
            #out = out+"lemma="+node.get('lemma')
            out = out + str (node.get('groupId')) + ','
            #Embeddings
            embLemma = emb.get_word_vector(str(node.get('lemma'))) #fasttext!
            #embLemma = emb.get(str(node.get('lemma')))
            #embLemma = emb.get(str(node.get('form')))#In SRST18 lemma and forma are inverted!!!
            #print("uPos="+node.get("uPoS"))
            if ((node.get("uPoS") not in closedUPoS) and (embLemma is not None)):
                #print("Sono qui!!"+node.get("uPoS"))
                for n in embLemma:
                    out = out + str(n) +","
            else:
                out = out + "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"#TODO
            #ClosedLemma
            if(node.get('lemma') in lemma2HVRlemma):
                out = out + lemma2HVRlemma.get(node.get('lemma'))  + ","
            else:
                out = out + lemma2HVRlemma.get('UNK')+ ","
            if(node.get('uPoS') in uPoS2HVRuPoS):
                out = out + uPoS2HVRuPoS.get(node.get('uPoS'))  + ","
            else:
                out = out + uPoS2HVRuPoS.get('UNK')  + ","
            if(node.get('xPoS') in xPoS2HVRxPoS ):#NO for PT!!!
                out = out + xPoS2HVRxPoS.get(node.get('xPoS'))  + ","
            else:
                out = out + xPoS2HVRxPoS.get('UNK')  + ","
            if (node.get("feats") is not None):
                for key in mfeat2HVR:
                    #print("k="+key)
                    #print("f+k="+str(node.get("feats").get(key)))
                    if (((node.get("feats").get(key)) is not None) and (mfeat2HVR[key].get(node.get("feats").get(key)) is not None)):
                        out = out + mfeat2HVR[key][node.get("feats").get(key)]  + ","
                    else:
                        out = out + mfeat2HVR[key][u'NaV']  + ","
            else:
                for key in mfeat2HVR:
                    out = out + mfeat2HVR[key][u'NaV']  + ","
            if(node.get('depRel') in dep2HVRdep):
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

        #ricorsione in coda su tutti i figli!
        for c in tn.children:            
            exploreTree(c)
            


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>            
# read the entire feature file to extract features and convert to binary string
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# #embeddings !!!LANGUAGE DEPENDENT!!!
if(emb_lang == "it"):
    #emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/it/embeddings_pkl.tar.bz2")
    emb =  fasttext.load_model('/home/ubuntu/data/embeddings/cc.it.64.bin')
elif(emb_lang == "en"):
    #emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/en/embeddings_pkl.tar.bz2")
    emb =  fasttext.load_model('/home/ubuntu/data/embeddings/cc.en.64.bin')
#elif(emb_lang == "fr"):
#    emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/fr/embeddings_pkl.tar.bz2")
elif(emb_lang == "es"):
    #emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/es/embeddings_pkl.tar.bz2")
    emb =  fasttext.load_model('/home/ubuntu/data/embeddings/cc.es.64.bin')
#elif(emb_lang == "pt"):
#    emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/pt/embeddings_pkl.tar.bz2")
#elif(emb_lang == "ar"): #arabic
#    emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/ar/embeddings_pkl.tar.bz2")
elif(emb_lang == "zh"): #chinese
    #emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/zh/embeddings_pkl.tar.bz2")
    emb =  fasttext.load_model('/home/ubuntu/data/embeddings/cc.zh.64.bin')
elif(emb_lang == "hi"): #hindi
    #emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/hi/embeddings_pkl.tar.bz2")
    emb =  fasttext.load_model('/home/ubuntu/data/embeddings/cc.hi.64.bin')
#elif(emb_lang == "id"): #indonesian
#    emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/id/embeddings_pkl.tar.bz2")
#elif(emb_lang == "ja"): #japanese
#    emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/ja/embeddings_pkl.tar.bz2")
#elif(emb_lang == "ko"): #korean
#    emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/ko/embeddings_pkl.tar.bz2")
#elif(emb_lang == "ru"):
#    emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/ru/embeddings_pkl.tar.bz2")
else:
    exit("Language not supported")    
    
# list of the closed PoS tags in Google PoS set
closedUPoS = ['ADP','AUX','CCONJ','DET','PART','PRON','SCONJ','PUNCT'] 

lemmaSet =  set([u'UNK'])
upostagList = [u'UNK']
xpostagList = [u'UNK']
deprelList = [u'UNK']
mfeatsDict = {}


file1 = open(featuresFile)
stringTree =""
for line in file1:
    if(line != '\n'):        
        stringTree += line
    else:
        #print(stringTree)#DEBUG
        flatTree = parse(stringTree)
        for node in flatTree[0]:
            if ((node.get("upostag") in closedUPoS) and (node.get("lemma") not in lemmaSet)):
                lemmaSet.add(node.get("lemma"))
                #print("closedLemma="+(node.get("lemma")))
            if (node.get("upostag") not in upostagList):
                upostagList.append(node.get("upostag"))
            if (node.get("xpostag") not  in xpostagList):
                xpostagList.append(node.get("xpostag"))
            if (node.get("feats") is not None):
#                for i, (key, value) in enumerate(node.get("feats").iteritems()):
                for i, (key, value) in enumerate(iter(node.get("feats").items())):    
                    #print(key+value)                    
                    if (key != "lin" and key != "original_id"): ##2019 
                        if (key not in mfeatsDict):
                            mfeatsDict[key] =[u'NaV']
                            mfeatsDict[key].append(value)
                        else:
                            if (value not in mfeatsDict[key]):
                                mfeatsDict[key].append(value)
            if (node.get("deprel") not in deprelList):
                deprelList.append(node.get("deprel"))
        stringTree = ""
lemmaList = list(lemmaSet)


lemma2HVRlemma = {} #NOTE: HVR is used only for closed PoS categories.
for lemma,i in zip (lemmaList,range(len(lemmaList))):
    lemma2HVRlemma[lemma] = ",".join(map(str, numpy.eye(len(lemmaList), dtype=int)[i]))
#print("lemma2HVRlemma="+str(lemma2HVRlemma))
uPoS2HVRuPoS = {}
for uPoS,i in zip (upostagList,range(len(upostagList)) ):
    uPoS2HVRuPoS[uPoS] = ",".join(map(str, numpy.eye(len(upostagList), dtype=int)[i]))
xPoS2HVRxPoS = {}
for xPoS,i in zip (xpostagList,range(len(xpostagList)) ):
    xPoS2HVRxPoS[xPoS] = ",".join(map(str, numpy.eye(len(xpostagList), dtype=int)[i]))        
dep2HVRdep = {}
for dep,i in zip (deprelList,range(len(deprelList)) ):
    dep2HVRdep[dep] = ",".join(map(str, numpy.eye(len(deprelList), dtype=int)[i]))
mfeat2HVR = {}
for key in mfeatsDict:
    mfeat2HVR[key] ={}
    for value,i in zip (mfeatsDict[key],range(len(mfeatsDict[key]))):
        mfeat2HVR[key][value] = ",".join(map(str, numpy.eye(len(mfeatsDict[key]), dtype=int)[i]))
        #print(key+"-"+value+"="+mfeat2HVR[key][value])


#NOTE: this is the main alghorithm        
#read the conll file and process the tree one-by-one to convert in 0-1
file = open(encodeFile)
stringTree =""
for line in file:
    if(line != '\n'):        
        stringTree += line
    else:
        #print(stringTree)#DEBUG
        exploreTree(parse_tree(stringTree)[0])
        stringTree = ""



