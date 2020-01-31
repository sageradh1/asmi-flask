from app import app,db
from flask import request,jsonify,make_response,redirect, render_template
import os
import urllib.request
from werkzeug.utils import secure_filename

from app.database.models import UploadedVideo,VideoAnalyticsFile,GeneratedVideo
from datetime import datetime

from app.utils.dataUtilsCode import uniqueClassSetAndDict,uniqueDictonairies,arrangeNnumberOfDictionary,returnList,writeListAsAJsonFile
from app.darkflowMerge.openCVTFNet import extractFrameInfosFromVideo,extractIndicesFromTuple,frameToVid


@app.route('/')
def empty():
    # u = User(username='susan', email='susan@example.com')
    # print(u)
    return 'yes'

@app.route('/database', methods=["GET", "POST"])
def database():
    # u = User(username='susan', email='susan@example.com')
    # print(u)
    return 'yes'

def isVideoNameAllowed(filename):
    # We only want files with a . in the filename
    if not "." in filename:
        return False
    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]
    # Check if the extension is in ALLOWED_VIDEO_EXTENSIONS
    if ext.lower() in app.config["ALLOWED_VIDEO_EXTENSIONS"]:
        return True
    else:
        return False

def isCSVNameAllowed(filename):
    # We only want files with a . in the filename
    if not "." in filename:
        return False
    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]
    # Check if the extension is in ALLOWED_USERDATA_EXTENSIONS
    if ext.lower() in app.config["ALLOWED_USERDATA_EXTENSIONS"]:
        return True
    else:
        return False

def isVideoFilesizeAllowed(videosize):
    if int(videosize) <= app.config["MAX_VIDEO_FILESIZE"]:
        return True
    else:
        return False

def isCSVFilesizeAllowed(csvsize):
    if int(csvsize) <= app.config["MAX_CSV_FILESIZE"]:
        return True
    else:
        return False


@app.route('/view_videos')
def view_videos():

    return render_template('jsonHTTPDockersALL/tylerindex.html')


