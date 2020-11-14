from django import template


register = template.Library()


def get_board_id(unique_id):
    return unique_id.split("-")[-1]


register.filter('get_board_id', get_board_id)
