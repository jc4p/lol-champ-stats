# lol-champ-stats
Python scripts to generate League of Legends item sets from champion.gg data

[Champion.gg](http://champion.gg/) is a website that tracks League of Legends champion's builds in high ranked games and aggregates that data.
These scripts *scrape* that data from Champion.gg and generate [Custom Item Sets](http://na.leagueoflegends.com/en/news/game-updates/game-updates/customize-your-build-client-item-sets) from them.

The item sets contain most played and highest win rate data for starting items, final item builds, and skill order.
In addition, they have common wards and elixirs attached at the bottom, so you hopefully don't have to ever use something other than the custom set.

# Usage (Easiest)

Download Champions.zip from the releases tab and unzip into the Champions folder of your League of Legends installation. If you're on a Windows computer, this is probably `C:\Riot Games\League of Legends\Config\Champions`. 

# Usage (Manual)

`python get.py` to scrape the newest data from Champion.gg and save them to a local file named 'cache'.

`python save.py` to process generated output from get.py and creates all item sets in a Champions directory.

Copy the contents of the Champions directory over to the folder described above.
