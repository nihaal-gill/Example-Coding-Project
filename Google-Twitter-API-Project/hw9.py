import tkinter
from tkinter import Tk, Canvas, Frame, Button, Label, Entry, END, LEFT, BOTTOM, TOP, RIGHT, SUNKEN
import math
import ssl
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode, quote_plus
import json
import oauth2 as oauth
from urllib.parse import quote_plus
from twitteraccess import *
from generateMarkerString import *
import webbrowser

global lat, lng, urlIndex
lat = 0
lng = 0
urlIndex = 0

#
# In HW8 Q2 and HW 9, you will use two Google services, Google Static Maps API
# and Google Geocoding API.  Both require use of an API key.
# You have two options for getting an API key:
#   1. (STRONGLY RECOMMENDED and WORTH 1 POINT on each assigment)
#     Get your own.  I think it is a valuable learning experience to see how
#     signing up for and using these services works.
#     Getting a key requires that you have a Google account *and* that you
#     "enable billing" BUT I guarantee you can do this homework for free. Google
#     provides a free trial that provides $300 worth of API usage and that amount
#     is *far* more than you will use, and provided $200/mo free Maps-related
#     free. The chances are small that you'd use more than $1/day while working
#     on the homework. You can get your free account here. (It actually includes
#     much more than just access to Google Maps services):
#     https://console.cloud.google.com
#     You can also start here:
#        https://developers.google.com/maps/documentation/geocoding/get-api-key
#
#   2. Use the API key for the class that I will provide separate via ICON on
#      ICON. If you use this one *DO NOT* share it with anyone outside the class.
#
# When you have the API key, put it between the quotes in the string below
GOOGLEAPIKEY = "AIzaSyCSKoYf7PqR5gfAe8I_hLGTmVciV616Ij0"


# To run the HW9 program, call the last function in this file: HW9().

# The Globals class demonstrates a better style of managing "global variables"
# than simply scattering the globals around the code and using "global x" within
# functions to identify a variable as global.
#
# We make all of the variables that we wish to access from various places in the
# program properties of this Globals class.  They get initial values here
# and then can be referenced and set anywhere in the program via code like
# e.g. Globals.zoomLevel = Globals.zoomLevel + 1
#
class Globals:
    rootWindow = None
    mapLabel = None
    locationEntry = None
    searchEntry = None
    defaultLocation = "Mauna Kea, Hawaii"
    mapLocation = defaultLocation
    mapFileName = 'googlemap.gif'
    mapSize = 400
    zoomLevel = 9
    mapType = 'roadmap'
    tweets = None
    currentTweetIndex = 0
    currentTweetUrlIndex = 0
    TweetNum = 0
    markerUrl = None


# Given a string representing a location, return 2-element tuple
# (latitude, longitude) for that location
#
# See https://developers.google.com/maps/documentation/geocoding/
# for details
#

def geocodeAddress(addressString):
    urlbase = "https://maps.googleapis.com/maps/api/geocode/json?address="
    geoURL = urlbase + quote_plus(addressString)
    geoURL = geoURL + "&key=" + GOOGLEAPIKEY

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    stringResultFromGoogle = urlopen(geoURL, context=ctx).read().decode('utf8')
    jsonResult = json.loads(stringResultFromGoogle)
    if (jsonResult['status'] != "OK"):
        print("Status returned from Google geocoder *not* OK: {}".format(jsonResult['status']))
        return (0.0, 0.0)  # this prevents crash in retrieveMapFromGoogle - yields maps with lat/lon center at 0.0, 0.0
    loc = jsonResult['results'][0]['geometry']['location']
    return (float(loc['lat']), float(loc['lng']))


