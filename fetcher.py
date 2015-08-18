"""This is a scraper for the "Dominion Visual Spoilers" website.

This script is extremely specific to the layout of the site at my time
of visiting (2015/08/17) and is likely to break if the website's
author changes the layout.

"""

from bs4 import BeautifulSoup
from collections import OrderedDict
from urllib2 import urlopen

import json

BASE_URL = "http://dominion.diehrstraits.com/"
ALL_CARDS_URL =  BASE_URL + "?set=All&f=list"
CARD_COLUMN = 1
TYPE_COLUMN = 3
COST_COLUMN = 4
RULES_COLUMN = 5

all_cards_url_contents = urlopen(ALL_CARDS_URL).read()
soup = BeautifulSoup(all_cards_url_contents, "html.parser")

# This loop fetches all of the data for each card except for its
# image, which we will retrieve later.
cards = []
for expansion_tag in soup.find_all('h2'):
    # First row is a header row, so we skip it.
    rows = expansion_tag.find_next('table').find_all('tr')[1:]
    for row in rows:
        columns = row.find_all('td')
        card_tag = columns[CARD_COLUMN].a

        cards.append(OrderedDict(
            link=card_tag['href'],
            name=card_tag.string,
            expansion=expansion_tag.string.replace("Dominion: ", ""),
            type=columns[TYPE_COLUMN].string,
            cost=columns[COST_COLUMN].string,
            rules=columns[RULES_COLUMN].string
        ))
        
            
# Visit each card's URL and fetch the card image from the page.
for card in cards:
    # Strip off the "./" at the beginning of the relative URL
    card_url = BASE_URL + card['link'][2:]
    card_soup = BeautifulSoup(urlopen(card_url).read(), "html.parser")
    image_url = BASE_URL + card_soup.table.a.img['src'][2:]
    
    image_data = urlopen(image_url).read()
    image_basename = image_url.split("/")[-1]
    local_image_path = "images/" + image_basename

    with open(local_image_path, "w") as image_file:
        print "Saving %s to %s." % (image_url, local_image_path)
        image_file.write(image_data)
    del card['link']
    card['image'] = local_image_path
    
# Dump the card data to JSON.
with open("raw_cards.json", "w") as card_data_file:
    card_data_file.write(json.dumps(cards, indent=4))

print "Saved card data to raw_cards.json"
