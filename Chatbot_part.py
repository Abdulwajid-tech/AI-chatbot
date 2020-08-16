import aiml
from Neo4j_part import storeIpAddressAndHostName , makeSemanticNetwork

kernal = aiml.Kernel()

storeIpAddressAndHostName()

aimlFilesList = ["aboutuni.aiml","animal.aiml","cblock.aiml","course.aiml","ground.aiml","hblock.aiml","nblock.aiml","phdblock","person.aiml"]

# for file in aimlFilesList:
#     kernal.learn(file)

while True :

    string = input("HUMAN : ")                      #Take input from the user...

    if(string==""):
        break
    else:
        sentenceFromSemanticNetwork = makeSemanticNetwork(str(string))      #For Wh Family it give sentence from Neo4j

        if(sentenceFromSemanticNetwork == ""):
            print("ROBOT : Data Saved.")
            # chatbot = kernal.respond(string)
            # if chatbot == "":
            #     print("ROBOT : Thanks for you information...")
            # else:
            #     print("ROBOT : ",chatbot)
        else:
            print("ROBOT : ",sentenceFromSemanticNetwork)
