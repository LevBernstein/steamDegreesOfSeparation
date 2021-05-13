# Steam: How Far to the Top?

## Lev Bernstein

A Python program that finds the degrees of separation between a given Steam user and the top 10 highest-level Steam users.

Due to limitations of the Steam Web API, it can take quite a while to get friends information about a user with a sufficiently large (>50 people) friends list. Please be patient. In addition, note that this does not find the *optimal* path between two users, but rather the path between two users found by only visiting the highest-level friend of a given user.

## How Does It Work?

Starting with the initial user, the algorithm vists a user's highest-level friend, and keeps doing so until it reaches someone in the top 10, finds a private profile, hits a loop, or has otherwise explored the user's 5 highest-level friends. Essentially, this is a greedy, naive algorithm that functions similarly to depth-first search. I'm fairly confident it runs in O(n) time, where n is the number of users in the investigated component of the whole social network (or, in other words, n is the number of users in each isolated "island" of users). The worst case of the algorithm involves fully exploring every user in a component without ever making it to the top 10; that would be O(n) time. In terms of actual real-world runtime, the Steam Web API is quite slow; as far as I know, there is no way to load just the top 5 friends for a given profile. As such, a profile with 1600 friends will have to have every friend loaded by the API before it gives the algorithm any of the data.

## Installation

1. Download the repository.

2. Create a file named "steamKey.txt" that contains your Steam Web API key (go to [this link](https://steamcommunity.com/dev/) to register for an API key).

3. Install the required dependencies.

### Dependencies

* Python 3. To install, visit https://python.org/downloads/ and follow the instructions for your OS.

* Steam for Python. To install, do pip install -U steam.

* My modified version of the steamapi wrapper (downloadable [here](https://github.com/LevBernstein/steamapi).)

## Sample Output

```
Enter the URL for the steam profile you would like to check. URL must start with http.
For example: https://steamcommunity.com/profiles/76561197993787733.
URL: https://steamcommunity.com/id/beardless
Searching... this may take a while...
Exploring Captain No-Beard's profile...
Exploring The Red Crit's profile...
Exploring mushroom's profile...
Exploring Sovereign's profile...
Exploring [Nutter] garnet.gg's profile...
Private friends list or profile, moving on...
Exploring Drush's profile...
Found Ejay [bluestreak]! Here's the full path to their profile from Captain No-Beard: 
Captain No-Beard, The Red Crit, mushroom, Sovereign, Drush, Ejay [bluestreak].
Captain No-Beard's Ejay [bluestreak] Number is 5.
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
