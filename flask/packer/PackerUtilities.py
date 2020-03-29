"""
File name: PackerUtilities.py
Purpose: This file is only for common functions that PackerCore.py or other test files might use.
"""

def getIP(out):
    listOut = str(out.decode("utf-8")).split("\n")
    for line in listOut:
        print("out: " + line)
        if "IP address" in line:
            line = line.split(":")[2]
            print("Here it is!!! "+str(line))
            return line.strip()