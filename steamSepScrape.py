"""
Steam: How Far to the Top?
Author: Lev Bernstein
This tool measures the degrees of separation between a given Steam user and
the top 10 highest-level users on steam. This variant of the program uses
BeautifulSoup to scrape the steam website, resulting in a faster runtime.
"""

import requests
import steam
from bs4 import BeautifulSoup
from steam.steamid import SteamID

from collections import OrderedDict
from typing import Optional, List, Tuple, Union


# Test values:
# https://steamcommunity.com/id/strykery # in top 10
# https://steamcommunity.com/id/St4ck # in top 10 but private friends list
# https://steamcommunity.com/id/The_Cpt_FROGGY # close to top 10
# https://steamcommunity.com/profiles/76561197993787733 # close to top 10
# https://steamcommunity.com/profiles/76561198061765150 # close to top 10
# https://steamcommunity.com/id/ah_ # lots of loops, good for testing that


def profInput() -> Union[str, int]:
	profileURL = input(
		"Enter the URL for the steam profile you would like to check."
		" URL must start with http.\nFor example:"
		" https://steamcommunity.com/profiles/76561197993787733.\nURL: "
	)
	try:
		if steam.steamid.from_url(profileURL) is None:
			raise Exception("Error! Invalid URL!")
		return profileURL
	except Exception as e:
		print(e)
		return -1


def scrapeFriendsList(url: str) -> Union[List[str], int]:
	soup = BeautifulSoup(
		requests.get(url).content.decode("utf-8"), "html.parser"
	)
	return [
		i.attrs["href"]
		for i in soup.body.find_all("a", "friendBlockLinkOverlay")
	]


def getTopTen() -> List[str]:
	soup = BeautifulSoup(
		requests.get("https://steamladder.com/").content.decode("utf-8"),
		"html.parser"
	)
	leaderboard = soup.find_all("td", "id")
	clean = lambda y: y.find("a").attrs["href"].replace("profile", "profiles")
	return [
		requests.get(
			"https://steamcommunity.com" + clean(leaderboard[i])
		).url for i in range(10)
	]


def getUserName(url: str) -> str:
	return BeautifulSoup(
		requests.get(url).content.decode("utf-8"), "html.parser"
	).title.text[19:]


def found(
	url: str,
	userName: str,
	initialUrl: str
) -> Tuple[str, str]:
	global usersPath
	usersPath.append((url, userName))
	initialUserName = getUserName(initialUrl)
	print(
		f"Found {userName}! Here's the full path"
		f" to their profile from {initialUserName}: ",
		" -> ".join(user[1] for user in usersPath) + f".",
		f"{initialUserName} is {len(usersPath) - 1}"
		" users away from the top 10.",
		sep="\n"
	)
	return (url, userName)


def steamDegree(url: str, initialUrl: str) -> str:
	global usersPath, exploredUsers
	if not url.endswith("/"):
		url += "/"
	userName = getUserName(url)
	if url in topTen:
		# recursion base case 1; only ever reached if you try to run this on a
		# user in the top 10. Otherwise, base case 2 will be the one to fire.
		return found(url, userName, initialUrl)
	print(f"Exploring {userName}'s profile...")
	if (url, userName) in exploredUsers:
		print("We're in a loop! Exiting the loop and moving down the list...")
		return None
	usersPath.append((url, userName))
	exploredUsers.append((url, userName))
	topSix = scrapeFriendsList(url)
	if len(topSix) == 0:
		# Private or friendless profile
		print("Empty friends list or private profile! Moving back and down...")
		usersPath.pop()
		return None
	searching = True
	count = 0
	for user in topSix:
		# base case 2
		if user in topTen:
			return found(url, userName, initialUser)
	while searching:
		result = steamDegree(topSix[count], initialUrl)
		if result is None:
			count += 1
		else:
			return result
		if count >= len(topSix):
			print(
				"We've checked this person's top",
				len(topSix),
				"friends, time to move on..."
			)
			usersPath.pop()
			searching = False
	return None

if __name__ == "__main__":
	global usersPath, exploredUsers, topTen
	usersPath = []
	exploredUsers = []
	link = profInput()
	if link != -1:
		print("Fetching the top 10 highest-level Steam users...")
		topTen = getTopTen()
		print("Done!")
		print("Searching...")
		if steamDegree(link, link) is None:
			print(
				"Unable to find a path to the top 10. There are multiple",
				"possible reasons for this: the necessary profiles might have",
				"private friends lists; doing so could require looking beyond",
				"a user's 6 highest-level friends; or the path does not exist."
			)