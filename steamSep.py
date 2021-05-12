# Steam: How Far to the Top?
# Author: Lev Bernstein
# This tool measures the degrees of separation between a given Steam user and the top 10 highest-level users on steam.
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
TOPTEN = [76561198023414915, 76561197986603983, 76561198294650349, 76561198046160451, 76561197984432884, 76561198048165534, 76561198409565259, 76561198062673538, 76561198039386132, 76561197968423451]
# If a member of the top 10 has their friends list set to private, you will likely not be able to form a path to them

# Initial input
profileURL = input("Enter the URL for the steam profile you would like to check. URL must start with http.\nFor example: https://steamcommunity.com/profiles/76561197993787733.\n")
# Placeholders for testing:
#profileURL = "https://steamcommunity.com/profiles/76561198954124241"
#profileURL = "https://steamcommunity.com/id/strykery"
#profileURL = "https://steamcommunity.com/id/The_Cpt_FROGGY"
#profileURL = "https://steamcommunity.com/profiles/76561197993787733"
#profileURL = "https://steamcommunity.com/profiles/76561198061765150"
#profileURL = "https://steamcommunity.com/id/beardless"

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
exploredUsers = []

def userLevel(user): # helper function for private profiles or random API errors; for a given private or broken profile, level will be recorded as 0
    try:
        return user.level
    except:
        return 0

def steamDegree(steamUser, friendsPosition): # users with extremely large friends lists will break the script
    global usersPath
    global usersPathFriends
    global exploredUsers
    if steamUser.steamid in TOPTEN:
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
    if friendsPosition >= 5:
        print("We've checked this person's top 5 friends, time to move on...")
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
    limit = 5  # to limit API calls, will only try the 5 highest level friends
    if len(users) > limit:
        for i in range(limit):
            topFive.append(users[i])
    else:
        topFive = users
    #print(topFive)
    usersPathFriends.append(topFive)
    searching = True
    count = 0
    while searching:
        try:
            result = steamDegree(topFive[count], count)
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
    print("Searching... this may take a while...")
    result = steamDegree(initialUser, 0)
    if result == None:
        print("Unable to find a path to the top 10. The necessary profiles might have private friends lists, or doing so would require looking beyond a user's 5 highest-level friends. Or the path could just not exist.")
except steamapi.errors.APIUnauthorized as err:
    print("Error! Private profile! Initial user's friends list must be publically accessible. (Error: " + str(err) + ")")
    sysExit(-1)
