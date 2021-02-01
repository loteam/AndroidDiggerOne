# coding: utf8
# author: Cusas@L.O.Team

import os

basePath="./data/apk"

def getrightstr(pstr,psub):
    ipos=pstr.find(psub)
    if ipos<0:
        return pstr
    else:
        return pstr[ipos+len(psub):len(pstr)]
def getrightstrrev(pstr,psub):
    ipos=pstr.rfind(psub)
    if ipos<0:
        return pstr
    else:
        return pstr[ipos+len(psub):len(pstr)]
def getleftstr(pstr,psub):
    ipos=pstr.find(psub)
    if ipos<0:
        return pstr
    else:
        return pstr[0:ipos]
def getleftstrrev(pstr,psub):
    ipos=pstr.rfind(psub)
    if ipos<0:
        return pstr
    else:
        return pstr[0:ipos]
def printhex(pstr):
    for char in pstr:
        print ord(char)
        
# step1: pull all apps
os.popen('adb root')
packlist = os.popen('adb shell "pm list packages"')
fail_list=''
count=0
while True:
    line=packlist.readline()
    if line=='':
        break
    packname=line.replace('\n','').replace('\r','').replace('package:','')
    print '['+packname+']'
    line='adb shell pm path '+packname
    print 'cmd==>'+line
    path = os.popen(line)
    line=path.read().replace('\n','').replace('\r','')
    print 'ret==>'+line
    while line.find('package:')>=0:
        apppath=getrightstr(line,'package:')
        apppath=getleftstr(apppath,'package:')
        line=getrightstr(line,apppath)
        # print 'apppath='+apppath
        # print 'line='+line
        if apppath.find("/data/app/")>=0:
            pullcmd='adb pull '+apppath+' '+basePath+'/'+packname+'.apk'
        else:
            pullcmd='adb pull '+getleftstrrev(apppath,"/")+'/ '+basePath+'/'
        print 'cmd==>'+pullcmd
        pull=os.popen(pullcmd)
        pullresult=pull.read()
        print 'ret==>'+pullresult
        if pullresult.find('100%')<0:
            fail_list+='['+packname+']'+pullcmd+'\n'
    count+=1
    if count>10:
        break
print '[Fail list==============>\n'+fail_list

# step2: decompile vdex->cdex->dex
def decompilePath(curPath,depth):
    if depth>30:
        print (curPath)
        return
    dirs=os.listdir(curPath)
    for file in dirs:
        if file=="" or file=="." or file=="..":
            depth=depth
        elif os.path.isfile(curPath+file):
            filetype=getrightstrrev(file,".")
            if filetype=="vdex":
                print(curPath+file)
                line="./bin/vdexExtractor -i "+curPath+file
                pull=os.popen(line)
                print(pull.read())
        else:
            decompilePath(curPath+file+"/",depth+1)
def decompilePathCdex(curPath,depth):
    if depth>30:
        print (curPath)
        return
    dirs=os.listdir(curPath)
    for file in dirs:
        if file=="" or file=="." or file=="..":
            depth=depth
        elif os.path.isfile(curPath+file):
            filetype=getrightstrrev(file,".")
            if filetype=="cdex":
                print(curPath+file)
                line="./bin/compact_dex_converters "+curPath+file
                pull=os.popen(line)
                print(pull.read())
        else:
            decompilePathCdex(curPath+file+"/",depth+1)

decompilePath(basePath,1)
decompilePathCdex(basePath,1)