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


# Setup
try:
    with open("steamKey.txt", "r") as f: # in steamKey.txt, paste in your own Steam Web API Key
        myKey = f.readline()
        if "\n" in myKey:
            myKey = myKey[:-1]
except:
    print("Error! Could not read steamKey.txt!")
    sysExit(-1)
steamapi.core.APIConnection(api_key=myKey, validate_key=True)
TARGET = 76561197986603983 # StrikeR's STEAM64 ID

# Initial input
profileURL = input("Enter the URL for the steam profile you would like to check. URL must start with http.\n For example: https://steamcommunity.com/profiles/76561197993787733 or https://steamcommunity.com/id/beardless\n")
# Placeholders for testing:
#profileURL = "https://steamcommunity.com/profiles/76561198954124241"
#profileURL = "https://steamcommunity.com/id/beardless"
#profileURL = "https://steamcommunity.com/id/strykery"
#profileURL = "https://steamcommunity.com/id/St4ck"
#profileURL = "https://steamcommunity.com/id/The_Cpt_FROGGY"
#profileURL = "https://steamcommunity.com/profiles/76561197993787733"

try:
    profileID = steam.steamid.from_url(profileURL)
    if profileID == None:
        raise Exception("Invalid URL!")
    #print(profileID)
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
        usersPath.append(steamUser)
        print("Found StrikeR! Here's the full path to their profile from " + str(initialUser) + ": ")
        print(usersPath)
        print(str(initialUser) + "\'s StrikeR Number is " + str(len(usersPath) - 1) + ".")
        return steamUser
    if friendsPosition >= 5:
        return None
    if steamUser in usersPath:
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
    searching = True
    count = 0
    while searching:
        try:
            result = steamDegree(topFive[count], count) # currently very capable of running into infinite loops!
        except steamapi.errors.APIUnauthorized:
            print("Private profile, moving on...")
            result = None
        if result == None:
            count += 1
        else:
            return result
        if count >= 5:
            searching = False
    return None

try:
    initialUser = steamapi.user.SteamUser(profileID)
    steamDegree(initialUser, 0)
except steamapi.errors.APIUnauthorized as err:
    print("Error! Private profile! Your friends list must be publically accessible. (Error: " + str(err) + ")")
    sysExit(-1)

#initialUser = steamapi.user.SteamUser(profileID)
#steamDegree(initialUser, 0)
