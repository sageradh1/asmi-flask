from app import app
import pickle
import json
from app.database.models import MergedAdCategory
    
def get_intkey(_currentVal,_currentList): 
    for key, value in _currentList.items():
        if _currentVal == value:
            return key
    return -1 

classSet = set()
classDict= dict()
def uniqueClassSetAndDict(allFrameResult):
    for i in range(len(allFrameResult)):
        eachFrameData= allFrameResult[i]        
        detectedObjectCount = len(eachFrameData)

        for j in range(detectedObjectCount):
            eachDetectObjectData= eachFrameData[j]
            label = eachDetectObjectData['label']
            if label not in classSet:
                classDict[len(classSet)]=label
                classSet.add(label)                
    return classSet,classDict

confidenceDict = dict()
numberOfTimesEmergedDict = dict()
averageConfidenceDict= dict()
def uniqueDictonairies(_classSet,_classDict,_allFrameResult):
    for a in range(len(_classDict)):
        confidenceDict[a]=0
        numberOfTimesEmergedDict[a]=0
        averageConfidenceDict[a]=0

    for i in range(len(_allFrameResult)):

        eachFrameData= _allFrameResult[i]
        detectedObjectCount = len(eachFrameData)
        
        for j in range(detectedObjectCount):
            eachDetectObjectData= eachFrameData[j]
            label = eachDetectObjectData['label']
            confidence = eachDetectObjectData['confidence']
            indexInDict = get_intkey(label,_classDict)
            confidenceDict[indexInDict]=confidenceDict[indexInDict]+confidence
            numberOfTimesEmergedDict[indexInDict]=numberOfTimesEmergedDict[indexInDict]+1
        
    for a in range(len(_classDict)):
    #     averageConfidenceDict[a]=confidenceDict[a]/numberOfTimesEmergedDict[a]
        if numberOfTimesEmergedDict[a] ==0:
            averageConfidenceDict[a]=0
        else:
            averageConfidenceDict[a]=confidenceDict[a]/numberOfTimesEmergedDict[a]
    return confidenceDict,numberOfTimesEmergedDict,averageConfidenceDict

def sortDictInAscendingOrder(_myDict):
    return {k: v for k, v in sorted(_myDict.items(), key=lambda item: item[1])} 

def sortDictInDescendingOrder(_myDict):
    return {k: v for k, v in reversed(sorted(_myDict.items(), key=lambda item: item[1]))}

def arrangeNnumberOfDictionary(_number,_myDict,_averageConfidenceDict):
    # print("Before Sorting....")
    # print("Class Dictionary : ")
    # print(_myDict)
    # print("Average Confidence Dictionary : ")
    # print(_averageConfidenceDict)

    # print("\nAfter Sorting In Descending Order....")
    newSortedDictWithRequiredKey = sortDictInDescendingOrder(_averageConfidenceDict)
    # print("newSortedDictWithRequiredKey : ")
    # print(newSortedDictWithRequiredKey)

    counter=0
    newSortedAvgConfidenceDictWithRequiredNumber=dict()
    newSortedClassDict=dict()

    for a in newSortedDictWithRequiredKey.keys():
        #print("counter = {:d} and counter = {:d}".format(counter,_number))
        if counter == _number:
            break
        newSortedAvgConfidenceDictWithRequiredNumber[counter]=newSortedDictWithRequiredKey[a]
        newSortedClassDict[counter] = _myDict[a]
        counter = counter + 1
    
    print("newSortedDictWithRequiredNumber")
    print(newSortedAvgConfidenceDictWithRequiredNumber)

    print("newSortedClassDict")
    print(newSortedClassDict)

    return newSortedClassDict,newSortedAvgConfidenceDictWithRequiredNumber

    #returnJson(newSortedClassDict,newSortedAvgConfidenceDictWithRequiredNumber,_allResultsWithTupleList)
