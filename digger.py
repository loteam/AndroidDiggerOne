#encoding : utf-8
import os


def getrightstrrev(pstr,psub):
    ipos=pstr.rfind(psub)
    if ipos<0:
        return pstr
    else:
        return pstr[ipos+len(psub):len(pstr)]
