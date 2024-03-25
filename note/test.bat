::默认编码格式为ANSI代表 GB2312 编码。
::不加@时，在运行时，会在窗口显示出这条命令,而加了@, 只会显示出 echo后面你要显示出的东西
mode con cols=80 lines=20&color 0c  rem  cols宽 lines高  cmd里面键入:help color 查查看
TITLE Tomcat                        rem  设置窗口标题
cmdow @ /top /mov 500 500           rem  移动窗口到某个位置 详见cmdow下载
@echo off 
@echo --  输出文字       --         rem 跟在输出后面会输出
::dir c:\*.* >a.txt                 rem 将c盘下所有文件名输出到a.txt中，如果没有a文件，则在bat同一目录下创建一个
::md D:\test                        rem 在D盘下创建test文件夹
::start http://www.baidu.com        rem 默认浏览器打开网页
::cd /d %~dp0                       rem 打开当前路径
@echo %AllUsersProfile%             rem    C:\ProgramData
@echo %tmp%                         rem    C:\Users\admin\AppData\Local\Temp
@echo %AppData%                     rem    C:\Users\admin\AppData\Roaming
@echo %CommonProgramFiles%          rem    C:\Program Files\Common Files
@echo %UserProfile%                 rem    C:\Users\admin
@echo %CD%                          rem 代表当前目录的字符串
@echo %DATE%                        rem 当前日期
@echo %TIME%                        rem 当前时间

set /p var=输入一个数:
if %var% EQU 1 (                    rem EQU 等于 || NEQ 不等于 || LSS 小于 || LEQ 小于或等于 ||  GTR 大于 || GEQ 大于或等于
    goto FIRST 
) else (
    goto SECOND 
)
:FIRST
@echo I AM FIRST
:SECOND
@echo I AM SECOND
:SECOND2
@echo I AM SECOND2

set a=aa1bb1aa2bb2
@echo %a%
set b=12
@echo %b%
set /a c=39/10           
@echo %c%

for  %%I in (A,B,C) do echo %%I     rem 循环
for /f "skip=1 tokens=9 delims= " %a in ('ping 172.20.123.231') do @echo %a
skip=1 #忽略第一行，默认显示所有行
tokens=9 #显示第9列 类似于awk的 参数$9
delims= #分隔符 本次分隔符为一个空格
ping 172.20.123.231 #循环该命令所有行
pause

:: 新窗口启动 /k 不关闭窗口 /c 关闭窗口
start cmd /k "c: && cd C:\Project\test-app-1 && npm start"
:: 新窗口延迟 5 秒启动 test-app-2, 
start cmd /k "timeout -nobreak 5 && c: && cd C:\Project\test-app-2 && npm start"
:: 获取管理员权限
runas /user:administrator cmd
:: 判断文件是否存在
if exist %SourceFile% (
    if not exist %GenFile1% (
) else (
    //你要做的事情
) 


netsh -c interface ip dump
netsh interface ip show config
netsh interface ip set address "本地连接" static 37.136.6.210 255.255.255.0 37.136.6.254 1  rem 设置网卡IP 掩码 网关
netsh interface set interface "本地连接" disabled rem 禁用网卡
netsh interface set interface "本地连接" enabled  rem 启用网卡
ncpa.cpl
::Usage：第一条命令 | 第二条命令 [| 第三条命令...]将第一条命令的结果作为第二条命令的参数来使用，记得在unix中这种方式很常见。
::Usage：第一条命令 || 第二条命令 [|| 第三条命令...]用这种方法可以同时执行多条命令，当碰到执行正确的命令后将不执行后面的命令，如果没有出现正确的命令则一直执行完所有命令；
::Usage：第一条命令 & 第二条命令 [& 第三条命令...]用这种方法可以同时执行多条命令，而不管命令是否执行成功
::Usage：第一条命令 && 第二条命令 [&& 第三条命令...]用这种方法可以同时执行多条命令，当碰到执行出错的命令后将不执行后面的命令，如果一直没有出错则一直执行完所有命令；
--------------------------------------------------一秒一个ping输出，超时5秒输出一个“请求超时。”#两个echo一个输出屏幕一个输出到文件
@echo off 
cd C:\Windows\System32
set host=172.20.123.231
set logfile=D:\ping_%host%.log
if exist %logfile% (
    del %logfile%
)
:loop
for /f "tokens=* skip=2" %%A in ('ping %host% -n 1') do (
    echo %date:~0,-3% %time:~0,-3% %%A >> %logfile%
    echo %date:~0,-3% %time:~0,-3% %%A
    timeout /t 1 /nobreak > nul
    goto loop
)
--------------------------------------------------添加服务 或 NSSM安装服务 https://nssm.cc/
sc create 服务名 binPath= "C:\win32srvDemo.exe"
sc config 服务名 start=AUTO   rem AUTO(自动)DEMAND(手动)DISABLED(禁用)
sc description Redis6.2.6 "This service runs the Redis server"