def getDetectedObjectsforDatabase(_myDict,_averageConfidenceDict):
    # print("Before Sorting....")
    # print("Class Dictionary : ")
    # print(_myDict)
    # print("Average Confidence Dictionary : ")
    # print(_averageConfidenceDict)

    # print("\nAfter Sorting In Descending Order....")
    newSortedDictWithRequiredKey = sortDictInDescendingOrder(_averageConfidenceDict)
    # print("newSortedDictWithRequiredKey : ")
    # print(newSortedDictWithRequiredKey)

    counter=0
    newSortedAvgConfidenceDictWithRequiredNumber=dict()
    newSortedClassDict=dict()

    for a in newSortedDictWithRequiredKey.keys():
        #print("counter = {:d} and counter = {:d}".format(counter,_number))
        # if counter == _number:
        #     break
        newSortedAvgConfidenceDictWithRequiredNumber[counter]=newSortedDictWithRequiredKey[a]
        newSortedClassDict[counter] = _myDict[a]
        counter = counter + 1

    outputstring=""
    for a in range(len(newSortedClassDict)):
        score = (len(newSortedClassDict)-a)/len(newSortedClassDict)
        outputstring+=newSortedClassDict[a]+":"+str(score)
        if a<(len(newSortedClassDict)-1):
            outputstring+="|"

    return outputstring

def returnList(_sortedClassDict,_allResultsWithTupleList):

    mainOutput = dict()
    
    mainOutput["dataForAds"]=returnDataForAds()

    mainOutput["dataPerObject"]=returnDataPerObject(_sortedClassDict,_allResultsWithTupleList)
 
    mainOutput["dataPerTimestamp"]=returnTimeStampsList(_sortedClassDict,_allResultsWithTupleList)

    print("\nmainOutput")
    print(mainOutput)
    return mainOutput


def returnDataPerObject(_sortedClassDict,_allResultsWithTupleList):
    finalJsonArray = []
    eachJsonObject = dict()

    counter=0

    for eachkey in range(len(_sortedClassDict)):
        eachJsonObject["Rank"]=eachkey
        eachJsonObject["Item"]=_sortedClassDict[eachkey]
        
        timeStampList =[]
        
        for currentTupleList in _allResultsWithTupleList:
            listofDetectedObject = currentTupleList[0]
            timeFrame= currentTupleList[1]

            for eachDetectedobject in listofDetectedObject:
                if eachJsonObject["Item"]==eachDetectedobject["label"]:
                    eachTimeStampObject=dict()
                    eachTimeStampObject["timeInMilliSec"]=timeFrame
                    eachTimeStampObject["x"]=(eachDetectedobject["topleft"]["x"]+eachDetectedobject["bottomright"]["x"])/2
                    eachTimeStampObject["y"]=(eachDetectedobject["topleft"]["y"]+eachDetectedobject["bottomright"]["y"])/2
                    
                    timeStampList.append(eachTimeStampObject)

        eachJsonObject["TimeStamp"]=timeStampList
        # print("EachObject in Array")
        # print(eachJsonObject)
        finalJsonArray.append(eachJsonObject.copy())
    # print("Final list length is {:d} may not be the accurate order".format(len(finalJsonArray)))
    # print(finalJsonArray)
    return finalJsonArray
    
def returnDataForAds():
    infoForAllLabelsList=[]

    try:
        mergedAd =  MergedAdCategory.query.filter(MergedAdCategory.id >= 11)

        for eachCategory in mergedAd:
            allinfoForThisCategory={}
          #   if mergedAd is None:
                # allinfoForThisCategory['ItemName']=eachCategory.category_name
                # allinfoForThisCategory['ImageUrl']="No information"
                # allinfoForThisCategory['IconUrl']="No information"
                # allinfoForThisCategory['Price']="No information"
          #   else:
            allinfoForThisCategory['ItemName']=str(eachCategory.category_name)            
            allinfoForThisCategory['ImageUrl']=str(app.config["BASE_URL_WITH_PORT"]+str("/static/img/ad-images/")+str(eachCategory.image_filename))
            allinfoForThisCategory['IconUrl']=str(app.config["BASE_URL_WITH_PORT"]+str("/static/img/ad-images/")+str(eachCategory.image_filename))
            allinfoForThisCategory['Price']=str(eachCategory.adprice)

            infoForAllLabelsList.append(allinfoForThisCategory.copy())
            
    except Exception as err:
        print("Problem while extracting information from Merged Ad Category Table")
        print(err)

    return infoForAllLabelsList

