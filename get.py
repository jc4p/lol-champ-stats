import requests
import shelve
from time import sleep
from collections import defaultdict
from collections import OrderedDict
from bs4 import BeautifulSoup
from static import *

shelf = shelve.open("cache")

def get_champ(name):
    if name not in CHAMP_NAMES:
        return "Unable to find {}".format(name)
    
    if shelf.has_key(name):
        return shelf[name]

    url = "http://champion.gg/champion/" + name
    page = BeautifulSoup(requests.get(url).content)
    
    roles = []
    for link in page.select(".champion-profile ul li a"):
        roles.append(link.h3.string.strip())
    
    data = defaultdict(dict)
    data[roles[0]] = get_role(page)
    print "Parsed {} {}".format(name, roles[0])
    
    if len(roles) > 1:
        for role in roles[1:]:
            page = BeautifulSoup(requests.get(url + "/" + role).content)
            data[role] = get_role(page)
            print "Parsed {} {}".format(name, role)

    shelf[name] = dict(data)

    return dict(data)

def get_role(page):
    data = {}
    
    columns = page.select(".col-md-6")
    data['skills'] = get_skills(columns[0])
    data['starters'] = get_starters(columns[1].select(".col-md-5")[0])
    data['build'] = get_build(columns[1].select(".col-md-7")[0])
    return data

def get_skills(column):
    data = {}
    
    if len(column.select(".skill-order")) == 0:
        return data

    mf_skills = parse_skill_order(column.select(".skill-order")[0])
    mf_winrate = column.select(".build-text")[0].stripped_strings.next()
    data['frequent'] = {'order': mf_skills, 'win_rate': mf_winrate}
    
    hw_skills = parse_skill_order(column.select(".skill-order")[1])
    hw_winrate = column.select(".build-text")[1].stripped_strings.next()
    data['highest'] = {'order': hw_skills, 'win_rate': hw_winrate}

    return data

def parse_skill_order(el):
    selections = el.select(".skill-selections")
    row_labels = ["", "Q", "W", "E", "R"]
    
    data = {}
    for row_num in range(1, len(selections)):
        row = selections[row_num]
        label = row_labels[row_num]
        i = 1
        for div in row.find_all('div'):
            if 'selected' in div['class']:
                data[i] = label
            i += 1
    return "".join([str(x) for x in data.values()])

def get_starters(column):
    data = {}

    mf_starters = parse_starters(column.select(".build-wrapper")[0])
    mf_winrate = column.select(".build-text")[0].stripped_strings.next()

    hw_starters = parse_starters(column.select(".build-wrapper")[1])
    hw_winrate = column.select(".build-text")[1].stripped_strings.next()

    #only add them both if they're not the same
    mf_str = str(mf_starters)
    hw_str = str(hw_starters)
    
    if mf_str != hw_str:
        data['frequent'] = {'items': mf_starters, 'win_rate': mf_winrate}
        
    data['highest'] = {'items': hw_starters, 'win_rate': hw_winrate}

    return data

def parse_starters(el):
    # use OrderedDict so the items come back in the correct order
    items = OrderedDict()
    for img in el.find_all('img'):
        src = img['src']
        src = src[src.rindex('/') + 1:]
        item_id = int(src[:src.index('.')])
        current = items.get(item_id, 0)
        items[item_id] = current + 1
    return items

def get_build(column):
    data = {}
    mf_build = parse_build(column.select(".build-wrapper")[0])
    mf_winrate = column.select(".build-text")[0].stripped_strings.next()
    data['frequent'] = {'items': mf_build, 'win_rate': mf_winrate}

    hw_build = parse_build(column.select(".build-wrapper")[1])
    hw_winrate = column.select(".build-text")[1].stripped_strings.next()
    data['highest'] = {'items': hw_build, 'win_rate': hw_winrate}
    
    return data

def parse_build(el):
    return [int(x) for x in parse_starters(el).keys()]

if __name__ == "__main__":
    for champ in CHAMP_NAMES:
        get_champ(champ)
        sleep(0.5)
    shelf.close()