from nltk import pos_tag,word_tokenize

def mergeHelpingverbs(stringList):
    a=""
    if len(stringList)==0:
        return ""
    if len(stringList)<1:
        a=a+stringList.pop(0)
        return a.upper()
    for i in stringList:
        if(stringList[-1]!=i):
            a+=i+"_"
        elif(stringList[-1]==i):
            a+=i
    return a.upper()

def process_Data(sentence):

    tokens = word_tokenize(sentence)
    postTaggList = pos_tag(tokens)

    verbs = []                  #List of All the verbs...
    properties = []             #List of Properties...
    whfamily = []               #List of Wh family
    nouns = []                  #List of Nouns....


    for item in postTaggList:

        if item[0] in ["son" , "father" , "brother" , "mother" , "sister"]:

            verbs.append(item[0])

        elif item[1] in ["NNP","NN"]:

            nouns.append(item[0])

        elif item[1] in ["VBZ", "VBD", "VBG", "DT", "IN", "VBP", "TO", "VB", 'NNS','JJ']:

            verbs.append(item[0])

        elif item[1] in ["VBN", "RB"]:
            properties.append(item[0])

        elif item[1] in ["WP"]:
            whfamily.append(item[0])

        elif item[1] in ["PRP$"]:
            if(item[0] not in ['I','My','Me']):
                whfamily.append(item[0])

    return nouns, verbs , properties , whfamily