from app import app,db
from flask import request,jsonify,make_response,redirect, render_template

from sklearn.neighbors import NearestNeighbors
from loadpandasdf import findmostimportantvideo,findksimilarvideo


def get_appropriate_adids(current_user_id,current_beingwatched_video_id):

############################################# Integrating #####################################################
	current_user_id=current_user_id
	current_beingwatched_video_id=current_beingwatched_video_id



###############################################################################################################	
	number_of_history_based_imp_videoid = 1

	print("Calculating most significant videos for the user.....")
	# find important videos according to who the user is and his views history 
	requiredVideoIDList = findmostimportantvideo(current_user_id,app.config['USERVIEWNORMALISEDDF'],number_of_video=number_of_history_based_imp_videoid)
	print("Most significance videoid according to userhistory : ",requiredVideoIDList)


	# In[15]:


	# Make a list of similar videos including important videos

	similar_videos_list=[]
	number_of_similar_videos=1

	for i in range(len(requiredVideoIDList)):
	    current_video_id = requiredVideoIDList[i]
	    similar_videos_list.append(current_video_id)
	    allvideoIds = findksimilarvideo(current_video_id,app.config['VIDEO_WITH_FEATURES_DF'],app.config['MATRIX_WITH_VIDEOID'], metric='euclidean',k=number_of_similar_videos)
	    for j in range(len(allvideoIds)):
	        similar_videos_list.append(allvideoIds[j])

	# If I had to recommend new video...I would recommend these without appending current_video_id as they had been already watched
	print("Similar videos to most significance videoid are : ",similar_videos_list)


	# In[16]:


	#### Extract important features from the videoid
	## First use already available app.config['VIDEO_WITH_FEATURES_DF'] for 'FEATURES' and app.config['MATRIX_WITH_VIDEOID'] for "VIDEO_ID" to make matrix_with_bothFeatureAndVideoId

	matrix_with_bothFeatureAndVideoId = app.config['VIDEO_WITH_FEATURES_DF'].copy()
	matrix_with_bothFeatureAndVideoId['video_id']= app.config['MATRIX_WITH_VIDEOID']['video_id']
	matrix_with_bothFeatureAndVideoId.head()



	# In[17]:



	# matrix_with_bothFeatureAndVideoId=matrix_with_bothFeatureAndVideoId[matrix_with_bothFeatureAndVideoId['video_id'] in similar_videos_list]
	filtered_df = matrix_with_bothFeatureAndVideoId.loc[matrix_with_bothFeatureAndVideoId['video_id'].isin(similar_videos_list)]
	filtered_df.head()


	# In[18]:


	listoffeatures = filtered_df.columns.tolist()
	listoffeatures.remove('video_id')


	# In[19]:


	##### MAIN SCORES TUPLE FROM USER HISTORY
	features_withscores_from_userhistory = []

	def make_required_tuple_from_df(listoffeatures,df=filtered_df):
	    features_withscores=[]
	    for i in range(len(listoffeatures)):
	        currentfeature = listoffeatures[i]
	        currentfeaturescore = df[currentfeature].mean()
	        features_withscores.append((currentfeature,currentfeaturescore))
	    return features_withscores

	    


	# In[20]:


	features_withscores_from_userhistory=make_required_tuple_from_df(listoffeatures,df=filtered_df)
	# print(features_withscores_from_userhistory)


	# In[21]:


	######## LETS START EXTRACTING AVAILABLE FEATURE FROM CURRENT VIDEO THAT USER IS WATCHING

	filtered_df = matrix_with_bothFeatureAndVideoId.loc[matrix_with_bothFeatureAndVideoId['video_id']==current_beingwatched_video_id]

	listoffeatures = filtered_df.columns.tolist()
	listoffeatures.remove('video_id')
	# listoffeatures


	# In[22]:

	print("Calculating scores for the confidence in the current video ......")
	## Make tuple as above:
	features_withscores_from_videocontent =make_required_tuple_from_df(listoffeatures,df=filtered_df)
	# print(features_withscores_from_videocontent)


	# In[23]:


	### Till now
	# From userhistory,  we got  features_withscores_from_userhistory
	# From videocontent, we got  features_withscores_from_videocontent

	significance_of_userhistory  = 0.6
	significance_of_videocontent = 0.4

	def getindexfromTupleListbasedonfeature(featurename,tuplename):
	#     for j in range(len(feature_matrix)):
	    for j in range(len(tuplename)):
	        if tuplename[j][0] == featurename:
	            return j
	    return -1

	avgout_feature_score=[]
	for i in range(len(listoffeatures)):
	    currentfeature = listoffeatures[i]
	    valuefrom_userhistory = features_withscores_from_userhistory[getindexfromTupleListbasedonfeature(currentfeature,features_withscores_from_userhistory)][1]
	    valuefrom_videocontent = features_withscores_from_videocontent[getindexfromTupleListbasedonfeature(currentfeature,features_withscores_from_videocontent)][1]
	    average = valuefrom_userhistory * significance_of_userhistory + valuefrom_videocontent * significance_of_videocontent
	    avgout_feature_score.append((currentfeature,average))

	# print(avgout_feature_score)

	sorted_avgout_feature_score = sorted(avgout_feature_score, key=lambda k: k[1],reverse=True)
	# print("Average sorted_avgout_feature_score: ")
	# print(sorted_avgout_feature_score)

	# In[25]:


	## Function that gets top scoring ads

	def getNamesofTopScoringAdsFromTupleOfAverage(numberofads,avg_tuple):
	    adnames = []
	    for i in range(numberofads):
	        adnames.append(avg_tuple[i][0])
	    return adnames
	    
	print("Calculating the most suitable ads ......")
	numberofadstobeshown = 2
	nameofads = getNamesofTopScoringAdsFromTupleOfAverage(numberofadstobeshown,sorted_avgout_feature_score)
	print("Most approapriate ads are : ",nameofads)

	return nameofads