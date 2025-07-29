@echo off
setlocal enabledelayedexpansion
:: 设置变量
set "host=10.100.255.254"  :: 目标主机IP地址
set "logdir=D:\logs"       :: 日志目录
set "logfile=%logdir%\ping_%host%_%date:~0,4%-%date:~5,2%-%date:~8,2%.log"  :: 日志文件名
set "max_loop=36000"        :: 最大循环次数（防止无限运行）

:: 创建日志目录（如果不存在）
if not exist "%logdir%" (
    mkdir "%logdir%"
)

:: 删除旧的日志文件（如果存在）
if exist "%logfile%" (
    del "%logfile%"
)

:: 初始化计数器
set /a count=0

:loop
:: 检查是否达到最大循环次数
if %count% geq %max_loop% (
    echo [INFO] 达到最大循环次数，脚本自动退出。
    goto end
)

for /f "tokens=* skip=2" %%A in ('ping %host% -n 1') do (
    set "pings=%%A"
    :: 检查 ping 输出是否为空
    if "!pings!"=="" (
        echo [ERROR] ping 输出为空
    ) else (
        echo %date:~0,-3% %time:~0,-3% !pings!
        for /f "tokens=1-5 delims= " %%B in ("!pings!") do (
            REM echo Token1: %%B & echo Token2: %%C & echo Token3: %%D & echo Token4: %%E & echo Token5: %%F
            :: 提取数字
            for /f "tokens=2 delims==" %%v in ("%%F") do (
                set "time_ms=%%v"
            )
            :: 从"time=15ms"中进一步提取纯数字部分
            for /f "tokens=1 delims=ms" %%n in ("%time_ms%") do (
                if %%n geq 10 (
                    echo %date:~0,-3% %time:~0,-3% !pings! >> %logfile%
                    echo !pings!
                )
            )

        )
        REM echo %date:~0,-3% %time:~0,-3% %%A
        timeout /t 1 /nobreak > nul
        set /a count+=1
    )
    goto loop
)

:end
echo [INFO] 脚本运行结束。
pause