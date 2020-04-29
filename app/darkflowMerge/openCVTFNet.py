from app import app
from app.utils.dataUtilsCode import uniqueClassSetAndDict,uniqueDictonairies,arrangeNnumberOfDictionary,returnList,writeListAsAJsonFile

import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
from datetime import datetime
import os
basedir = os.path.abspath(os.path.dirname(__file__))
# from PIL import Image

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
    "threshold": 0.6
    }

tfnet = TFNet(options)



def getThumbnailName(filename):
    # We only want files with a . in the filename
    return filename.split(".")[0]+".png"

def save_frame_as_image(imagelocation,imagefilename,originalFrame):
        print("Saving thumbnail ......")

        print("At location : {}   filename : {}     path : {}".format(
            imagelocation,
            imagefilename,
            os.path.join(imagelocation, imagefilename)
            ))
        cv2.imwrite(os.path.join(imagelocation, imagefilename) , originalFrame)

def extractFrameInfosFromVideo(_videoname,selected_option):

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
    frame_count = 100

    thumbnail_name = getThumbnailName("thumbnail_for_"+_videoname)


    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
     
     
    if int(major_ver)  < 3 :
        fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
    else :
        print("the version is : "+str(major_ver))
        fps = capture.get(cv2.CAP_PROP_FPS)
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    print("The video fps is : {:f}".format(fps))
    print("The video frame count is : {:d}".format(frame_count))
    duration = frame_count/ fps

    print('duration (S) = ' + str(duration))
    minutes = int(duration/60)
    seconds = int(duration%60)
    totalduration= str(minutes) + ':' + str(seconds)
    print('duration (M:S) = ' + totalduration)


    frame_index_for_thumbnail = int(frame_count/2)

    print("Thumbnail frame index "+str(frame_index_for_thumbnail))
    print("Processing each frame ..... ")
    
    while (capture.isOpened()):
        stime = time.time()
        ret, frame = capture.read()

        originalFrame = frame

        if ret:
            framecounter=framecounter+1

            if framecounter==frame_index_for_thumbnail:
                save_frame_as_image(app.config["THUMBNAIL_FOR_UPLOADED_VIDEO_FOLDER"],thumbnail_name,originalFrame)

            frame_msec = capture.get(cv2.CAP_PROP_POS_MSEC)
            print("Frame number : {:d} TimeStamp: {:f}".format(framecounter,frame_msec))
            #print("Frame No \t Objects Count \t Object Label \t Confidence ")        
            results = tfnet.return_predict(frame)
            print("Results : ",results)

            new_result = []
            for eachObject in results:
                # print("The selected option is {} and the detected object is {}".format(selected_option,eachObject['label']))

                if eachObject['label']==selected_option:
                    new_result.append(eachObject.copy())

            listOfResultsWithTuple.append((new_result,frame_msec))
            listOfResultsWithoutTuple.append(new_result)

            # if framecounter==30:
            #     thumb = image_to_thumbs(frame)
            #     # os.makedirs(app.config['THUMBNAIL_FOR_UPLOADED_VIDEO_FOLDER'])
            #     for k, v in thumb.items():
            #         print("In 30th frame , the value of k is {}".format(k))
            #         cv2.imwrite(app.config['THUMBNAIL_FOR_UPLOADED_VIDEO_FOLDER']+'/'+str(k)+'.png' , v)


            for eachObject in new_result:

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

                isRequiredObjectDetected = False

                if eachObject['label']=="bottle":
                    icon_img = cv2.imread(app.config["ADIMAGE_UPLOADS_FOLDER"] +"/cup.png")
                    isRequiredObjectDetected = True
                elif eachObject['label']=="dog":
                    icon_img = cv2.imread(app.config["ADIMAGE_UPLOADS_FOLDER"] +"/dogfood.png")
                    isRequiredObjectDetected = True
                elif eachObject['label']=="car":
                    icon_img = cv2.imread(app.config["ADIMAGE_UPLOADS_FOLDER"] +"/tesla.png")
                    isRequiredObjectDetected = True
                elif eachObject['label']=="sofa":
                    icon_img = cv2.imread(app.config["ADIMAGE_UPLOADS_FOLDER"] +"/furniture.png")
                    isRequiredObjectDetected = True
                elif eachObject['label']=="motorbike":
                    icon_img = cv2.imread(app.config["ADIMAGE_UPLOADS_FOLDER"] +"/suzuki.png")
                    isRequiredObjectDetected = True
                elif eachObject['label']=="person":
                    icon_img = cv2.imread(app.config["ADIMAGE_UPLOADS_FOLDER"] +"/amazon.png")
                    isRequiredObjectDetected = True
                elif eachObject['label']=="tie":
                    icon_img = cv2.imread(app.config["ADIMAGE_UPLOADS_FOLDER"] +"/suzuki.png")
                    isRequiredObjectDetected = True

                if isRequiredObjectDetected:
                    icon_img1= cv2.resize(icon_img, (iconWidth,iconHeight))
                    
                    # else:
                    #     icon_img = cv2.imread(app.config["ADIMAGE_UPLOADS_FOLDER"] +"/amazon.png")
                    #     icon_img1= cv2.resize(icon_img, (iconWidth,iconHeight))

                    # icon_img = cv2.imread(basedir +"/icon6.png")
                    # icon_img1= cv2.resize(icon_img, (iconWidth,iconHeight))

                    x_offset=br[0]-iconWidth
                    y_offset=int((tl[1]+br[1])/2)-iconHeight
                    frame[y_offset:y_offset+icon_img1.shape[0], x_offset:x_offset+icon_img1.shape[1]] = icon_img1

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
            return listOfResultsWithTuple,listOfResultsWithoutTuple,originalFrameArray,newframeArray,fps,totalduration,thumbnail_name

    print("Outside loop")
    return listOfResultsWithTuple,listOfResultsWithoutTuple,originalFrameArray,newframeArray,fps,totalduration,thumbnail_name

#extractFrameInfosFromVideo("20200118154330dogvideo.mp4")