# Contruct a Google Static Maps API URL that specifies a map that is:
# - is centered at provided latitude lat and longitude long
#
# - Globals.mapSize-by-Globals.mapsize in size (in pixels),
# - is "zoomed" to the Google Maps zoom level in Globals.zoomLevel
#
# See https://developers.google.com/maps/documentation/static-maps/
#
# YOU WILL NEED TO MODIFY THIS TO BE ABLE TO
# 1) DISPLAY A PIN ON THE MAP
# 2) SPECIFY MAP TYPE - terrain vs road vs ...
#
def getMapUrl(lat, lng):
    urlbase = "http://maps.google.com/maps/api/staticmap?"
    args = "center={},{}&zoom={}&size={}x{}&maptype={}&{},{}{}&sensor=false&format=gif".format(lat, lng, Globals.zoomLevel, Globals.mapSize,
                                                               Globals.mapSize,Globals.mapType,lat,lng,Globals.markerUrl)
    args = args + "&key=" + GOOGLEAPIKEY
    mapURL = urlbase + args
    return mapURL


# Retrieve a map image via Google Static Maps API:
# - centered at the location specified by global propery mapLocation
# - zoomed according to global property zoomLevel (Google's zoom levels range from 0 to 21)
# - width and height equal to global property mapSize
# Store the returned image in file name specified by global variable mapFileName
#

def retrieveMapFromGoogle():
    global lat, lng, mapCenterLatLon
    lat, lng = geocodeAddress(Globals.mapLocation)
    mapCenterLatLon = (lat,lng)
    url = getMapUrl(lat, lng)
    urlretrieve(url, Globals.mapFileName)


##########
#  basic GUI code

def displayMap():
    retrieveMapFromGoogle()
    mapImage = tkinter.PhotoImage(file=Globals.mapFileName)
    Globals.mapLabel.configure(image=mapImage)
    # next line necessary to "prevent (image) from being garbage collected" - http://effbot.org/tkinterbook/label.htm
    Globals.mapLabel.mapImage = mapImage

def readEntriesSearchTwitterAndDisplayMap():
    global lat, lng, tweetPrintLabel, tweetLatLonList, screenNamesList, nameList, urlList, urlIndex, urlPrintLabel
    global mapCenterLatLon
    #print('function entered')
    Globals.currentTweetIndex = 0
    Globals.TweetNum = 1
    urlIndex = 0
    #### you should change this function to read from the location from an Entry widget
    #### instead of using the default location
    locationString = Globals.locationEntry.get()
    Globals.mapLocation = locationString
    lat, lng = geocodeAddress(Globals.mapLocation)
    getTweetsFromLocation()
    tweetPrintLabel.configure(text=printable(tweetsList[Globals.currentTweetIndex]))
    currentTweetNumLabel.configure(text='Tweet # {} of {}'.format('1', len(tweetsList)))
    screenNamePrintLabel.configure(text='@'+printable(screenNamesList[Globals.currentTweetIndex]))
    namePrintLabel.configure(text=printable(nameList[Globals.currentTweetIndex]))
    urlList = []
    tweetIndex = 0
    for ele in (Globals.tweets):
        urlList.append([])
        for url in ele['entities']['urls']:
            urlList[tweetIndex].append(url['expanded_url'])
        tweetIndex += 1
    urlPrintLabel.configure(text = urlList[Globals.currentTweetIndex][urlIndex])
    Globals.markerUrl = generateMarkerString(Globals.currentTweetIndex, tweetLatLonList, mapCenterLatLon)
    displayMap()
    #print(urlList)

def nextUrl():
    global urlList, urlPrintLabel,urlIndex
    if urlIndex < len(urlList[Globals.currentTweetIndex])-1:
        urlIndex += 1
        urlPrintLabel.configure(text=urlList[Globals.currentTweetIndex][urlIndex])

def prevUrl():
    global urlList, urlPrintLabel, urlIndex
    if urlIndex >= 1:
        urlIndex -= 1
        urlPrintLabel.configure(text=urlList[Globals.currentTweetIndex][urlIndex])

def nextTweet():
    global tweetsList,currentTweetNumLabel,tweetLatLonList, screenNamesList, nameList,screenNamePrintLabe,namePrintLabel
    global mapCenterLatLon
    if (Globals.currentTweetIndex + 1 != len(tweetsList)):
        Globals.currentTweetIndex += 1
        Globals.TweetNum += 1
        Globals.markerUrl = generateMarkerString(Globals.currentTweetIndex, tweetLatLonList, mapCenterLatLon)
        tweetPrintLabel.configure(text=printable(tweetsList[Globals.currentTweetIndex]))
        screenNamePrintLabel.configure(text='@'+printable(screenNamesList[Globals.currentTweetIndex]))
        namePrintLabel.configure(text=printable(nameList[Globals.currentTweetIndex]))
        currentTweetNumLabel.configure(text='Tweet # {} of {}'.format(Globals.TweetNum,len(tweetsList)))
        displayMap()


