#########################################################################
# 自动更新脚本
#########################################################################
#!/bin/bash

ftpAddr="http://songjian:songjian@119.3.235.61:7005/bkk/log/"

fname="localhostlog.sh"
rm -f $fname
wget $ftpAddr$fname
chmod 744 $fname