import steam
import steamapi # (https://github.com/LevBernstein/steamapi)
#import requests
from collections import OrderedDict
from operator import itemgetter
from steam.client import SteamClient
from steam.webapi import WebAPI
from steam.steamid import SteamID
from sys import exit as sysExit

# Dependencies: steam, eventemitter, steamapi, steamladder api

# Setup
try:
    with open("steamKey.txt", "r") as f: # in steamKey.txt, paste in your own Steam Web API Key
        myKey = f.readline()
        if "\n" in myKey:
            myKey = myKey[:-1]
except:
    print("Error! Could not read steamKey.txt!")
    sysExit(-1)
try:
    with open("ladderKey.txt", "r") as f: # in steamKey.txt, paste in your own Steam Web API Key
        ladderKey = f.readline()
        if "\n" in ladderKey:
            ladderKey = ladderKey[:-1]
except:
    print("Error! Could not read ladderKey.txt!")
    sysExit(-1)
ladderURL = 'https://steamladder.com/api/v1'
steamapi.core.APIConnection(api_key=myKey, validate_key=True)

# Initial input
#profileURL = input("Enter the URL for the steam profile you would like to check. URL must start with http.\n For example: https://steamcommunity.com/id/beardless\n")
profileURL = "https://steamcommunity.com/profiles/76561198954124241"
try:
    profileID = steam.steamid.from_url(profileURL)
    if profileID == None:
        raise Exception("Invalid URL!")
    print(profileID)
except:
    print("Invalid URL!")
    sysExit(-1)

usersPath = []
usersPathFriends = []

def steamDegree(profileID, friendsPosition):
    global usersPath
    global usersPathFriends
    user = steamapi.user.SteamUser(profileID)
    usersPath.append(user)
    friends = user.friends
    usersPathFriends.append(friends)
    levels = []
    diction = {}
    topFive = []

    for friend in friends:
        try:
            levels.append(friend.level)
        except:
            levels.append(0)
    for i in range(len(friends)):
        diction[friends[i]] = levels[i]
    sortedDict = OrderedDict(sorted(diction.items(), key = itemgetter(1), reverse=True))
    #print(sortedDict)
    if len(friends) != 0:
        i = 0
        for key in sortedDict.keys():
            topFive.append(key)
            i+=1
            if i == 5: # to limit API calls, will only try the 5 highest from a friends list
                break
    else:
        print("Empty friends list!")
    print(topFive)

steamDegree(profileID, 0)

'''
def steamDegree(profileID, friendsPosition):
    # friendsPosition repsresents how far down the user's highest level friends we have looked
    r = requests.get(ladderURL + '/profile/' + str(profileID) + '/', headers={'Authorization': 'Token ' + ladderKey})
    print("Get: " + r.url)
    if r.status_code == 200:
        print(r.json()['steam_stats']['friends'])
        global usersPath
        usersPath.append(profileID)
    elif r.status_code == 401:
        print("Unauthorized.")
    elif r.status_code == 404:
        print("User not found.")
    elif r.status_code == 429:
        print("Request rate limited. Max 1000 requests per hour.")

steamDegree(profileID, 0)

'''
