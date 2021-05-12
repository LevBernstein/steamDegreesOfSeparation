# Steam: How Far to the Top?

A Python program that finds the degrees of separation between a given Steam user and the top 10 highest-level Steam users.

Due to limitations of the Steam Web API, it can take quite a while to get friends information about a user with a sufficiently large (>50 people) friends list. Please be patient. In addition, note that this does not find the *optimal* path between two users, but rather the path between two users found by only visiting the highest-level friend of a given user.

## Installation

1. Download the repository.

2. Create a file named "steamKey.txt" that contains your Steam Web API key (go to [this link](https://steamcommunity.com/dev/) to register for an API key).

3. Install the required dependencies.

### Dependencies

* Python 3. To install, visit https://python.org/downloads/ and follow the instructions for your OS.

* Steam for Python. To install, do pip install -U steam.

* My modified version of the steamapi wrapper (downloadable [here](https://github.com/LevBernstein/steamapi).)

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
