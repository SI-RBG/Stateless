"""
File name: config.py
Purpose: To be imported by different files to use only common functions
"""
import sys

def debugMessage(q):
    """
    :param q: a string
    :return: None
    """
    print("Debug Message :" + str(q), file=sys.stderr)
