ps -ef|grep java|grep -v color|awk '{print $2}' | xargs kill -9
sleep 1s
rm -f log.file
sleep 3s
nohup java -jar master_base-0.0.1_BASE.jar >>log.file 2>&1 &
