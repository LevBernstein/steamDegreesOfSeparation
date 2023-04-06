# Steam: How Far to the Top?

## Lev Bernstein

A Python script that finds the degrees of separation between a given Steam user and the top 10 highest-level Steam users. This project represents me finally implementing an algorithm I've had in my head for almost a decade, but have lacked the experience to create until now.

This repository contains two versions of the same program: steamSepWithApi.py and steamSepScrape.py. The former uses the Steam API, while the latter uses webscraping. I would recommend using steamSepScrape.py, as it runs anywhere from 50% to 5000% faster. I include steamSepWithApi.py in this repo only to show the evolution of the program.

Please note that this does not find the *optimal* path between two users, but rather the path between two users found by visiting the highest-level friends of a given user.

## How Does It Work?

Starting with the initial user, the algorithm vists a user's highest-level friend, and keeps doing so until it reaches someone in the top 10, finds a private profile, hits a loop, or has otherwise explored the user's 5 (or 6 for steamSepScrape.py) highest-level friends. Essentially, this is a greedy, naive algorithm that functions similarly to depth-first search. I'm fairly confident it runs in O(n) time, where n is the number of users in a given component of the whole social network (or, in other words, n is the number of users in a given isolated "island" of users). The worst case of the algorithm involves fully exploring every user in a component without ever making it to the top 10; that would be O(n) time. In terms of actual real-world runtime, the Steam Web API is quite slow; as far as I know, there is no way to load just the top 5 friends for a given profile. As such, using the Steam API, a profile with 1600 friends will have to have every friend loaded by the API before it gives the algorithm any of the data. By contrast, the version of this program using web scraping will usually finish in 30 seconds to a minute. Please use that version instead, I beg you.

## Installation

1. Download the repository.

2. Create a file named "steamKey.txt" that contains your Steam Web API key (go to [this link](https://steamcommunity.com/dev/) to register for an API key).

3. Install the required dependencies.

### Dependencies

* Python 3. To install, visit https://python.org/downloads/ and follow the instructions for your OS.

* Steam for Python. To install, do `pip3 install -U steam`.

For steamSepScrape.py:

* Requests and Beautiful Soup. To install, do `pip3 install requests bs4`.

For steamSepWithApi.py:

* My modified version of the steamapi wrapper (downloadable [here](https://github.com/LevBernstein/steamapi).)

## Sample Output

```
Enter the URL for the steam profile you would like to check. URL must start with http.
For example: https://steamcommunity.com/profiles/76561197993787733.
URL: https://steamcommunity.com/id/beardless
Fetching the top 10 highest-level Steam users...
Done!
Searching...
Exploring Captain No-Beard's profile...
Exploring The Red Crit's profile...
Exploring Medic Fiend's profile...
Empty friends list or private profile! Moving back and down...
Exploring mushroom's profile...
Exploring Sovereign's profile...
Exploring PopcornDE's profile...
Exploring Apenox | Profile Designer's profile...
Found StiGGe! Here's the full path to their profile from Captain No-Beard:
Captain No-Beard -> The Red Crit -> mushroom -> Sovereign -> PopcornDE -> Apenox | Profile Designer -> StiGGe.
Captain No-Beard is 6 users away from the top 10.
```

## License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
