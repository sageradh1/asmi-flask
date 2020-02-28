from app import app
from app.utils.dataUtilsCode import uniqueClassSetAndDict,uniqueDictonairies,arrangeNnumberOfDictionary,returnList,writeListAsAJsonFile

import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
from datetime import datetime
import os
basedir = os.path.abspath(os.path.dirname(__file__))



# converting array of frames into Video
indexOfRequiredFrame=set()

def extractIndicesFromTuple(listOfResultsWithTuple,newSortedClassDict):
    frameCount = 0 
    for currentTupleList in listOfResultsWithTuple:
        listofDetectedObject = currentTupleList[0]
        timeFrame= currentTupleList[1]

        for eachDetectedobject in listofDetectedObject:
            if eachDetectedobject["label"] in newSortedClassDict.values():
                indexOfRequiredFrame.add(frameCount)
           
        frameCount=frameCount+1
    return indexOfRequiredFrame


# converting array of frames into Video
def frameToVid(indexOfRequiredFrame,originalFrameArray,newframeArray,vOutPath, fps):
    height, width, layer = newframeArray[0].shape

    # vOut = cv2.VideoWriter(
    #     vOutPath, 0x7634706d, fps, (width, height))

    # vOut = cv2.VideoWriter(
    #     vOutPath, cv2.VideoWriter_fourcc(
    #         * 'mp4v'), fps, (width, height))

    fourcc = cv2.VideoWriter_fourcc(*'vp80')

    #fourcc = cv2.VideoWriter_fourcc(*'H264')

    vOut = cv2.VideoWriter(
        vOutPath, fourcc, fps, (width, height))

    for index in range(len(originalFrameArray)):
        frame = originalFrameArray[index]
        
        if index in indexOfRequiredFrame:
            frame = newframeArray[index]
        vOut.write(frame)
    vOut.release()



options = {
    "model": basedir+"/cfg/yolo.cfg", 
    "load": basedir+"/bin/yolov2.weights", 
    "threshold": 0.1
    }

tfnet = TFNet(options)
def extractFrameInfosFromVideo(_videoname):

    capture = cv2.VideoCapture(app.config["VIDEO_UPLOADS_FOLDER"]+"/"+_videoname)

 #   capture = cv2.VideoCapture(_videoname)
 
    colors = [tuple(255 * np.random.rand(3)) for i in range(5)]

    framecounter =0

    listOfResultsWithTuple = []
    listOfResultsWithoutTuple = []

    classSet = set()
    classDict= dict()
    confidenceDict = dict()
    numberOfTimesEmergedDict = dict()
    averageConfidenceDict= dict()
    FrameDict = dict()
    originalFrameArray=[]
    newframeArray=[]
    generatedVideoFilename=''
    generatedVideoStartingTime=datetime.utcnow()
    fps = 20

    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
     
     
    if int(major_ver)  < 3 :
        fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
    else :
        fps = capture.get(cv2.CAP_PROP_FPS)

    print("The video fps is : {:f}".format(fps))
    print("Processing each frame ..... ")

    while (capture.isOpened()):
        stime = time.time()
        ret, frame = capture.read()

        originalFrame = frame

        if ret:
            framecounter=framecounter+1
            frame_msec = capture.get(cv2.CAP_PROP_POS_MSEC)
            print("Frame number : {:d} TimeStamp: {:f}".format(framecounter,frame_msec))
            #print("Frame No \t Objects Count \t Object Label \t Confidence ")        
            results = tfnet.return_predict(frame)
            # print("Results : ",results)
            listOfResultsWithTuple.append((results,frame_msec))
            listOfResultsWithoutTuple.append(results)
            #print(results)

            for eachObject in results:

                tl = (eachObject['topleft']['x'],eachObject['topleft']['y'])
                br = (eachObject['bottomright']['x'],eachObject['bottomright']['y'])

                rectFrameWidth = br[0]-tl[0]
                rectFrameHeight = br[1]-tl[1]

                iconWidth = int (0.2*rectFrameWidth)
                iconHeight = int (0.2*rectFrameHeight)


                # iconWidth = 40
                # iconHeight = 40

                if iconWidth==0 or iconHeight==0:
                    continue
                icon_img = cv2.imread(basedir +"/icon6.png")
                icon_img1= cv2.resize(icon_img, (iconWidth,iconHeight))
                
                x_offset=br[0]-iconWidth
                y_offset=int((tl[1]+br[1])/2)-iconHeight
                frame[y_offset:y_offset+icon_img1.shape[0], x_offset:x_offset+icon_img1.shape[1]] = icon_img1
                
                #frame = cv2.putText(frame, "", tl, cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), 0)
                #frame = cv2.rectangle(frame, tl, br, (255, 255, 255),2)
            newframeArray.append(frame)
            originalFrameArray.append(originalFrame)            
            # frame = cv2.rectangle(frame, tl, br, color, 7)
            # frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
            #cv2.imshow('frame', frame)
            
        else:
            capture.release()
            cv2.destroyAllWindows()
            print("listOfResultsWithTuple")
            print(listOfResultsWithTuple)
            print("\nlistOfResultsWithoutTuple")
            print(listOfResultsWithoutTuple)


            #frameToVid(originalFrameArray,newframeArray,app.config['VIDEO_GENERATED_FOLDER']+"/"+generatedVideoFilename,fps)
            return listOfResultsWithTuple,listOfResultsWithoutTuple,originalFrameArray,newframeArray,fps
    print("Outside loop")
    return listOfResultsWithTuple,listOfResultsWithoutTuple,originalFrameArray,newframeArray,fps

#extractFrameInfosFromVideo("20200118154330dogvideo.mp4")