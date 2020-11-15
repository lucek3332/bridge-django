from django import template
from math import ceil


register = template.Library()


def get_board_id(unique_id):
    return unique_id.split("-")[-1]


def get_suit(hand, color):
    res = []
    for c in hand:
        if color in c:
            if len(c) == 2:
                res.append(c[1])
            elif "10" in c:
                res.append("T")
            elif "11" in c:
                res.append("J")
            elif "12" in c:
                res.append("Q")
            elif "13" in c:
                res.append("K")
            elif "14" in c:
                res.append("A")
    return res


def get_bidding(bidding):
    bidding = [b.strip(" [''] ") for b in bidding]
    res = []
    countRows = ceil(len(bidding) / 4)
    for row in range(countRows):
        res.append(bidding[row * 4: row * 4 + 4])
    return res


def get_tricks(tricks):
    tricks = [t.strip(" [''] ") for t in tricks]
    modified_tricks = []
    for t in tricks:
        if t.endswith("*") and len(t) == 4:
            if '10' in t:
                t = 'T' + t[0].lower() + "*"
            elif '11' in t:
                t = 'J' + t[0].lower() + "*"
            elif '12' in t:
                t = 'Q' + t[0].lower() + "*"
            elif '13' in t:
                t = 'K' + t[0].lower() + "*"
            elif '14' in t:
                t = 'A' + t[0].lower() + "*"
        elif t.endswith("*") and len(t) == 3:
            t = t[1] + t[0].lower() + "*"
        elif len(t) == 3:
            if '10' in t:
                t = 'T' + t[0].lower()
            elif '11' in t:
                t = 'J' + t[0].lower()
            elif '12' in t:
                t = 'Q' + t[0].lower()
            elif '13' in t:
                t = 'K' + t[0].lower()
            elif '14' in t:
                t = 'A' + t[0].lower()
        else:
            t = t[1] + t[0].lower()
        modified_tricks.append(t)

    res = []
    countRows = ceil(len(modified_tricks) / 4)
    for row in range(countRows):
        res.append(modified_tricks[row * 4: row * 4 + 4])
    res = [row[1::] + [row[0]] for row in res]
    return res


register.filter('get_board_id', get_board_id)
register.filter('get_suit', get_suit)
register.filter('get_bidding', get_bidding)
register.filter('get_tricks', get_tricks)
