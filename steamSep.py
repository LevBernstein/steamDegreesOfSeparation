# Steam: How Far to the Top?
# Author: Lev Bernstein
# This tool measures the degrees of separation between a given Steam user and the top 10 highest-level users on steam.
# For any user with a sufficiently large friends list, it will take quite a while to find all their friends. Expect to wait a while if a user in the path has a friends list of 50+ people.

import steam
import steamapi # (https://github.com/LevBernstein/steamapi)
from steam.steamid import SteamID
from collections import OrderedDict
from operator import itemgetter
from sys import exit as sysExit

# Setup
try:
    with open("steamKey.txt", "r") as f: # in steamKey.txt, paste in your own Steam Web API Key
        myKey = f.readline()
        if myKey.endswith("\n"): # API doesn't handle line and carriage return characters well
            myKey = myKey[:-1]
        if myKey.endswith("\r"):
            myKey = myKey[:-1]
except:
    print("Error! Could not read steamKey.txt!")
    sysExit(-1)
steamapi.core.APIConnection(api_key=myKey, validate_key=True)
usersPath = []
usersPathFriends = []
exploredUsers = []
LIMIT = 5 # to limit API calls, will only try the 5 highest level friends
TOPTEN = [76561198023414915, 76561197986603983, 76561198294650349, 76561198046160451, 76561197984432884, 76561198048165534, 76561198409565259, 76561198062673538, 76561198039386132, 76561197968423451]
# If a member of the top 10 has their friends list set to private, you might not be able to form a path to them

def profInput():
    profileURL = input("Enter the URL for the steam profile you would like to check. URL must start with http.\nFor example: https://steamcommunity.com/profiles/76561197993787733.\nURL: ")
    # Placeholders for testing:
    #profileURL = "https://steamcommunity.com/profiles/76561198954124241"
    #profileURL = "https://steamcommunity.com/id/strykery"
    #profileURL = "https://steamcommunity.com/id/The_Cpt_FROGGY"
    #profileURL = "https://steamcommunity.com/profiles/76561197993787733"
    #profileURL = "https://steamcommunity.com/profiles/76561198061765150"
    try:
        profileID = steam.steamid.from_url(profileURL)
        if profileID == None:
            raise Exception("Invalid URL!")
    except Exception as err:
        print(str(err))
        sysExit(-1)
    return profileID

def userLevel(user): # helper method for private profiles or random API errors; for a given private or broken profile, level will be recorded as 0
    try:
        return user.level
    except:
        return 0

def found(steamUser):
    global usersPath
    usersPath.append(steamUser)
    print("Found " + str(steamUser) + "! Here's the full path to their profile from " + str(initialUser) + ": ")
    report = ""
    for user in usersPath:
        report += str(user) + ", "
    report = report[:-2] + "."
    print(report)
    #print(usersPath)
    print(str(initialUser) + "\'s " + str(steamUser) + " Number is " + str(len(usersPath) - 1) + ".")
    return steamUser

def steamDegree(steamUser, friendsPosition): # users with extremely large friends lists will break the script
    global usersPath
    global usersPathFriends
    global exploredUsers
    if steamUser.steamid in TOPTEN: # recursion base case 1; only ever reached if you try to run this on a user in the top 10. Otherwise, base case 2 will be the one to fire.
        return found(steamUser)
    if friendsPosition >= 5:
        print("We've checked this person's top 5 friends, time to move on...")
        usersPath.pop()
        return None
    print("Exploring " + str(steamUser) + "\'s profile...")
    if steamUser in usersPath or steamUser in exploredUsers:
        print("We're in a loop! Exiting the loop and moving down the list...")
        return None
    usersPath.append(steamUser)
    exploredUsers.append(steamUser)
    friends = steamUser.friends
    topFive = []
    if len(friends) == 0:
        print("Empty friends list!")
        return None
    users = sorted(friends, key = lambda user: userLevel(user), reverse=True)
    #print(users)
    if len(users) > LIMIT:
        for i in range(LIMIT):
            topFive.append(users[i])
    else:
        topFive = users
    #print(topFive)
    usersPathFriends.append(topFive)
    searching = True
    count = 0
    for user in topFive: # base case 2; workaround to allow accesing profiles with one-way private friends lists
        if user.steamid in TOPTEN:
            return found(user)
    while searching:
        try:
            result = steamDegree(topFive[count], count)
        except steamapi.errors.APIUnauthorized:
            print("Private friends list or profile, moving on...")
            usersPath.pop()
            result = None
        if result == None:
            count += 1
        else:
            return result
        if count >= len(topFive):
            searching = False
    return None

try:
    initialUser = steamapi.user.SteamUser(profInput())
    print("Searching... this may take a while...")
    result = steamDegree(initialUser, 0)
    if result == None:
        print("Unable to find a path to the top 10. The necessary profiles might have private friends lists, or doing so would require looking beyond a user's 5 highest-level friends. Or the path could just not exist.")
except steamapi.errors.APIUnauthorized:
    print("Error! Private friends list or profile! Initial user's friends list must be publically accessible.")
    sysExit(-1)
