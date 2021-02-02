# coding: utf8
# author: Cusas@L.O.Team

import os

basePath="./data/apk/" #nust be end with /

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
fo=open("exclude","r")
exclude_apps=[]
for line in fo.readlines():
    exclude_apps.append(line.strip())
def ignore_app(appName):
    global exclude_apps
    for app in exclude_apps:
        if app == appName:
            return True
    return False
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
    if ignore_app(packname)==True:
        continue
    line='adb shell pm path '+packname
    print 'cmd==>'+line
    path = os.popen(line)
    line=path.read().replace('\n','').replace('\r','')
    print 'ret==>'+line
    split_count=0
    while line.find('package:')>=0:
        apppath=getrightstr(line,'package:')
        apppath=getleftstr(apppath,'package:')
        line=getrightstr(line,apppath)
        # print 'apppath='+apppath
        # print 'line='+line
        if apppath.find("/data/app/")>=0:
            if split_count==0:
                pullcmd='adb pull '+apppath+' '+basePath+'/'+packname+'.apk'
            else:
                pullcmd='adb pull '+apppath+' '+basePath+'/'+packname+'_'+str(split_count)+'.apk'
            split_count+=1
        else:
            pullcmd='adb pull '+getleftstrrev(apppath,"/")+'/ '+basePath+'/'
        print 'cmd==>'+pullcmd
        pull=os.popen(pullcmd)
        pullresult=pull.read()
        print 'ret==>'+pullresult
        if pullresult.find('100%')<0:
            fail_list+='['+packname+']'+pullcmd+'\n'
    #count+=1
    #if count>10:
    #    break
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
                line="vdexExtractor -i "+curPath+file
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
                line="./bin/compact_dex_converter "+curPath+file
                pull=os.popen(line)
                print(pull.read())
        else:
            decompilePathCdex(curPath+file+"/",depth+1)

decompilePath(basePath,1)
decompilePathCdex(basePath,1)

# step3: jadx decompile
startflag=True
def decompilePath(curPath,count):
    global startflag
    if count>30:
        print (curPath)
        return
    dirs=os.listdir(curPath)
    for file in dirs:
        if file=="" or file=="." or file=="..":
            count=count
        elif os.path.isfile(curPath+file):
            if startflag==False:
                if file=="com.xx.smarthome.apk":
                    startflag=True
            else:
                filetype=getrightstrrev(file,".")
                if filetype=="apk":
                    print(curPath+file)
                    sfile=curPath+file
                    dfile=sfile.replace("/apk/","/java/")
                    dfile=dfile.replace("/oat/arm64/","/")
                    line="jadx --show-bad-code --deobf --export-gradle --escape-unicode -j 4 -d "+dfile+" "+sfile
                    pull=os.popen(line)
                    print(pull.read())
                if filetype=="new":
                    print(curPath+file)
                    sfile=curPath+file
                    sfile=sfile.replace(".new",".dex")
                    os.rename(curPath+file,sfile)
                    dfile=curPath.replace("/apk/","/java/")
                    dfile=dfile.replace("/oat/arm64/","/")
                    line="jadx --show-bad-code --deobf --export-gradle --escape-unicode -j 4 -d "+dfile+" "+sfile
                    pull=os.popen(line)
                    print(pull.read())
                if filetype=="dex":
                    print(curPath+file)
                    sfile=curPath+file
                    dfile=curPath.replace("/apk/","/java/")
                    dfile=dfile.replace("/oat/arm64/","/")
                    line="jadx --show-bad-code --deobf --export-gradle --escape-unicode -j 4 -d "+dfile+" "+sfile
                    pull=os.popen(line)
                    print(pull.read())
        else:
            decompilePath(curPath+file+"/",count+1)
            
decompilePath(basePath,1)