@app.route('/upload', methods=["GET", "POST"])
def upload_files():
    
    if request.method == 'GET':

        message = "Please upload the video(<20MB size) and csv files(<10MB size)"
        print(message)
        return render_template('jsonHTTPDockersALL/upload.html',message=message)
    
    if request.method == 'POST':

        _videoUploadStartingTime=datetime.utcnow()
        startingdt_string = _videoUploadStartingTime.strftime("%Y%m%d%H%M%S")
        
        # check if the post request has the file part
        if not request.files:
            message ="No files received "
            print(message)
            return redirect(request.url)
        if ('videofile' not in request.files) or ('csvfile' not in request.files):
            message ="Missing files "
            print(message)
            return render_template("jsonHTTPDockersALL/upload.html",message=message)
		#file = request.files['file']
        videofile = request.files['videofile']
        csvfile = request.files['csvfile']

        if not isVideoNameAllowed(secure_filename(videofile.filename)):
            message="Please make sure video file is in valid format"
            print(message)
            return render_template("jsonHTTPDockersALL/upload.html",message=message)
        
        if not isCSVNameAllowed(secure_filename(csvfile.filename)):
            message="Please make sure CSV file is in valid format"
            print(message)
            return render_template("jsonHTTPDockersALL/upload.html",message=message)
        
        if ("videosize" not in request.cookies) or ("csvsize" not in request.cookies):
            message="Your browser is not supporting cookie functionality"
            print(message)
            return render_template("jsonHTTPDockersALL/upload.html",message=message)
        
        if not isVideoFilesizeAllowed(request.cookies["videosize"]):
            message="Videosize exceeded maximum limit"
            print(message)
            return render_template("jsonHTTPDockersALL/upload.html",message=message)
        
        if not isCSVFilesizeAllowed(request.cookies["csvsize"]):
            message="CSV filesize exceeded maximum limit"
            print(message)
            return render_template("jsonHTTPDockersALL/upload.html",message=message)

        _videostorageLocation = app.config["VIDEO_UPLOADS_FOLDER"]
        _videofilename= videofile.filename

        _basename=startingdt_string+_videofilename.split('.')[0]
        _extension=_videofilename.split('.')[1]

        print("Video Saving Started ....")
        videofile.save(os.path.join(app.config["VIDEO_UPLOADS_FOLDER"], startingdt_string+videofile.filename))
        csvfile.save(os.path.join(app.config["CSV_UPLOADS_FOLDER"], csvfile.filename))
        print("Video Saving Completed ....")
        
        _videoUploadCompletedTime=datetime.utcnow()
        
        _uploadedVideo=UploadedVideo(filename = _basename, extension = _extension,storagelocation = _videostorageLocation,uploadStartedTime = _videoUploadStartingTime,uploadCompletedTime = _videoUploadCompletedTime)

        db.session.add(_uploadedVideo)
        db.session.commit()

        listOfResultsWithTuple,listOfResultsWithoutTuple,originalFrameArray,newframeArray,fps=extractFrameInfosFromVideo(startingdt_string+videofile.filename)

        myUniqueClassSet,myClassDict = uniqueClassSetAndDict(listOfResultsWithoutTuple)
        print("\nmyUniqueClassSet")
        print(myUniqueClassSet)
        print("\nmyClassDict")
        print(myClassDict)
        confidenceDict,numberOfTimesEmergedDict,averageConfidenceDict = uniqueDictonairies(myUniqueClassSet,myClassDict,listOfResultsWithoutTuple)

        print("\n confidenceDict")
        print(confidenceDict)
        print("\n numberOfTimesEmergedDict")
        print(numberOfTimesEmergedDict)
        print("\n averageConfidenceDict")
        print(averageConfidenceDict)

        #x=int(input("Enter the number of classes with highest confidence : "))
        x=3
        newSortedClassDict,newSortedAvgConfidenceDictWithRequiredNumber = arrangeNnumberOfDictionary(x,myClassDict,averageConfidenceDict)

        print("See here if the dict is only length 3: ")
        print(newSortedClassDict)
        finalJsonArray = returnList(newSortedClassDict,listOfResultsWithTuple)

        _analyticsFileUploadTime=datetime.utcnow()
        analyticsstartingdt_string = _analyticsFileUploadTime.strftime("%Y%m%d%H%M%S")
        analyticsFileName = analyticsstartingdt_string+_videofilename.split('.')[0]+".json"
        writeListAsAJsonFile(finalJsonArray,analyticsFileName)

        generatedAnalyticsFile = VideoAnalyticsFile(filename=analyticsFileName,storagelocation=app.config["VIDEOANALYTICS_GENERATED_FOLDER"],createdTime = _analyticsFileUploadTime,videoFile=_uploadedVideo)
        db.session.add(generatedAnalyticsFile)
        db.session.commit()

        generatedVideoStartingTime=datetime.utcnow()
        gen_video_dt_string = generatedVideoStartingTime.strftime("%Y%m%d%H%M%S")
        generatedVideoFilename = gen_video_dt_string+"_generated_"+_videofilename.split('.')[0]

        indexOfRequiredFrame=extractIndicesFromTuple(listOfResultsWithTuple,newSortedClassDict)


        frameToVid(indexOfRequiredFrame,originalFrameArray,newframeArray,app.config['VIDEO_GENERATED_FOLDER']+"/"+generatedVideoFilename+".webm", fps)
        #frameToVid(listOfResultsWithTuple,newSortedClassDict,originalFrameArray,newframeArray,app.config['VIDEO_GENERATED_FOLDER']+"/"+generatedVideoFilename,fps)
        
        generatedVideo = GeneratedVideo(filename = generatedVideoFilename,storagelocation = app.config['VIDEO_GENERATED_FOLDER'],createdTime = generatedVideoStartingTime,video_id = _uploadedVideo.videoid)
        db.session.add(generatedVideo)
        db.session.commit()
    
    message = "Till now no error"
    print(message)
    return render_template("jsonHTTPDockersALL/upload.html",message=message)




@app.route("/json",methods=["POST"])
def json():
    if request.is_json:
        #Accessing JSON from request
        req = request.get_json()
        #Now req can be treated as python dictionary
        
        #Parsing value from key
        name = req.get("name")

        #making response dictionary
        res ={
            "key":"This is response",
            "Received name value":name
        }

        #Converting Dictionary into json
        jsonifiedResponse = jsonify(res)
        httpStatusCode = 200

        finalHttpResponse = make_response(jsonifiedResponse,httpStatusCode) 
        
        return finalHttpResponse
    else:
        return make_response("No JSON has been Received",400)









@app.route("/flaskappconfiguration")
def configuration():
    #To see configuration
    print("Before app config")
    print(app.config)
    #We can change values of already present keys and also we can create our own new key-value pair in app config dictionary
    app.config["MyOwnKey"]="My Own Value"
    print("After app config")
    print(app.config)
    
    return "This is a page for configuraiton of flask app.asdasd"
