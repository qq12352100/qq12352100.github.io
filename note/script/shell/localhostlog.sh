#########################################################################
# 先删除本地20210325.txt，然后去FTP取20210325.txt，然后打印基本信息和logname的日志后10行到20210325.txt，然后上传到FTP
# 注意：要修改变量logname，ftpAddr
#########################################################################
#!/bin/bash
localName="69sqweb"
logname=('/var/log/yisa_get_file_from_ftp.log' \
'/var/log/yisa_worker_cpu.log' \
)
scriptName=('/root/bkk/localhostlog.sh' \
'/yisa_oe/message/config.yaml' \
'/yisa_oe/message/yisa_get_file_from_ftp.py' \
'/yisa_oe/message_car_cpu/config.yaml' \
'/yisa_oe/message_car_cpu/yisa_worker_to_kafka.py' \
'/yisa_oe/message_ssc/config.yaml' \
'/yisa_oe/message_ssc/ssc_upload_location_cache.py' \
)
#互联网
#ftpAddr="http://songjian:songjian@119.3.235.61:7005/bkk/log/"
#公安网
ftpAddr="http://songjian:songjian@10.52.223.3:36998/bkk/log/"

fname="`date +%Y%m%d`.txt"
rm -f 2021*.txt
wget $ftpAddr$fname
echo "------${localName}--------`date +%Y_%m_%d---%H_%M_%S`" >>$fname
#CPU
cat /proc/cpuinfo | grep "physical id" |sort -k 3| uniq | wc -l|awk '{print "CPU个数:",$0}'>> $fname
cat /proc/cpuinfo | grep "cpu cores" | uniq >> $fname
cat /proc/cpuinfo | grep 'model name' |uniq >> $fname
#IP
/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:" >> $fname
#fdisk
df -h | awk 'NF>2&&+$5>50{print $0}' >> $fname
fdisk -l | grep "Disk /dev/sd" | awk -F '[ :,]+' '{printf "%.0f\n",$5/1072741824}' | awk -v total=0 '{total+=$1}END{printf "磁盘总共：%.0fG\n",total}' >> $fname
df -h | grep '^/dev/' >> $fname
#free
free -g | sed -n '2p' | awk -v a='G' '{print "内存总共：",$2a,"使用：",$3a,"剩余：",$4a}' >> $fname
echo '-----------------------------------------------------------------------------------------------------' >> $fname
ps -ef | grep 'python' | grep 'start$' | uniq | wc -l |awk '{print "正在运行的python脚本:",$1-1}' >> $fname
ps -ef | grep 'python' | grep 'start$' | awk '{print $8,$9,$10}'| sort -k 2 | uniq >> $fname
ps -ef | grep 'python' | grep ':app$' | awk '{print $13,$NF}' | uniq >> $fname
screen -ls >> $fname
ps -ef | grep 'redis-' | grep -v 'color' | wc -l |awk '{print "正在运行的redis程序:",$1}' >> $fname
jps >> $fname
echo "--------------------------------------------------------------------------------------------------------------------------" >> $fname
#log
for i in ${logname[@]}
do
echo "--------------------------【${i}】------------------------" >> $fname
tail -n 10 $i >> $fname
done
echo "===============================================================================================================================${localName}===`date +%Y_%m_%d---%H_%M_%S`" >> $fname
curl -F file=@$fname $ftpAddr
#backup script
for i in ${scriptName[@]}
do
curl -F file=@$i $ftpAddr"bak/`date +%Y%m%d`/"$localName${i%/*}
done