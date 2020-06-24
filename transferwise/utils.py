import re


def camelcase(string):
    string = re.sub(r"^[\-_\.]", '', str(string))
    if not string:
        return string
    return string[0].lower() + re.sub(r"[\-_\.\s]([a-z])", lambda matched: matched.group(1).upper(), string[1:])


def snakecase(string):
    string = re.sub(r"[\-\.\s]", '_', str(string))
    if not string:
        return string
    if string == string.upper():
        return string.lower()
    return string[0].lower() + re.sub(r"[A-Z]", lambda matched: '_' + matched.group(0).lower(), string[1:])
