@echo off
:: 设置窗口大小和颜色
mode con cols=30 lines=5 & color 0c
:: 切换到指定目录
D: && cd /A/scrcpy-win64-v3.2

REM adb tcpip 5555
REM adb connect 192.168.3.100:5555

:: 初始化标志变量：是否已在周五执行过提醒
set "friday_alert_done=no"

call :dingding
:: 循环判断当前为12点、12点55、17点30打卡
:start
    :: 获取当前小时和分钟
    for /f "tokens=1,2 delims=: " %%a in ('time /t') do (
        set hour=%%a
        set minute=%%b
    )
    :: 获取当前周几
    for /f %%a in ('powershell -command "$(Get-Date).DayOfWeek"') do set "dayofweek=%%a"
    
    :: 去除前导空格（有些系统格式为 " 9:45 AM"）
    set hour=%hour: =%
    set minute=%minute: =%
    echo 当前时间为：%hour%:%minute% (%dayofweek%)

    :: 判断是否为指定时间点之一
    set "run=no"
    if "%hour%"=="12" if "%minute%"=="00" set run=yes
    if "%hour%"=="12" if "%minute%"=="55" set run=yes
    if "%hour%"=="17" if "%minute%"=="30" set run=yes

    if "%run%"=="yes" (
        echo 时间匹配！正在运行 dingding 子程序...
        call :dingding
    )
    :: 如果是 17:30，额外执行休眠命令,并退出程序
    if "%hour%"=="17" if "%minute%"=="35" (
        powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)"
        exit
    )
    
    :: 判断是否是周五，是否第一次执行，是否下午5点，弹窗提醒写ppt
    if /i "%friday_alert_done%" neq "yes" if /i "%dayofweek%"=="Friday" if "%hour%"=="17" (
        msg * "今天是星期五！记得写ppt哦！"
        set "friday_alert_done=yes"
    )
        
    :: 等待 50 秒后再次检查
    timeout /t 50 /nobreak >nul
    cls
goto :start

:: 钉钉打卡
:dingding
    :: 执行流程函数-清理后台任务
    REM call :clear_bak_task
    call :back3time

    adb shell monkey -p com.alibaba.android.rimet -c android.intent.category.LAUNCHER 1     rem 打开钉钉：点击钉钉图标
    timeout /t 2 /nobreak

    call :clink_t_x_y 5 752 381     rem 横标签打卡：点击横标签打卡位置
    call :clink_t_x_y 1 534 1297    rem 中间打卡：点击中间打卡位置
exit /b

    REM pause                       rem 暂停脚本，等待用户确认

:: 定义一个通用函数，用于模拟屏幕点击操作
:clink_t_x_y
    set delay=%1
    set x=%2
    set y=%3
    adb shell input tap %x% %y%
    timeout /t %delay% /nobreak
exit /b

::返回三次
:back3time
    set count=3
    for /L %%i in (1,1,%count%) do (
        adb shell input keyevent KEYCODE_BACK
        timeout /t 1 /nobreak >nul
    )
exit /b

:: 定义一个流程函数，封装主菜单、多任务、关闭等操作
:clear_bak_task
    adb shell input keyevent KEYCODE_HOME   rem 主菜单：点击主菜单按钮   # 回到主屏幕
    timeout /t 1 /nobreak

    adb shell input keyevent KEYCODE_MENU   rem 多任务：点击多任务按钮   # 菜单键
    timeout /t 1 /nobreak

    call :tap_screen 1 542 1880             rem 关闭：关闭当前应用
exit /b


