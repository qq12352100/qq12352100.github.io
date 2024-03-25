#无法连互联网注释掉前两行wget
wget https://github.com/codeskyblue/gohttpserver/releases/download/1.1.0/gohttpserver_1.1.0_linux_amd64.tar.gz
wget https://studygolang.com/dl/golang/go1.16.4.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.16.4.linux-amd64.tar.gz
tar -xzf gohttpserver_1.1.0_linux_amd64.tar.gz
echo "export PATH=$PATH:/usr/local/go/bin" >> /etc/profile
source /etc/profile
./gohttpserver -r ./FTPDATA --port 8000 --auth-type http --auth-http bkk:bkk --upload --delete
#-r 根目录
#--delete 删除+新建文件夹
#--auth-type http --auth-http bkk:bkk 用户名密码