def returnTimeStampsList(_sortedClassDict,_allResultsWithTupleList):

    # print("For reference: ")
    # print(_allResultsWithTupleList[0])

    allDataInSimplerFormArray=[]
    uniqueTimeStamps=[]
    uniqueLabels=[]
    for index in range(len(_allResultsWithTupleList)):
        allDataObject=dict()

        eachresult=_allResultsWithTupleList[index]
        objectsInThatFrameList=eachresult[0]

        allDataObject["TimeinMilliSec"]=eachresult[1]

        #Unique TimeStamps
        if eachresult[1] not in uniqueTimeStamps:
            uniqueTimeStamps.append(eachresult[1])


        for eachObject in objectsInThatFrameList:
            allDataObject["Label"]=eachObject["label"]
            if eachObject["label"] not in uniqueLabels:
                uniqueLabels.append(eachObject["label"])

            allDataObject["x"]=(eachObject["topleft"]["x"]+eachObject["bottomright"]["x"])/2
            allDataObject["y"]=(eachObject["topleft"]["y"]+eachObject["bottomright"]["y"])/2
            allDataInSimplerFormArray.append(allDataObject.copy())
    # print("\nuniqueTimeStamps")
    # print(uniqueTimeStamps)

    # print("\nuniqueLabels")
    # print(uniqueLabels)

    # print("\nallDataInSimplerFormArray")
    # print(allDataInSimplerFormArray)

    # print("\n_sortedClassDict")
    # print(_sortedClassDict.values())

    #This line makes the code search for only those labels inside the _sortedClassDict
    #If this line is removed ,all labels will be searched
    uniqueLabels=list(_sortedClassDict.values())

######################Use SimplerDataForm##############################
    finalTimeJsonArray = []
    eachTimeJsonObject = dict()

    for index in range(len(uniqueTimeStamps)):
        eachTimeJsonObject["timeInMilliSec"]=uniqueTimeStamps[index]

        objectsWithCoordinates=[]

        for index1 in range(len(uniqueLabels)):
            currentLabel=uniqueLabels[index1]
            eachObjectWithCoordinate=dict()

            allCoordinates=[]

            for index2 in range(len(allDataInSimplerFormArray)):
                simplerDataObject=allDataInSimplerFormArray[index2]

                if(simplerDataObject["Label"]==currentLabel and simplerDataObject["TimeinMilliSec"]==uniqueTimeStamps[index]):
                    eachObjectWithCoordinate["label"]=currentLabel

                    eachXYObject=dict()

                    eachXYObject["x"]=simplerDataObject["x"]
                    eachXYObject["y"]=simplerDataObject["y"]
                    allCoordinates.append(eachXYObject.copy())


                    eachObjectWithCoordinate["allCoordinates"]=allCoordinates


            if (eachObjectWithCoordinate):
                objectsWithCoordinates.append(eachObjectWithCoordinate)




        eachTimeJsonObject["objectsWithCoordinates"]=objectsWithCoordinates
        finalTimeJsonArray.append(eachTimeJsonObject.copy())
    print("\nfinalTimeJsonArray")
    print(finalTimeJsonArray)

    return finalTimeJsonArray


