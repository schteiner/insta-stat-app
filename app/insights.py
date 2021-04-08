from app.defines import getCreds, makeApiCall
import json
import requests

# python3 insights2.py

# allPostInsights = {}

# allPostInsights["n"] = "insights"
# print(allPostInsights)

def getAllUserMedia( params ) :
	""" Get users media
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict() # parameter to send to the endpoint
	# endpointParams['fields'] = 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	url = params['endpoint_base'] + params['instagram_account_id'] + '/media' # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

def getMediaInsightsById( params, ids ) :
	""" Get insights for a specific media id
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{ig-media-id}/insights?metric={metric}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['metric'] = params['metric'] # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	allInsights = []

	for id in ids:
		url = params['endpoint_base'] + str(id) + '/insights' # endpoint url
		response = makeApiCall( url, endpointParams, params['debug'] ) # make the api call
		allInsights.append(response)

	return allInsights

params = getCreds()
response = getAllUserMedia( params )

ids = []
for id in response['json_data']['data']:
	ids.append(id['id'])

# Вот тут может быть проблемный момент с получением id ig-media
while True:
	if 'next' in response['json_data']["paging"]:
		url = response['json_data']["paging"]['next']
		data = requests.get( url )

		response = dict() # тут я переопределил response для того что бы снять все придыдущие настройки и сделать все тоже само что и в defines.py
		response['json_data'] = json.loads( data.content )

		for id in response['json_data']['data']:
			ids.append(id['id'])
	else:
		break


# if 'VIDEO' == response['json_data']['data'][0]['media_type'] : # media is a video
# 	params['metric'] = 'engagement,impressions,reach,saved,video_views'
# else : # media is an image
# 	params['metric'] = 'engagement,impressions,reach,saved'

params['metric'] = 'engagement,impressions,reach,saved'
allInsights = getMediaInsightsById( params,  ids) # get insights for a specific media id

allPostInsightsNOT_FUNC = dict()

for n in range(0, len(allInsights) + 1):

	if 'error' in allInsights[n]['json_data']: # обработка ошибки, если статистика недоступна по данному посту
		print("\n---- ERROR MESSAGE -----\n")
		print(allInsights[n]['json_data']['error']['message'])
		break

	# print("\n---- "+ str(n + 1) + " POST INSIGHTS -----\n")

	insights = [] # engagement, impressions, reach, saved

	for insight in allInsights[n]['json_data']['data']:
		 
		insights.append(str( insight['values'][0]['value']))

		# print ("\t" + insight['title'] + " (" + insight['period'] + "): " + str( insight['values'][0]['value'] ))
	
	allPostInsightsNOT_FUNC[n] = insights

def allPostInsights(ins = allPostInsightsNOT_FUNC):
    return ins

def computeStat():
	stat = dict()

	for x in allPostInsightsNOT_FUNC:
		err = (int(allPostInsightsNOT_FUNC[x][0]) / int(allPostInsightsNOT_FUNC[x][2])) * 100
		stat[x] = round(err, 2)

	
	return stat


