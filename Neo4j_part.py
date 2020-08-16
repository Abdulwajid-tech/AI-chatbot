from py2neo import *
from NLTK_part import *
from machineLearning_part import *
import socket

def storeIpAddressAndHostName():                #Store the user IP ADDRESS AND HOST NAME...

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "asdfgh"))            # Create Connection

    noOfIpAddressesStore  = graph.run("MATCH(n:IpAddress) RETURN count(n) as Count").to_data_frame().iloc[0]['Count']
    noOfHostNameStore   = graph.run("MATCH(n:HostName) RETURN count(n) as Count").to_data_frame().iloc[0]['Count']

    query1 = "MERGE(ip" + str(noOfIpAddressesStore) + ":IpAddress{ name:'"+str(IPAddr)+"'}) on CREATE SET ip"+str(noOfIpAddressesStore)+".name='" + str(IPAddr) + "'"
    query2 = "MERGE(host" + str(noOfHostNameStore) + ":HostName{ name:'" + hostname + "'}) on CREATE SET host" + str(noOfHostNameStore) + ".name='" + str(hostname) + "'"

    query = "MATCH (m:IpAddress{name:'"+str(IPAddr)+"'}) ,(n:HostName{name:' " + str(hostname) + "'}) MERGE (m)-[:HAS_THE_HOSTNAME]->(n)"
    graph.run(query1)
    graph.run(query2)
    graph.run(query)

def mergeHelpingverbs(stringList):          #If verbs are more than 1 then merge them using _
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

def removeUnderScore(string):
        string2 = ""
        for i in string:
            if i == "_":
                i = " "
            string2 = string2 + i

        return string2

