import json, requests
from utils import *
from config import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Movie
from django.forms.models import model_to_dict

@api_view()
def search(request,query):
    rtURL=rottenTomatoesUrl +'/movies.json?q=' + query + '&apikey=' + rottenKey
    dbURL=theMovieDBUrl + '/search/movie?query=' + query + '&api_key=' + movieDBKey

    rtResponse=safeRequestJSON(rtURL)
    rtIDs=getIDrottenTomatoes(rtResponse) if rtResponse else localSearch("rottenTomatoes",query)

    dbResponse=safeRequestJSON(dbURL)
    dbIDs=getIDtheMovieDB(dbResponse) if dbResponse else localSearch("theMovieDB",query)
    return getResponse(rtIDs,dbIDs)

@api_view()
def now_playing(request):    
    rtNowUrl=rottenTomatoesUrl +'/lists/movies/in_theaters.json?&apikey=' + rottenKey
    dbNowUrl=theMovieDBUrl + '/movie/now_playing?&api_key=' + movieDBKey

    rtResponse=safeRequestJSON(rtNowUrl)
    rtIDs=getIDrottenTomatoes(rtResponse)

    dbResponse=safeRequestJSON(dbNowUrl)
    dbIDs=getIDtheMovieDB(dbResponse)
    return getResponse(rtIDs,dbIDs)

def getResponse(rtIDs,dbIDs):    
    rtMovies=getMovies(rtIDs)
    dbMovies=getMovies(dbIDs)
    finalMovies=aggregateMovies(rtMovies,dbMovies)
    # serialize model objects to json
    response=[model_to_dict(ob,exclude=['source','sourceID','id']) for ob in finalMovies]
    return Response(response)