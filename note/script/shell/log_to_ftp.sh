logname=('/var/log/hik_sdk_to_ftp4.log' \
'/var/log/yisa_put_file_to_ftp.log' \
)
echo "------视频网--------`date +%Y_%m_%d---%H_%M_%S`" >> /log.txt
/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:" >> /log.txt
fdisk -l | grep "Disk /dev/sd" | awk -F '[ :,]+' '{printf "%.0f\n",$5/1072741824}' | awk -v total=0 '{total+=$1}END{printf "磁盘总共：%.0fG\n",total}' >> /log.txt
df -h | grep '^/dev/' >> /log.txt
free -g | sed -n '2p' | awk -v a='G' '{print "内存总共：",$2a,"使用：",$3a,"剩余：",$4a}' >> /log.txt
echo '-----------------------------------------------------------------------------------------------------' >> /log.txt
ps -ef | grep 'python' | grep 'start$' | awk '{print $8,$9,$10}'| sort -k 2 | uniq | wc -l |awk '{print "正在运行的python脚本:",$1-1}' >> /log.txt
ps -ef | grep 'python' | grep 'start$' | awk '{print $8,$9,$10}'| sort -k 2 | uniq >> /log.txt
ps -ef | grep 'python' | grep ':app$' | awk '{print $13,$NF}' | uniq >> /log.txt
ps -ef | grep 'redis' | grep -v 'color' | wc -l |awk '{print "正在运行的redis程序:",$1}'  >> /log.txt
java -jar r.jar | tr "\n" ","| sed -e 's/,$/\n/' >> /log.txt
cat /var/log/yisa_put_file_to_ftp.log|grep 'set(' |tail -n 10 >> /log.txt
for i in ${logname[@]}
do
echo "--------------------------【${i}】------------------------" >> /log.txt
tail -n 10 $i >> /log.txt
done
echo "===============================================================================================================================视频网===`date +%Y_%m_%d---%H_%M_%S`" >> /log.txt
sleep 3s
mv /log.txt /ftpdata/yisa_car/log.txt