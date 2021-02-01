#encoding : utf-8
import os


def getrightstrrev(pstr,psub):
    ipos=pstr.rfind(psub)
    if ipos<0:
        return pstr
    else:
        return pstr[ipos+len(psub):len(pstr)]
startflag=False
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
                if file=="com.xiaomi.smarthome.apk":
                    startflag=True
            else:
                filetype=getrightstrrev(file,".")
                if filetype=="apk":
                    print(curPath+file)
                    sfile=curPath+file
                    dfile=sfile.replace("/APKs/","/Java/")
                    dfile=dfile.replace("/oat/arm64/","/")
                    line="D:/os/shared/decompileAPK/jadx-0.9.0/bin/jadx.bat --show-bad-code --deobf --export-gradle --escape-unicode -j 4 -d "+dfile+" "+sfile
                    pull=os.popen(line)
                    print(pull.read())
                if filetype=="new":
                    print(curPath+file)
                    sfile=curPath+file
                    sfile=sfile.replace(".new",".dex")
                    os.rename(curPath+file,sfile)
                    dfile=curPath.replace("/APKs/","/Java/")
                    dfile=dfile.replace("/oat/arm64/","/")
                    line="D:/os/shared/decompileAPK/jadx-0.9.0/bin/jadx.bat --show-bad-code --deobf --export-gradle --escape-unicode -j 4 -d "+dfile+" "+sfile
                    pull=os.popen(line)
                    print(pull.read())
                if filetype=="dex":
                    print(curPath+file)
                    sfile=curPath+file
                    dfile=curPath.replace("/APKs/","/Java/")
                    dfile=dfile.replace("/oat/arm64/","/")
                    line="D:/os/shared/decompileAPK/jadx-0.9.0/bin/jadx.bat --show-bad-code --deobf --export-gradle --escape-unicode -j 4 -d "+dfile+" "+sfile
                    pull=os.popen(line)
                    print(pull.read())
        else:
            decompilePath(curPath+file+"/",count+1)
            
# basePath="/mnt/hgfs/shared/decompileAPK/"
basePath="D:/os/shared/decompileAPK/APKs/"
decompilePath(basePath,1)