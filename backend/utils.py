from django.core.cache import cache
import json, requests
from django.db import models
from models import Movie
from config import *

# unique pair of identifiers. source can take 'rottenTomatoes' or 'theMovieDB' value. sourceID is the movie's ID in the source's API
class Identifiers():
	sourceID=int
	source=str	

# delimiter for actors string
actorsDelimiter=', '
# upper limit of actors to get from theMovieDB
numOfStarringActorsDB=5

def safeRequestJSON(url):
	response=None
	try:
		response = requests.get(url=url).json()
	except:
		pass
	return response		

def getIDrottenTomatoes(results):
	identifiersList=[]
	for element in results['movies']:
			identifiers=Identifiers()
			identifiers.sourceID=element['id']	
			identifiers.source='rottenTomatoes'
			identifiersList.append(identifiers)	
	return identifiersList

def getIDtheMovieDB(results):
	identifiersList=[]
	for element in results['results']:
			identifiers=Identifiers()
			identifiers.sourceID=element['id']	
			identifiers.source='theMovieDB'
			identifiersList.append(identifiers)		
	return identifiersList

# create movie list for given identifiers list
def getMovies(identifiers):
	movies=[]
	for ids in identifiers:
		movies.append(getDetails(ids))
	return movies

def getDetails(identifiers):
	try:
		movie=Movie.objects.get(sourceID=identifiers.sourceID,source=identifiers.source)
	except:
		movie=Movie()
		if identifiers.source=='rottenTomatoes':
			movie=fetchDetailsRottenTomatoes(identifiers)
		elif identifiers.source=='theMovieDB':
			movie=fetchDetailsTheMovieDB(identifiers)
		movie.save()
	return movie	

def fetchDetailsRottenTomatoes(identifiers):
	movie=Movie()
	movie.sourceID=identifiers.sourceID
	movie.source=identifiers.source
	url=rottenTomatoesUrl +'/movies/' + str(identifiers.sourceID) + '.json?apikey=' + rottenKey
	data=safeRequestJSON(url)
	reviewsUrl=rottenTomatoesUrl +'/movies/' + str(identifiers.sourceID) + '/reviews.json?apikey=' + rottenKey
	try:
		movie.year = str(data['year'])
	except:
		movie.year =''
	try:	
		movie.title = data['title']
	except:
		movie.title =''	
	try:
		movie.numReviews=safeRequestJSON(reviewsUrl)['total']
	except:
		movie.numReviews=0
	try:    
		movie.description=data['synopsis'] if data['synopsis'] else ''
	except:
		movie.description=''
	try:
		movie.actors=''
		for actor in data['abridged_cast']:
			if 	actor !=data['abridged_cast'][-1]:
				movie.actors+=actor['name'] + actorsDelimiter
			else:	
				movie.actors+=actor['name']
	except:
		movie.actors=''
	return movie	

def fetchDetailsTheMovieDB(identifiers):	
	movie=Movie()
	movie.sourceID=identifiers.sourceID
	movie.source=identifiers.source
	url=theMovieDBUrl + '/movie/' + str(identifiers.sourceID) + '?api_key=' + movieDBKey
	data=safeRequestJSON(url)
	reviewsUrl=theMovieDBUrl + '/movie/' + str(identifiers.sourceID) + '/reviews?api_key=' + movieDBKey
	try:
		movie.year = data['release_date'][:4]
	except:
		movie.year =''
	try:	
		movie.title = data['title']
	except:
		movie.title =''	
	try:
		movie.numReviews=safeRequestJSON(reviewsUrl)['total_results']
	except:
		movie.numReviews=0
	try:
		movie.description=data['overview'] if data['overview'] else ''
	except:
		movie.description='' 
	actorsUrl=theMovieDBUrl + '/movie/' + str(identifiers.sourceID) + '/credits?api_key=' + movieDBKey
	try:
		actors=safeRequestJSON(actorsUrl)['cast']
		movie.actors=''
		for actor in actors[:numOfStarringActorsDB]:	
			if 	actor !=actors[numOfStarringActorsDB-1]:
				movie.actors+=actor['name'] + actorsDelimiter
			else:	
				movie.actors+=actor['name']
	except:		   
		movie.actors=''
	return movie

def aggregateMovies(first,second):
	commonIndexes=[]
	finalMovies=[]
	for firstMovie in first:
	    finalMovie=Movie()
	    finalMovie.title=firstMovie.title
	    finalMovie.year=firstMovie.year
	    for index,secondMovie in enumerate(second):
	        if secondMovie.title==firstMovie.title and secondMovie.year==firstMovie.year:
	            finalMovie.numReviews=secondMovie.numReviews+firstMovie.numReviews
	            finalMovie.description=max([secondMovie.description,firstMovie.description], key=len)
	            actorsList=set(firstMovie.actors.split(actorsDelimiter) + secondMovie.actors.split(actorsDelimiter))
	            actorsList = list(firstMovie.actors.split(actorsDelimiter))
	            actorsList.extend(x for x in secondMovie.actors.split(actorsDelimiter) if x not in actorsList)
	            for actor in actorsList:	
	            	if 	actor !=actorsList[-1]:
	            		finalMovie.actors+=actor + actorsDelimiter
	            	else:	
	            		finalMovie.actors+=actor
	            commonIndexes.append(index)
	            break
	        elif secondMovie==second[-1]:
	            finalMovie.numReviews=firstMovie.numReviews
	            finalMovie.description=firstMovie.description	    
	            finalMovie.actors=firstMovie.actors
	    finalMovies.append(finalMovie)    
	for index,secondMovie in enumerate(second):
	    if index not in commonIndexes:
	        finalMovie=Movie()
	        finalMovie.title=secondMovie.title
	        finalMovie.year=secondMovie.year
	        finalMovie.numReviews=secondMovie.numReviews
	        finalMovie.description=secondMovie.description
	        finalMovie.actors=secondMovie.actors
	        finalMovies.append(finalMovie)
   	return finalMovies   

def localSearch(source,query):
	results=Movie.objects.filter(source=source).filter(title__icontains=query)
	movies=[]
	for result in results:
		movies.append(Movie.objects.get(sourceID=result.sourceID))
	return movies	

