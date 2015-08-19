"""Performs more in-depth parsing of raw_cards.json"""

import re

def parseModifiers(rule_text):
    """Extracts modifiers from rule text that don't have a condition.

    Returns a dictionary mapping each resource (e.g. actions or cards)
    to a value.

    Example:
      parseModifiers("+1 Coin; +2 Actions") returns:
      {'cards': 0, 'coins': 1, 'actions': 2, 'buys': 0}
    """
    action_re = r"^\+(\d+) Action[s]?[,;\s]*"
    card_re = r"^\+(\d+) Card[s]?[,;\s]*"
    buy_re = r"^\+(\d+) Buy[s]?[,;\s]*"
    coin_re = r"^\+(\d+) Coin[s]?[,;\s]*"
    # Local copy of argument
    rule_text = rule_text[:]

    actions = 0
    cards = 0
    buys = 0
    coins = 0
    while True:
        matches_any = False
        action_match = re.match(action_re, rule_text)
        if action_match:
            matches_any = True
            actions = int(action_match.groups()[0])
            rule_text = rule_text[action_match.end():]
            
        card_match = re.match(card_re, rule_text)
        if card_match:
            matches_any = True
            cards = int(card_match.groups()[0])
            rule_text = rule_text[card_match.end():]

        buy_match = re.match(buy_re, rule_text)
        if buy_match:
            matches_any = True
            buys = int(buy_match.groups()[0])
            rule_text = rule_text[buy_match.end():]

        coin_match = re.match(coin_re, rule_text)
        if coin_match:
            matches_any = True
            coins = int(coin_match.groups()[0])
            rule_text = rule_text[coin_match.end():]
            
        if not matches_any:
            break
        
    return {
        "actions": actions,
        "cards": cards,
        "buys": buys,
        "coins": coins
    }


def parseCost(cost_text):
    """Parses a card's cost text for coin and potion cost.

    Returns a dictionary in the following form:
    {"coins": 5, "uses_potion": True}
    """
    cost_re = r"\$(\d+)( 1P)?"
    match = re.match(cost_re, cost_text)
    return {
        "coins": int(match.group(1)),
        "uses_potion": match.group(2) is not None
    }


def parseTypes(type_text):
    """Returns a list of card types that this Card is a part of.

    Example return for Militia: ["Action", "Attack"]
    """
    types = ["Action", "Victory", "Treasure", "Curse",
             "Attack", "Reaction", "Duration", "Reserve", "Event"]
    return filter(lambda t: t in type_text, types)
