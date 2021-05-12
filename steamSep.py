# Steam: How Far to the Top?
# Author: Lev Bernstein
# This tool measures the degrees of separation between a given Steam user and the highest-level user on steam. That user is currently St4ck, but since their friends list is private, this tool will instead measure the distance to StrikeR.
# For any user with a sufficiently large friends list, it will take quite a while to find all their friends. Expect to wait a while if you have a friends list of 50+ people.

import steam
import steamapi # (https://github.com/LevBernstein/steamapi)
from collections import OrderedDict
from operator import itemgetter
from steam.steamid import SteamID
from sys import exit as sysExit
#import requests

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
TARGET = 76561197986603983 # StrykeR's STEAM64 ID

# Initial input
#profileURL = input("Enter the URL for the steam profile you would like to check. URL must start with http.\n For example: https://steamcommunity.com/id/beardless\n")
#profileURL = "https://steamcommunity.com/profiles/76561198954124241" # Placeholder for testing
#profileURL = "https://steamcommunity.com/id/beardless" # Placeholder for testing
profileURL = "https://steamcommunity.com/id/strykery" # Placeholder for testing
#profileURL = "https://steamcommunity.com/id/St4ck"
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

def userLevel(user): # helper function for private profiles; for a given private profile, level will be recorded as 0
    try:
        return user.level
    except:
        return 0

def steamDegree(steamUser, friendsPosition):
    global usersPath
    global usersPathFriends
    if steamUser.steamid == TARGET:
        print("Found StrykeR! Here's the full path to their profile: ")
        print(usersPath)
        return steamUser
    if friendsPosition >= 5:
        return None
    usersPath.append(steamUser)
    friends = steamUser.friends
    topFive = []
    if len(friends) == 0:
            print("Empty friends list!")
            return None
    users = sorted(friends, key = lambda user: userLevel(user), reverse=True)
    print(users)
    limit = 5  # to limit API calls, will only try the 5 highest level friends
    if len(users) > limit:
        for i in range(limit):
            topFive.append(users[i])
    else:
        topFive = users
    print(topFive)
    usersPathFriends.append(topFive)

try:
    steamDegree(steamapi.user.SteamUser(profileID), 0)
except:
    print("Error! Private profile!")
    sysExit(-1)

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
