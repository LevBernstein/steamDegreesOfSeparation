# Steam: How Far to the Top?

A Python program that finds the degrees of separation between a given Steam user and the top 10 highest-level Steam users.

Due to limitations of the Steam Web API, it can take quite a while to get friends information about a user with a sufficiently large (>50 people) friends list. Please be patient.

## Installation

1. Download the repository.

2. Create a file named "steamKey.txt" that contains your Steam Web API key (go to [this link](https://steamcommunity.com/dev/) to register for an API key).

3. Install the required dependencies.

### Dependencies

* Python 3. To install, visit https://python.org/downloads/ and follow the instructions for your OS.

* Steam for Python. To install, do pip install -U steam.

* My modified version of the steamapi wrapper (downloadable [here](https://github.com/LevBernstein/steamapi).)
