::大多数 Windows 外部命令（如 dir, ping, ipconfig 等）不区分大小写
::默认编码格式为ANSI代表 GB2312 编码。
::不加@时，在运行时，会在窗口显示出这条命令,而加了@, 只会显示出 echo后面你要显示出的东西
mode con cols=80 lines=20&color 0c  rem  cols宽 lines高  cmd里面键入:help color 查查看
TITLE Tomcat                        rem  设置窗口标题
cmdow @ /top /mov 500 500           rem  移动窗口到某个位置 详见cmdow下载 https://github.com/ritchielawrence/cmdow/releases/tag/v1.4.8  将 cmdow.exe 文件复制到 C:\Windows\System32
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
timeout /t 10 /nobreak              rem 睡眠10s   /NOBREAK        忽略按键并等待指定的时间（延时期间，不允许用户按任意键终端延时）。
timeout /t 10 /nobreak >nul         rem 控制台不会输出倒计时
timeout /t 10 /nobreak >nul 2>&1    rem 既不想看到正常输出也不想看到错误信息  2>&1 发生错误也不输出
-------------------------------------------判断执行哪一步
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

-------------------------------------------函数运行环境设置
:: 设置一个全局变量
set globalVar=这是全局变量的值

:: 开始局部环境
setlocal
:: 修改全局变量
set globalVar=这是局部环境中的新值
echo 在局部环境中: globalVar=%globalVar%

:: 结束局部环境
endlocal

:: 检查全局变量的值是否恢复
echo 在局部环境外: globalVar=%globalVar%

:: 输出
:: 在局部环境中: globalVar=这是局部环境中的新值
:: 在局部环境外: globalVar=这是全局变量的值
-------------------------------------------函数
:: 调用函数 后面要跟exit /b，不然进入递归
call :tap_screen 1 534 1297
call :tap_screen 1 534 1297
exit /b

:: 声明函数
:tap_screen
    set delay=%1
    set x=%2
    set y=%3
    echo %delay% %x% %y%
exit /b
-------------------------------------------变量声明
set a=aa1bb1aa2bb2
@echo %a%
set b=12
@echo %b%
set /a c=39/10    rem 整数除法       
@echo %c%

-------------------------------------------循环
for  %%I in (A,B,C) do echo %%I     

for /f "skip=1 tokens=9 delims= " %a in ('ping 172.20.123.231') do @echo %a
skip=1 #忽略第一行，默认显示所有行
tokens=9 #显示第9列 类似于awk的 参数$9
delims= #分隔符 本次分隔符为一个空格
ping 172.20.123.231 #循环该命令所有行
pause

-------------------------------------------新窗口启动
:: 新窗口启动 /k 执行完指定的命令后，不关闭命令提示符窗口。 /c 执行完指定的命令后，关闭命令提示符窗口。 /b 立即启动任务而不创建新的窗口。
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
--------------------------------------------------【NirCmd】修改文件的创建时间与修改时间
打开下拉到最下面下载  https://www.nirsoft.net/utils/nircmd.html  

nircmd.exe setfiletime "D://1.txt" "24-06-2003 17:57:11" "22-11-2005 10:21:56"

-------------cmd要以管理员运行----------【添加服务 或 NSSM安装服务 https://nssm.cc/】
sc create frp_service binPath= "D:\AAA\frp_0.57.0_windows_amd64\frpc.exe -c D:\AAA\frp_0.57.0_windows_amd64\frpc.toml"
sc config frp_service start=AUTO    rem AUTO(自动)DEMAND(手动)DISABLED(禁用)
sc description frp_service "This service runs the frp client"

net start MyFRPService      rem 启动服务
sc query MyFRPService       rem 查看启动是否启动成功
net stop MyFRPService       rem 停止服务
sc delete MyFRPService      rem 删除服务



sc config MyService start= [auto| demand | disabled | boot | system] rem auto：在系统启动时自动启动。demand：被标记为手动启动，即需要手动启动服务。disabled：服务被禁用，不会自动启动，也无法手动启动。boot：在系统引导时启动。system：在系统初始化时启动。
sc config MyService binPath= [PathToExecutable]                      rem 指定服务的可执行文件的路径。
sc config MyService obj= [UserOrGroup]                               rem 指定服务运行时所使用的用户或组帐户。
sc config MyService tagBits= [TagBits]                               rem 设置服务的标签位。
sc config MyService display= [DisplayName]                           rem 设置服务的显示名称。
sc config MyService error= [normal| severe| critical| ignore]        rem 设置服务失败时的系统反应。normal：默认动作。severe：严重错误。critical：致命错误。ignore：忽略错误。
sc config MyService group= [LoadOrderGroup]                          rem 设置服务的加载顺序组。
sc config MyService depend= [DependentServiceNames]                  rem 设置服务依赖的其他服务名称。
sc config MyService Type= [ownShare| share| interact| kernel| kernelDriver| fileSystemDriver] rem ownShare：服务拥有自己的进程空间。share：服务与其他服务共享进程空间。interact：服务可以与桌面交互。kernel：内核驱动程序。kernelDriver：内核驱动程序。fileSystemDriver：文件系统驱动程序。

下载https://nssm.cc/，解压之后管理员身份启动cmd切换到解压目录
nssm install FrpService "D:\AAA\frp_0.57.0_windows_amd64\frpc.exe" -c "D:\AAA\frp_0.57.0_windows_amd64\frpc.toml"

NSSM: The non-sucking service manager
Version 2.24 64-bit, 2014-08-31
Usage: nssm <option> [<args> ...]

To show service installation GUI:
        nssm install [<servicename>]
To install a service without confirmation:
        nssm install <servicename> <app> [<args> ...]
To show service editing GUI:
        nssm edit <servicename>
To retrieve or edit service parameters directly:
        nssm get <servicename> <parameter> [<subparameter>]
        nssm set <servicename> <parameter> [<subparameter>] <value>
        nssm reset <servicename> <parameter> [<subparameter>]
To show service removal GUI:
        nssm remove [<servicename>]
To remove a service without confirmation:
        nssm remove <servicename> confirm
To manage a service:
        nssm start <servicename>
        nssm stop <servicename>
        nssm restart <servicename>
        nssm status <servicename>
        nssm rotate <servicename>