def prevTweet():
    global tweetsList,currentTweetNumLabel,namePrintLabel, screenNamePrintLable
    if (Globals.currentTweetIndex - 1 != len(tweetsList)-1 and Globals.currentTweetIndex - 1 >= 0):
        Globals.currentTweetIndex -= 1
        Globals.TweetNum -= 1
        Globals.markerUrl = generateMarkerString(Globals.currentTweetIndex, tweetLatLonList, mapCenterLatLon)
        tweetPrintLabel.configure(text=printable(tweetsList[Globals.currentTweetIndex]))
        tweetPrintLabel.configure(text=printable(tweetsList[Globals.currentTweetIndex]))
        screenNamePrintLabel.configure(text='@'+printable(screenNamesList[Globals.currentTweetIndex]))
        namePrintLabel.configure(text=printable(nameList[Globals.currentTweetIndex]))
        currentTweetNumLabel.configure(text='Tweet # {} out of {}'.format(Globals.TweetNum,len(tweetsList)))
        displayMap()

#function for being able to zoom in
def ZoomIn():
   Globals.zoomLevel += 1
   displayMap()

#function for being able to zoom out
def ZoomOut():
    Globals.zoomLevel -= 1
    displayMap()

def radioButtonChosen():
    global selectedButtonText
    global choiceVar
    global label

    if choiceVar.get() == 1:
        selectedButtonText = "roadmap"
        Globals.mapType = "roadmap"
    elif choiceVar.get() == 2:
        selectedButtonText = "satellite"
        Globals.mapType = "satellite"
    elif choiceVar.get() == 3:
        selectedButtonText = "terrain"
        Globals.mapType = "terrain"
    else:
        selectedButtonText = "hybrid"
        Globals.mapType = "hybrid"
    displayMap()
    label.configure(text="Radio button choice is: {}".format(selectedButtonText))

def openUrl():
    global urlList,urlIndex
    if urlIndex < len(urlList[Globals.currentTweetIndex]):
        if(urlList[Globals.currentTweetIndex][urlIndex] != None):
            webbrowser.open(urlList[Globals.currentTweetIndex][urlIndex])

