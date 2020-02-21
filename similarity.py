import pandas as pd

#################################### For important Video ######################################

#Read database and add index column if necessary
view_history_raw_df = pd.read_csv("datasetasmi/userViewHistories.csv")
# view_history_raw_df.head()

#Generate new dataframe with WatchCount(watch_count)
unique_user_id_list =view_history_raw_df.user_id.unique()
unique_video_id_list =view_history_raw_df.watched_video_id.unique()

counter=0
allrowsList=[]
for eachvideoid in unique_video_id_list:
    for eachuserid in unique_user_id_list:
        #Check conditions
        rowsthatsatisfy = view_history_raw_df[(view_history_raw_df['watched_video_id']==eachvideoid) & (view_history_raw_df['user_id']==eachuserid)]
#         print(rowsthatsatisfy)
        count=len(rowsthatsatisfy)
#         print(count)
        if count==0:
            continue
        totalwatchtime=rowsthatsatisfy['watch_time_in_sec'].sum()
        rowdict={'user_id':eachuserid,'watched_video_id':eachvideoid,'watch_count':count,'total_watch_time':totalwatchtime}
        allrowsList.append(rowdict.copy())
featured_view_history = pd.DataFrame(allrowsList)
# featured_view_history.head()
# print(featured_view_history.shape)

#Normalise the data according to average
word_count_avg=featured_view_history['watch_count'].mean()
watch_time_avg=featured_view_history['total_watch_time'].mean()
# print("Average word count is : ",word_count_avg)
# print("Average watch time is : ",watch_time_avg)

currentindex=0
current_class_name=''
def avg_out_score(row):
    return row[current_class_name]/avgList_forcolumns[currentindex]

columnsToBeNormalised=['watch_count','total_watch_time']
avgList_forcolumns = [word_count_avg,watch_time_avg]

normalisedf=featured_view_history[['user_id','watched_video_id','total_watch_time']].copy()

# normaliseddf = pd.DataFrame(columns = None)
for eachclass in columnsToBeNormalised:
    current_class_name=eachclass
    currentindex=columnsToBeNormalised.index(eachclass)
    normalisedf['avg_'+eachclass]=featured_view_history.apply(avg_out_score,axis=1)

watch_time_importance = 0.7
watch_count_importance = 0.3

def calculate_video_importance(row):
    return row['avg_watch_count']*watch_count_importance*row['avg_total_watch_time']*watch_time_importance

normalisedf['video_importance']=normalisedf.apply(calculate_video_importance,axis=1)

# normalisedf = normalisedf.sort_values(by=['video_importance'], ascending=False)
# normalisedf.head()


##Find most important video
def findmostimportantvideo(user_id,dataframe=normalisedf,number_of_video=1):
    dataframe=dataframe[dataframe['user_id']==user_id]
    dataframe=dataframe.sort_values(by=['video_importance'], ascending=False)
    return dataframe.head(number_of_video)['watched_video_id'].values
#################################### End For important Video ######################################





#################################### Start similar video ##########################################
def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]


#Read database and add index column if necessary
asmidf = pd.read_csv("datasetasmi/uploadedVideosEdited.csv")
# asmidf.head()

classes = ["Shirt","Trousers","Footwear","Handbag","Watch","Guitar","Mobile_phone","Headphones","Hat","Sunglasses"]

#Generate a new dataframe with all the scores of detected objects
currentindex=0
def class_score(row):
    detectedobjectsstr=str(row['detected_objects_withconfidence'])
    detectedobjectswithScore=detectedobjectsstr.split("|")
    currentclass=classes[currentindex]
    
    for eachobjectwithScore in detectedobjectswithScore:
        if eachobjectwithScore.split(":")[0] in classes and eachobjectwithScore.split(":")[0]==currentclass:
            return int(int(eachobjectwithScore.split(":")[1]))

# newdf=asmidf[['video_id']].copy()
newdf = pd.DataFrame(columns = None)
for eachclass in classes:
    currentindex=classes.index(eachclass)
    newdf[eachclass]=asmidf.apply(class_score,axis=1)

newdf.head()



from sklearn.metrics import pairwise_distances
#Use Cosine, if data is sparse (many ratings are undefined)
# metric="cosine"

#Use Euclidean, if your data is not sparse and the magnitude of the attribute values is significant
metric="euclidean"

similarity_max = 1-pairwise_distances(newdf, metric=metric)
# pd.DataFrame(similarity_max)


# In[7]:


#This function finds k similar video given the video_id and ratings matrix M
#Note that the similarities are same as obtained via using pairwise_distances
k=3
from sklearn.neighbors import NearestNeighbors

def getvideoindexfromvideoid(video_id,matrixwithvideoid):
#     for j in range(len(feature_matrix)):
    for j in range(matrixwithvideoid.shape[0]):
        if matrixwithvideoid.iloc[j]['video_id'] == video_id:
            return j
    return -1

def getvideoidfromindex(index,matrixwithvideoid):
    if index<=matrixwithvideoid.shape[0]:
        return matrixwithvideoid.iloc[index]['video_id']
    else:
        return -1

def findksimilarvideo(video_id, feature_matrix=newdf,matrixwithvideoid=asmidf, metric = metric, k=k):
    similarities=[]
    indices=[]
    videoindex=getvideoindexfromvideoid(video_id,matrixwithvideoid)
    
    print("video_id: {}".format(video_id))
    print("videoindex: {}".format(videoindex))
    if videoindex==-1:
        print("Row with the video_id {} wasnot found.".format(video_id))
        return similarities,indices
    
    model_knn = NearestNeighbors(metric = metric, algorithm = 'brute') 
    model_knn.fit(feature_matrix)
    
    distances, indices = model_knn.kneighbors(feature_matrix.iloc[videoindex, :].values.reshape(1, -1), n_neighbors = k+1)
    similarities = 1-distances.flatten()
    print("Similarity coefficient : ",similarities)
    print("Index for similarity   : ",indices.flatten())
    
    print('{0} most similar videos for Video {1}:\n'.format(k,video_id))

    allvideoid=[]
    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i] == videoindex:
            continue;
        else:
            videoID=getvideoidfromindex(indices.flatten()[i],matrixwithvideoid) 
            allvideoid.append(videoID)
            print('video_index:{0} video_id:{1} with similarity of {2}'.format( indices.flatten()[i],videoID,similarities.flatten()[i]))
            
    return allvideoid


#################################### End similar video ##########################################