# listOfResultsWithTuple = [([{'label': 'chair', 'confidence': 0.141772, 'topleft': {'x': 4, 'y': 21}, 'bottomright': {'x': 197, 'y': 339}}, {'label': 'diningtable', 'confidence': 0.29719263, 'topleft': {'x': 558, 'y': 238}, 'bottomright': {'x': 716, 'y': 379}}, {'label': 'tvmonitor', 'confidence': 0.2524646, 'topleft': {'x': 401, 'y': 42}, 'bottomright': {'x': 697, 'y': 399}}, {'label': 'microwave', 'confidence': 0.20507553, 'topleft': {'x': 43, 'y': 333}, 'bottomright': {'x': 540, 'y': 404}}, {'label': 'tvmonitor', 'confidence': 0.36070397, 'topleft': {'x': 91, 'y': 330}, 'bottomright': {'x': 544, 'y': 404}}], 0.0), ([{'label': 'diningtable', 'confidence': 0.121414885, 'topleft': {'x': 561, 'y': 239}, 'bottomright': {'x': 714, 'y': 373}}, {'label': 'tvmonitor', 'confidence': 0.10568733, 'topleft': {'x': 28, 'y': 17}, 'bottomright': {'x': 306, 'y': 250}}, {'label': 'tvmonitor', 'confidence': 0.3991819, 'topleft': {'x': 404, 'y': 24}, 'bottomright': {'x': 692, 'y': 404}}, {'label': 'tvmonitor', 'confidence': 0.432798, 'topleft': {'x': 92, 'y': 327}, 'bottomright': {'x': 541, 'y': 403}}, {'label': 'microwave', 'confidence': 0.3703576, 'topleft': {'x': 76, 'y': 318}, 'bottomright': {'x': 554, 'y': 401}}], 100.0), ([{'label': 'chair', 'confidence': 0.15903777, 'topleft': {'x': 2, 'y': 219}, 'bottomright': {'x': 104, 'y': 394}}, {'label': 'chair', 'confidence': 0.18745604, 'topleft': {'x': 13, 'y': 225}, 'bottomright': {'x': 259, 'y': 398}}, {'label': 'diningtable', 'confidence': 0.16162585, 'topleft': {'x': 560, 'y': 235}, 'bottomright': {'x': 713, 'y': 380}}, {'label': 'tvmonitor', 'confidence': 0.13487224, 'topleft': {'x': 30, 'y': 9}, 'bottomright': {'x': 316, 'y': 227}}, {'label': 'tvmonitor', 'confidence': 0.10557344, 'topleft': {'x': 528, 'y': 38}, 'bottomright': {'x': 719, 'y': 404}}, {'label': 'tvmonitor', 'confidence': 0.47824207, 'topleft': {'x': 112, 'y': 328}, 'bottomright': {'x': 529, 'y': 401}}, {'label': 'microwave', 'confidence': 0.41216028, 'topleft': {'x': 32, 'y': 291}, 'bottomright': {'x': 550, 'y': 404}}], 200.0), ([{'label': 'chair', 'confidence': 0.20980461, 'topleft': {'x': 1, 'y': 224}, 'bottomright': {'x': 56, 'y': 388}}, {'label': 'chair', 'confidence': 0.10808728, 'topleft': {'x': 5, 'y': 215}, 'bottomright': {'x': 265, 'y': 403}}, {'label': 'diningtable', 'confidence': 0.12779975, 'topleft': {'x': 565, 'y': 212}, 'bottomright': {'x': 713, 'y': 354}}, {'label': 'tvmonitor', 'confidence': 0.115053035, 'topleft': {'x': 27, 'y': 16}, 'bottomright': {'x': 313, 'y': 216}}, {'label': 'tvmonitor', 'confidence': 0.116568, 'topleft': {'x': 453, 'y': 40}, 'bottomright': {'x': 714, 'y': 358}}, {'label': 'tvmonitor', 'confidence': 0.30774802, 'topleft': {'x': 61, 'y': 310}, 'bottomright': {'x': 523, 'y': 403}}, {'label': 'laptop', 'confidence': 0.12993729, 'topleft': {'x': 107, 'y': 307}, 'bottomright': {'x': 530, 'y': 403}}, {'label': 'microwave', 'confidence': 0.36867908, 'topleft': {'x': 82, 'y': 292}, 'bottomright': {'x': 549, 'y': 404}}], 300.0), ([{'label': 'bird', 'confidence': 0.19501163, 'topleft': {'x': 330, 'y': 368}, 'bottomright': {'x': 378, 'y': 404}}, {'label': 'cat', 'confidence': 0.10808395, 'topleft': {'x': 198, 'y': 376}, 'bottomright': {'x': 289, 'y': 404}}, {'label': 'chair', 'confidence': 0.110156655, 'topleft': {'x': 273, 'y': 125}, 'bottomright': {'x': 440, 'y': 273}}, {'label': 'chair', 'confidence': 0.12092763, 'topleft': {'x': 5, 'y': 180}, 'bottomright': {'x': 269, 'y': 400}}, {'label': 'tvmonitor', 'confidence': 0.16968393, 'topleft': {'x': 405, 'y': 19}, 'bottomright': {'x': 695, 'y': 301}}, {'label': 'tvmonitor', 'confidence': 0.16052675, 'topleft': {'x': 562, 'y': 195}, 'bottomright': {'x': 718, 'y': 331}}, {'label': 'tvmonitor', 'confidence': 0.7032519, 'topleft': {'x': 2, 'y': 294}, 'bottomright': {'x': 575, 'y': 399}}, {'label': 'laptop', 'confidence': 0.10222144, 'topleft': {'x': 103, 'y': 263}, 'bottomright': {'x': 604, 'y': 404}}], 400.0), ([{'label': 'cat', 'confidence': 0.35772175, 'topleft': {'x': 174, 'y': 346}, 'bottomright': {'x': 393, 'y': 402}}, {'label': 'bird', 'confidence': 0.1658162, 'topleft': {'x': 328, 'y': 349}, 'bottomright': {'x': 382, 'y': 403}}, {'label': 'chair', 'confidence': 0.12223534, 'topleft': {'x': 657, 'y': 288}, 'bottomright': {'x': 718, 'y': 403}}, {'label': 'tvmonitor', 'confidence': 0.2144852, 'topleft': {'x': 405, 'y': 28}, 'bottomright': {'x': 692, 'y': 290}}, {'label': 'tvmonitor', 'confidence': 0.64373803, 'topleft': {'x': 17, 'y': 267}, 'bottomright': {'x': 559, 'y': 404}}], 500.0), ([{'label': 'person', 'confidence': 0.10750235, 'topleft': {'x': 1, 'y': 333}, 'bottomright': {'x': 44, 'y': 404}}, {'label': 'cat', 'confidence': 0.31962994, 'topleft': {'x': 174, 'y': 336}, 'bottomright': {'x': 382, 'y': 401}}, {'label': 'chair', 'confidence': 0.13275713, 'topleft': {'x': 2, 'y': 175}, 'bottomright': {'x': 55, 'y': 359}}, {'label': 'tvmonitor', 'confidence': 0.1755416, 'topleft': {'x': 409, 'y': 19}, 'bottomright': {'x': 690, 'y': 257}}, {'label': 'tvmonitor', 'confidence': 0.6187084, 'topleft': {'x': 12, 'y': 264}, 'bottomright': {'x': 564, 'y': 404}}, {'label': 'laptop', 'confidence': 0.14482969, 'topleft': {'x': 129, 'y': 253}, 'bottomright': {'x': 664, 'y': 404}}], 600.0), ([{'label': 'cat', 'confidence': 0.47887805, 'topleft': {'x': 162, 'y': 311}, 'bottomright': {'x': 403, 'y': 403}}, {'label': 'chair', 'confidence': 0.10665593, 'topleft': {'x': 61, 'y': 175}, 'bottomright': {'x': 276, 'y': 236}}, {'label': 'chair', 'confidence': 0.3392219, 'topleft': {'x': 657, 'y': 257}, 'bottomright': {'x': 718, 'y': 401}}, {'label': 'tvmonitor', 'confidence': 0.2952641, 'topleft': {'x': 410, 'y': 29}, 'bottomright': {'x': 686, 'y': 240}}, {'label': 'tvmonitor', 'confidence': 0.6430622, 'topleft': {'x': 42, 'y': 250}, 'bottomright': {'x': 527, 'y': 404}}], 700.0000000000001), ([{'label': 'cat', 'confidence': 0.7067051, 'topleft': {'x': 170, 'y': 303}, 'bottomright': {'x': 395, 'y': 399}}, {'label': 'chair', 'confidence': 0.1010209, 'topleft': {'x': 664, 'y': 245}, 'bottomright': {'x': 717, 'y': 403}}, {'label': 'tvmonitor', 'confidence': 0.1069465, 'topleft': {'x': 34, 'y': 8}, 'bottomright': {'x': 314, 'y': 182}}, {'label': 'tvmonitor', 'confidence': 0.44680485, 'topleft': {'x': 65, 'y': 239}, 'bottomright': {'x': 499, 'y': 404}}], 800.0), ([{'label': 'person', 'confidence': 0.1470381, 'topleft': {'x': 0, 'y': 85}, 'bottomright': {'x': 273, 'y': 360}}, {'label': 'person', 'confidence': 0.20587572, 'topleft': {'x': 0, 'y': 303}, 'bottomright': {'x': 41, 'y': 400}}, {'label': 'cat', 'confidence': 0.6494799, 'topleft': {'x': 183, 'y': 285}, 'bottomright': {'x': 368, 'y': 404}}, {'label': 'chair', 'confidence': 0.13149841, 'topleft': {'x': 661, 'y': 226}, 'bottomright': {'x': 719, 'y': 393}}, {'label': 'tvmonitor', 'confidence': 0.20233664, 'topleft': {'x': 408, 'y': 18}, 'bottomright': {'x': 686, 'y': 213}}, {'label': 'tvmonitor', 'confidence': 0.6835653, 'topleft': {'x': 57, 'y': 209}, 'bottomright': {'x': 580, 'y': 404}}], 900.0), ([{'label': 'person', 'confidence': 0.14286262, 'topleft': {'x': 6, 'y': 1}, 'bottomright': {'x': 59, 'y': 56}}, {'label': 'person', 'confidence': 0.27864012, 'topleft': {'x': 0, 'y': 302}, 'bottomright': {'x': 42, 'y': 402}}, {'label': 'cat', 'confidence': 0.6392344, 'topleft': {'x': 180, 'y': 276}, 'bottomright': {'x': 374, 'y': 404}}, {'label': 'chair', 'confidence': 0.120299965, 'topleft': {'x': 14, 'y': 0}, 'bottomright': {'x': 562, 'y': 366}}, {'label': 'chair', 'confidence': 0.12723537, 'topleft': {'x': 665, 'y': 207}, 'bottomright': {'x': 719, 'y': 404}}, {'label': 'tvmonitor', 'confidence': 0.30947506, 'topleft': {'x': 403, 'y': 24}, 'bottomright': {'x': 697, 'y': 203}}, {'label': 'tvmonitor', 'confidence': 0.6165459, 'topleft': {'x': 81, 'y': 202}, 'bottomright': {'x': 560, 'y': 404}}], 1000.0), ([{'label': 'chair', 'confidence': 0.141772, 'topleft': {'x': 4, 'y': 21}, 'bottomright': {'x': 197, 'y': 339}}, {'label': 'diningtable', 'confidence': 0.29719263, 'topleft': {'x': 558, 'y': 238}, 'bottomright': {'x': 716, 'y': 379}}, {'label': 'tvmonitor', 'confidence': 0.2524646, 'topleft': {'x': 401, 'y': 42}, 'bottomright': {'x': 697, 'y': 399}}, {'label': 'microwave', 'confidence': 0.20507553, 'topleft': {'x': 43, 'y': 333}, 'bottomright': {'x': 540, 'y': 404}}, {'label': 'tvmonitor', 'confidence': 0.36070397, 'topleft': {'x': 91, 'y': 330}, 'bottomright': {'x': 544, 'y': 404}}], 1100.0)]
# newSortedClassDict={0: 'cat', 1: 'tvmonitor', 2: 'microwave'}
# returnList(newSortedClassDict,listOfResultsWithTuple)



    
def writeListAsAJsonFile(_mylist,_filename):
    print("Creating json file ")
    #print(finalList)
    data = _mylist
    # Writing a JSON file
    with open(app.config["VIDEOANALYTICS_GENERATED_FOLDER"]+"/"+_filename, 'w') as f:
        print("Saving data as json : ")
        json.dump(data, f)

    f.close()
    # Reading a JSON file
    # with open(app.config["VIDEOANALYTICS_GENERATED_FOLDER"]+"/"+_filename, 'r') as f:
    #     # print("Extracting data from file")
    #     data = json.load(f)
    # print(data)





