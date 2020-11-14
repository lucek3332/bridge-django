from django import template


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


register.filter('get_board_id', get_board_id)
register.filter('get_suit', get_suit)