def makeSemanticNetwork(sentence):

    string = ""
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "asdfgh"))            #Create Connection

    nouns, verbs , properties , whfamily= process_Data(sentence)

    if(len(whfamily)==0):

        noOfPersons = graph.run("MATCH(n:Person) RETURN count(n) as Count").to_data_frame().iloc[0]['Count']
        noOfAnimals = graph.run("MATCH(n:Animal) RETURN count(n) as Count").to_data_frame().iloc[0]['Count']
        noOfObjects = graph.run("MATCH(n:Object) RETURN count(n) as Count").to_data_frame().iloc[0]['Count']
        noOfPlaces  = graph.run("MATCH(n:Place) RETURN count(n) as Count").to_data_frame().iloc[0]['Count']

        listForRelationship = []

        if len(properties)!=0:
            if len(nouns) == 2:
                nouns[1] = properties[0] + " " + nouns[1]
                properties[0]=nouns[1]

            for nodes in nouns:

                type = MachineLearningAlgo(nodes)
                if (type == "Person"):

                    listForRelationship.append("Person")
                    createNode = "MERGE(p"+str(noOfPersons)+":Person{ name:'" + nodes + "'}) on CREATE SET p"+str(noOfPersons)+".name='" + nodes + "'"

                elif (type == "Place"):

                    listForRelationship.append("Place")
                    createNode = "MERGE(l" + str(noOfPlaces) + ":Place{ name:'" + nodes + "'}) on CREATE SET l"+str(noOfPlaces)+".name='" + nodes + "'"

                elif (type == "Animal"):

                    listForRelationship.append("Animal")
                    createNode = "MERGE(a" + str(noOfAnimals) + ":Animal{ name:'" + nodes + "'}) on CREATE SET a"+str(noOfAnimals)+".name='" + nodes + "'"

                elif(type == "Object"):

                    listForRelationship.append("Object")
                    createNode = "MERGE(o" + str(noOfObjects) + ":Object{ name:'" + nodes + "'}) on CREATE SET o" + str(noOfObjects) + ".name='" + nodes + "'"

                graph.run(createNode)

            for prop in properties:

                type = MachineLearningAlgo(prop)

                if (type == "Person"):

                    listForRelationship.append("Person")
                    createNodeProps = "MERGE(p"+str(noOfPersons)+":Person{ name:'" + prop + "'}) on CREATE SET p"+str(noOfPersons)+".name='" + prop + "'"

                elif (type == "Place"):

                    listForRelationship.append("Place")
                    createNodeProps = "MERGE(l" + str(noOfPlaces) + ":Place{ name:'" + prop + "'}) on CREATE SET l" + str(noOfPlaces) + ".name='" + prop + "'"

                elif (type == "Animal"):

                    listForRelationship.append("Animal")
                    createNodeProps = "MERGE(a" + str(noOfAnimals) + ":Animal{ name:'" + prop + "'}) on CREATE SET a" + str(noOfAnimals) + ".name='" + prop + "'"

                elif (type == "Object"):

                    listForRelationship.append("Object")
                    createNodeProps = "MERGE(o" + str(noOfObjects) + ":Object{ name:'" + prop + "'}) on CREATE SET o" + str(noOfObjects) + ".name='" + prop + "'"

                graph.run(createNodeProps)

            relation = mergeHelpingverbs(verbs)

            query="MATCH(m:"+listForRelationship[0]+"{name:'"+nouns[0]+"'}),(n:"+listForRelationship[1]+"{name:'"+properties[0]+"'}) MERGE (m)-[:"+relation+"]->(n)"

            graph.run(query)

        else:
            for nodes in nouns:

                type = MachineLearningAlgo(nodes)

                if (type == "Person"):

                    listForRelationship.append("Person")
                    createNode = "MERGE(p" + str(noOfPersons) + ":Person{ name:'" + nodes + "'}) on CREATE SET p"+str(noOfPersons)+".name='" + nodes + "'"

                elif (type == "Place"):

                    listForRelationship.append("Place")
                    createNode = "MERGE(l" + str(noOfPlaces) + ":Place{ name:'" + nodes + "'}) on CREATE SET l"+str(noOfPlaces)+".name='" + nodes + "'"

                elif (type == "Animal"):

                    listForRelationship.append("Animal")
                    createNode = "MERGE(a" + str(noOfAnimals) + ":Animal{ name:'" + nodes + "'}) on CREATE SET a"+str(noOfAnimals)+".name='" + nodes + "'"

                elif (type == "Object"):

                    listForRelationship.append("Object")
                    createNode = "MERGE(o" + str(noOfObjects) + ":Object{ name:'" + nodes + "'}) on CREATE SET o"+str(noOfObjects)+".name='" + nodes + "'"

                graph.run(createNode)

            rel=mergeHelpingverbs(verbs)

            query="MATCH(m:"+listForRelationship[0]+"{name:'"+nouns[0]+"'}),(n:"+listForRelationship[1]+"{name:'"+nouns[1]+"'}) MERGE(m)-[:"+rel+"]->(n)"

            graph.run(query)

    else:
        yesFind = None
        indexWhereRelationshipmatch = -1

        for noun in nouns:
            type = MachineLearningAlgo(noun)

            if(type == "Person"):

                query = "MATCH (n:Person {name :'"+noun+"'}) -[r]-(m) RETURN type(r) as relationship"
                a = graph.run(query).to_data_frame()

                for ind in a.index:
                    for verb in verbs:
                        relationship = str(a['relationship'][ind])
                        yesFind = relationship.find(str(verb).upper())
                        if(yesFind != -1):
                            indexWhereRelationshipmatch = ind
                            break
                    if (yesFind != -1):
                        break

                if indexWhereRelationshipmatch != -1 :

                    query = "MATCH (n:Person {name :'" + noun + "'}) -[r:"+str(a['relationship'][indexWhereRelationshipmatch]) +"]-(m) RETURN n['name'] as n ,type(r) as r ,m['name'] as m"
                    b = graph.run(query).to_data_frame()
                    relation = str(b['r'][0])

                    relation = relation.lower()
                    relation = removeUnderScore(relation)
                    string = str(b['n'][0]) + " "+ relation + " " +str(b['m'][0])

                elif indexWhereRelationshipmatch != -1:

                    string = ""

            elif (type == "Animal"):

                query = "MATCH (n:Animal {name :'"+noun +"'}) -[r]-(m) RETURN type(r) as relationship"
                a = graph.run(query).to_data_frame()

                for ind in a.index:
                    for verb in verbs:
                        relationship = str(a['relationship'][ind])
                        yesFind = relationship.find(str(verb).upper())
                        if (yesFind != -1):
                            indexWhereRelationshipmatch = ind
                            break
                    if (yesFind != -1):
                        break

                if indexWhereRelationshipmatch != -1:
                    query = "MATCH (n:Animal {name :'" + noun + "'}) -[r:" + str(a['relationship'][indexWhereRelationshipmatch]) + "]-(m) RETURN n['name'] as n ,type(r) as r ,m['name'] as m"
                    b = graph.run(query).to_data_frame()
                    relation = str(b['r'][0])
                    relation = relation.lower()
                    relation = removeUnderScore(relation)

                    string = str(b['n'][0]) + " " + relation + " " + str(b['m'][0])

                elif indexWhereRelationshipmatch != -1:
                    string = ""

            elif (type == "Object"):

                query = "MATCH (n:Object {name :'" + noun + "'}) -[r]-(m) RETURN type(r) as relationship"
                a = graph.run(query).to_data_frame()

                for ind in a.index:
                    for verb in verbs:
                        relationship = str(a['relationship'][ind])
                        yesFind = relationship.find(str(verb).upper())
                        if (yesFind != -1):
                            indexWhereRelationshipmatch = ind
                            break
                    if (yesFind != -1):
                        break

                if indexWhereRelationshipmatch != -1:
                    query = "MATCH (n:Object {name :'" + noun + "'}) -[r:" + str(a['relationship'][indexWhereRelationshipmatch]) + "]-(m) RETURN n['name'] as n ,type(r) as r ,m['name'] as m"
                    b = graph.run(query).to_data_frame()
                    relation = str(b['r'][0])
                    relation = relation.lower()
                    relation = removeUnderScore(relation)
                    string = str(b['n'][0]) + " " + relation + " " + str(b['m'][0])

                elif indexWhereRelationshipmatch != -1:
                    string = ""

            elif (type == "Place"):

                query = "MATCH (n:Place {name :'" + noun + "'}) -[r]-(m) RETURN type(r) as relationship"
                a = graph.run(query).to_data_frame()

                for ind in a.index:
                    for verb in verbs:
                        relationship = str(a['relationship'][ind])
                        yesFind = relationship.find(str(verb).upper())
                        if (yesFind != -1):
                            indexWhereRelationshipmatch = ind
                            break
                    if (yesFind != -1):
                        break

                if indexWhereRelationshipmatch != -1:
                    query = "MATCH (n:Place {name :'" + noun + "'}) -[r:" + str(a['relationship'][indexWhereRelationshipmatch]) + "]-(m) RETURN n['name'] as n ,type(r) as r ,m['name'] as m"
                    b = graph.run(query).to_data_frame()
                    relation = str(b['r'][0])
                    relation = relation.lower()
                    relation = removeUnderScore(relation)
                    string = str(b['n'][0]) + " " + relation + " " + str(b['m'][0])

                elif indexWhereRelationshipmatch != -1:
                    string = ""

    return string
