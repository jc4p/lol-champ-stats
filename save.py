import shelve
from static import *
import json
import os

shelf = shelve.open("cache")

patch = "5.11"

def parse_champ(name):
    if name not in CHAMP_NAMES:
        return "Unable to find {}".format(name)

    if not shelf.has_key(name):
        return "No data for {}".format(name)

    champ = shelf[name]
    if not os.path.exists("Champions/{}/Recommended".format(name)):
        os.makedirs("Champions/{}/Recommended/".format(name))

    for role in champ.keys():
        data = get_base(name, role)
        if 'starters' in champ[role]:
            data['blocks'] += get_starters(champ[role]['starters'])
        if 'build' in champ[role]:
            data['blocks'] += get_build(champ[role]['build'])
        data['blocks'] += get_skills_and_misc(champ[role]['skills'], role)
        print "Saving {} {}".format(name, role)
        with open("Champions/{}/Recommended/{}{}.json".format(name, role, patch.replace(".", "_")), "w+") as f:
            f.write(json.dumps(data))

    return True
        
def get_base(name, role):
    data = json.loads(BASE_ATTRS)
    data['title'] = "{} {} {}".format(name, role, patch)
    data['champion'] = name
    return data

def get_starters(s):
    res = []

    for label in s.keys():
        d = s[label]

        block = {}
        block['type'] = "Start ({}) - {} win".format(label.title(), d['win_rate'])
        block['items'] = [{"count": v, "id": str(k)} for k,v in d['items'].iteritems()]
        # Let's jam a yellow trinket in there too
        block['items'].append({"count": 1, "id": "3340"})

        res.append(block)

    return res

def get_build(s):
    res = []

    for label in s.keys():
        d = s[label]

        block = {}
        block['type'] = "Build ({}) - {} win".format(label.title(), d['win_rate'])
        block['items'] = [{"count": 1, "id": str(k)} for k in d['items']]

        res.append(block)

    return res

def get_skills_and_misc(s, role):
    first = {"type": "Trinkets // Skill Order (Frequent) - {}".format(s['frequent']['order'] if 'frequent' in s else '')}
    second = {"type": "Consumables // Skill Order (Highest) - {}".format(s['highest']['order'] if 'highest' in s else '')}

    # Pink vision trinket, upgraded red trinket, upgraded blue trinket
    first['items'] = [{"count": 1, "id": "3362"}, {"count": 1, "id": "3364"}, {"count": 1, "id": "3363"}]

    # Health and mana pots
    second['items'] = [{"count": 1, "id": "2003"}, {"count": 1, "id": "2004"}]

    if role == "Middle" or role == "Support":
        second['items'].append({"count": 1, "id": "2139"})  # Elixir of Sorcery
    elif role == "Top" or role == "Jungle":
        second['items'].append({"count": 1, "id": "2138"})  # Elixir of Iron
    elif role == "ADC":
        second['items'].append({"count": 1, "id": "2140"})  # Elixir of Wrath

    second['items'].append({"count": 1, "id": "2044"})  # Green ward
    second['items'].append({"count": 1, "id": "2043"})  # Pink ward

    return [first, second]

if __name__ == "__main__":
    for champ in CHAMP_NAMES:
        parse_champ(champ)
    shelf.close()