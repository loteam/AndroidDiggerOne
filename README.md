## AndroidDiggerOne
从手机中拖出所有APP，并反编译成Java源码，最后利用opengrok创建索引

### 环境准备
1、安装adb
sudo apt install adb

2、获得vdexExtrator
git clone https://github.com/anestisb/vdexExtractor
cd vdexExtractor
./make.sh
./make.sh gcc
vim ~/.bashrc
Append a line==>export PATH=$PATH:~/tools/vdexExtractor/bin

3、获得compact_dex_converters
download it from: https://github.com/anestisb/vdexExtractor/issues/23
compact_dex_converter_linux.zip
Extrat to AndroidDiggerOne/bin/

4、获得jadx
sudo apt-get install openjdk-8-jdk
Download from: https://github.com/skylot/jadx/releases/tag/v1.2.0
vim ~/.bashrc
Append a line==>export PATH=$PATH:~/tools/vdexExtractor/bin:~/tools/jadx-1.2.0/bin

5、安装apache-tomcat
sudo apt-get install default-jdk
sudo apt-get install tomcat8
service tomcat8 status

6、获得opengrok
sudo apt-get install exuberant-ctags
https://github.com/oracle/opengrok/wiki/How-to-setup-OpenGrok
sudo cp ~/tools/opengrok-1.5.11/lib/source.war /var/lib/tomcat8/webapps/

### 运行工具
python2 ./pull_dec.py


