from database import escape_string
# This is probably a terrible sanitizing function, it just
# emulates QUOTE
def sanitize(item):
    if isinstance(item, str):
        return escape_string(item)
    else:
        return item
