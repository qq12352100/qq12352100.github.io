#!/bin/bash
#备份目录
BACKUP=/data/backup/db
#当前时间
DATETIME=$(date +%Y-%m-%d_%H%M%S)
echo $DATETIME
#数据库的地址
HOST=locaLhost
#数据库用户名
DB_USER=root
#数据库密码
DB_Pw=hspedu100
#备份的数据库名
DATABASE=hspedu

#创建备份目录，如果不存在，就创建
[ ! -d "${BACKUP}/${DATETIME}" ] && mkdir -p "$ {BACKUP}/${DATETIME} "
#备份数据库
mysqldump -u${DB_USER} -p${DB_PW} --host=${HOST} -q -R --databases ${DATABASE} | gzip > ${BACKUP}/${DATETIME} /$DATETIME.sql.gz
#将文件处理成tar.gz
cd ${BACKUP}
tar -zcvf $DATETIME.tar.gz ${DATETIME}
#删除对应的备份目录
rm -rf ${BACKUP}/${DATETIME}
#删除10天前的备份文件
find ${BACKUP} -atime +10 - name "*.tar.gz" -exec rm -rf {} \;
echo "备份数据库 ${DATABASE} 成功!"
