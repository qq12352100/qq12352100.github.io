ps -ef | grep '[a]pp.py' | awk '{print $2}' | xargs kill -9
wget -O app.py https://raw.githubusercontent.com/qq12352100/note/master/note/script/python/web/app.py
wget -O TOTP.py https://raw.githubusercontent.com/qq12352100/note/master/note/script/python/web/TOTP.py
wget -O online_note.py https://raw.githubusercontent.com/qq12352100/note/master/note/script/python/web/online_note.py
wget -O stock.py https://raw.githubusercontent.com/qq12352100/note/master/note/script/python/web/stock.py
if [ ! -f "start_update_app.sh" ]; then
    wget -O start_update_app.sh https://raw.githubusercontent.com/qq12352100/note/master/note/script/python/web/start_update_app.sh
    chmod +x start_update_app.sh
fi

sleep 3
nohup python3 app.py > log.file 2>&1 &
sleep 1
tail -30f log.file