def dynamicJsonFile(_filename,requiredObjectLabels):
    #Extract all the required informations such as image urls, prices, etc from MergedAdCategory
    infoForAllLabelsList=[]
    for j in range(len(requiredObjectLabels)):
        try:
            mergedAd =  MergedAdCategory.query.filter_by(category_name=requiredObjectLabels[j]).first()
            allinfoForThisCategory={}
            if mergedAd is None:
                allinfoForThisCategory['category_name']=requiredObjectLabels[j]
                allinfoForThisCategory['adimage_url']="No information"
                allinfoForThisCategory['price']="No information"
            else:
                allinfoForThisCategory['category_name']=requiredObjectLabels[j]
                allinfoForThisCategory['adimage_url']=str(mergedAd.adimage_url)
                allinfoForThisCategory['price']=str(mergedAd.adprice)

            infoForAllLabelsList.append(allinfoForThisCategory.copy())
        except Exception as err:
            print("Problem while extracting information from Merged Ad Category Table")
            print(err)

    # print(infoForAllLabelsList)

    with open(app.config["VIDEOANALYTICS_GENERATED_FOLDER"]+"/"+_filename, 'r') as f:
        # print("Extracting data from file")
        data = json.load(f)
    f.close()

    olddataPerTimestamp = data['dataPerTimestamp']
    newdataPerTimestamp = []

    for i in range(len(olddataPerTimestamp)):

        eachdict_For_newdataPerTimestamp = {}   
        eachdict_For_newdataPerTimestamp['timeInMilliSec']=olddataPerTimestamp[i]['timeInMilliSec']
        
        allobjects = olddataPerTimestamp[i]['objectsWithCoordinates']
        eachdict_For_newdataPerTimestamp['objectsWithCoordinates']=[]
        for a in range(len(allobjects)):
            currentobjectwithcoordinate = allobjects[a]
            if currentobjectwithcoordinate["label"] in requiredObjectLabels:
                currentobjectwithcoordinate['adimage_url']=infoForAllLabelsList[requiredObjectLabels.index(currentobjectwithcoordinate["label"])]['adimage_url']
                currentobjectwithcoordinate['price']=infoForAllLabelsList[requiredObjectLabels.index(currentobjectwithcoordinate["label"])]['price']

                eachdict_For_newdataPerTimestamp['objectsWithCoordinates'].append(currentobjectwithcoordinate.copy())

        newdataPerTimestamp.append(eachdict_For_newdataPerTimestamp.copy())

    # print(newdataPerTimestamp)
    return newdataPerTimestamp