def initializeGUIetc():
    global selectedButtonText, choiceVar, label, tweetsList, tweetPrintLabel,currentTweetNumLabel,urlPrintLabel,namePrintLabel
    global screenNamePrintLabel, urlList, urlIndex

    Globals.rootWindow = tkinter.Tk()
    Globals.rootWindow.title("HW9")

    locationLabelFrame = tkinter.Frame(Globals.rootWindow)
    locationLabel = Label(locationLabelFrame, text="Enter the location:")
    locationLabelFrame.pack()
    locationLabel.pack()

    Globals.locationEntry = tkinter.Entry()
    Globals.locationEntry.pack()

    seachTermFrame = tkinter.Frame(Globals.rootWindow)
    seachTermFrame.pack()
    seachTermLabel = Label(seachTermFrame, text="Enter your search term:")
    seachTermLabel.pack()

    Globals.searchEntry = tkinter.Entry()
    Globals.searchEntry.pack()

    mainFrame = tkinter.Frame(Globals.rootWindow)
    mainFrame.pack()

    # until you add code, pressing this button won't change the map (except
    # once, to the Beijing location "hardcoded" into readEntryAndDisplayMap)
    # you need to add an Entry widget that allows you to type in an address
    # The click function should extract the location string from the Entry widget
    # and create the appropriate map.
    readEntriesSearchTwitterAndDisplayMapButton = tkinter.Button(mainFrame, text="Show me the map!", command=readEntriesSearchTwitterAndDisplayMap)
    readEntriesSearchTwitterAndDisplayMapButton.pack()

    ZoomInButton = tkinter.Button(mainFrame,text="+", command=ZoomIn)
    ZoomInButton.pack()

    ZoomOutButton = tkinter.Button(mainFrame,text="-",command=ZoomOut)
    ZoomOutButton.pack()

    selectedButtonText = ""
    choiceVar = tkinter.IntVar()
    choiceVar.set(1)
    choice1 = tkinter.Radiobutton(mainFrame, text="Road Map View", variable=choiceVar, value=1,command=radioButtonChosen)
    choice1.pack()
    choice2 = tkinter.Radiobutton(mainFrame, text="Satellite Map View", variable=choiceVar, value=2, command=radioButtonChosen)
    choice2.pack()
    choice3 = tkinter.Radiobutton(mainFrame,text="Terrain Map View", variable=choiceVar,value=3,command=radioButtonChosen)
    choice3.pack()
    choice4 = tkinter.Radiobutton(mainFrame,text="Hybrid Map View", variable=choiceVar,value=4,command=radioButtonChosen)
    choice4.pack()

    label = tkinter.Label(mainFrame, text="radio button choice is: {}".format(selectedButtonText))
    label.pack()

    twitterTitleLabel = tkinter.Label(mainFrame, text='Twitter Information:')
    twitterTitleLabel.pack()

    tweetPrintLabel = tkinter.Label(mainFrame)
    tweetPrintLabel.pack()

    screenNamePrintLabel = tkinter.Label(mainFrame)
    screenNamePrintLabel.pack()

    namePrintLabel = tkinter.Label(mainFrame)
    namePrintLabel.pack()

    nextTweetButton = tkinter.Button(mainFrame, text='Next Tweet', command=nextTweet)
    nextTweetButton.pack()

    prevTweetButton = tkinter.Button(mainFrame, text='Previous Tweet', command=prevTweet)
    prevTweetButton.pack()

    currentTweetNumLabel = tkinter.Label(mainFrame)
    currentTweetNumLabel.pack()
    Globals.TweetNum += 1

    urlPrintLabel = tkinter.Label(mainFrame)
    urlPrintLabel.pack()

    nextUrlButton = tkinter.Button(mainFrame,text='Next Url',command=nextUrl)
    nextUrlButton.pack()

    prevUrlButton = tkinter.Button(mainFrame,text='Previous Url',command=prevUrl)
    prevUrlButton.pack()

    urlButton = tkinter.Button(mainFrame,text='Open Url',command=openUrl)
    urlButton.pack()
    # we use a tkinter Label to display the map image
    Globals.mapLabel = tkinter.Label(mainFrame, width=Globals.mapSize, bd=2, relief=tkinter.FLAT)
    Globals.mapLabel.pack()


def getTweetsFromLocation():
    global lat, lng,tweetsList,tweetLatLonList, screenNamesList, nameList, urlList
    tweetLatLonList = []
    tweetsList = []
    screenNamesList= []
    nameList = []
    urlList = []
    latLng= [lat,lng]
    searchTerm = Globals.searchEntry.get()
    print("Searching for", searchTerm, "around", latLng[0], ",", latLng[1])
    Globals.tweets = searchTwitter(searchTerm, latlngcenter=latLng)

    #iterate through the twitter dictionary (global.tweets in this case)
        #put all of the lat and longitude into a list called tweetLatLonList
        #put all of the tweets in a list as well
        #put all of the screen names into a list
        #put all of the names into a list

    
    for ele in Globals.tweets:
        if(ele['coordinates'] == None):
            tweetLatLonList.append(latLng)
        else:
            tweetLatLonList.append(ele['coordinates']['coordinates'])
        tweetsList.append(ele['text'])
        screenNamesList.append(ele['user']['screen_name'])
        nameList.append(printable(ele['user']['name']))

    for ele in tweetLatLonList:
        var1 = ele[0]
        var2 = ele[1]
        ele[0],ele[1] = var2, var1

    
def HW9():
    authTwitter()
    initializeGUIetc()
    displayMap()
    Globals.rootWindow.mainloop()
    getTweetsFromLocation()

HW9()