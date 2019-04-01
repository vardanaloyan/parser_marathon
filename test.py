import re
def reprDist(val):
    retval = float(re.findall(r"[-+]?\d*\.\d+|\d+", val)[0])
    unit = val.replace(re.findall(r"[-+]?\d*\.\d+|\d+", val)[0], "").strip()
    return retval, str(retval)+unit
print reprDist("100mb")