import base



# 1360 * 768
time.sleep(5)
print(time.strftime("%Y��%m��%d��  %H:%M:%S ����%w", time.localtime()) + "_start!")
# get_location()
# dingding(0)
taobao()
# xuexiqiangguo()
while 1:  # ѭ������Ϊ1�ض�����
    ttime = int(time.strftime("%H%M", time.localtime()))
    # holiday = int(time.strftime("%m%d", time.localtime()))
    ding(ttime)
    time.sleep(60*10)


