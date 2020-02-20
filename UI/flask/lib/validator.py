"""
This file should have independent fuctions where it validates data.


    # Tested on:
        # https://regex101.com/
        # http://gamon.webfactional.com/regexnumericrangegenerator/
"""

import re


def isIP(parameter):
    """
    Is parameter an IP?

    :return:
    """
    regx = "\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b"
    if re.match(regx, str(parameter)):
        # If the 4th octet is .0
        if str(parameter).strip('.')[-1] == "0":
            return False
        return True
    return False


def isNetwork(parameter):
    """
    Is parameter a network?
    # ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])/([1-9]|[12][0-9]|3[0-2])$

    :return:
    """
    regx = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])/([1-9]|[12][0-9]|3[0-2])$"

    if re.match(regx, str(parameter)):
        return True
    return False


def isMask(parameter):
    """
    Is parameter a network?

    :return:
    """
    return None


def isNetwork(parameter):
    """
    Is parameter a network?

    :return:
    """
    return None


def isDomain(parameter):
    """
    Is parameter a domain?

    :return:
    """
    regx = "^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$"
    if re.match(regx, str(parameter)):
        return True
    return False



