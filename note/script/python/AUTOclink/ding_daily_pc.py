import base



# 1360 * 768
time.sleep(5)
print(time.strftime("%Y年%m月%d日  %H:%M:%S 星期%w", time.localtime()) + "_start!")
# get_location()
# dingding(0)
taobao()
# xuexiqiangguo()
while 1:  # 循环条件为1必定成立
    ttime = int(time.strftime("%H%M", time.localtime()))
    # holiday = int(time.strftime("%m%d", time.localtime()))
    ding(ttime)
    time.sleep(60*10)


