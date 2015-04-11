# lol-champ-stats
Python scripts to generate League of Legends item sets from champion.gg data

[Champion.gg](http://champion.gg/) is a website that tracks League of Legends champion's builds in high ranked games and aggregates that data.
These scripts *scrape* that data from Champion.gg and generate [Custom Item Sets](http://na.leagueoflegends.com/en/news/game-updates/game-updates/customize-your-build-client-item-sets) from them.

The item sets contain most played and highest win rate data for starting items, final item builds, and skill order.
In addition, they have common wards and elixirs listed at the end of the page. If you have any ideas of more things to add, please [open an issue](https://github.com/jc4p/lol-champ-stats/issues).

![Example Image](http://i.imgur.com/ITidkEA.jpg)

# Usage (Easy Way)

Download the newest Champions.zip [from the releases tab](https://github.com/jc4p/lol-champ-stats/releases) and unzip into the Champions folder of your League of Legends installation. If you're on a Windows computer, this is probably `C:\Riot Games\League of Legends\Config\Champions`.

# Usage (Manual Way)

> Note: This assumes you already have Python 2.x installed. If you are on Windows and haven't installed it before, you probably don't have it. You can download Python from https://www.python.org/downloads/ -- Please download the 2.7.x version, not the 3.x version.

> This also assumes you have `pip` installed. If you don't, just run `easy_install pip` and you should be all set.

- First, we need to install the dependencies, you can do this with pip by running `pip install -r requirements.txt`  from a command prompt.
- `python get.py` will scrape the newest data from Champion.gg and save them to a local file named 'cache'.
- `python save.py` will process the output from get.py and create the item sets into a new directory called Champions.
- Finally, copy the contents of the Champions directory over to the folder described above.
