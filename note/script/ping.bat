@echo off
setlocal enabledelayedexpansion
:: ���ñ���
set "host=10.100.255.254"  :: Ŀ������IP��ַ
set "logdir=D:\logs"       :: ��־Ŀ¼
set "logfile=%logdir%\ping_%host%_%date:~0,4%-%date:~5,2%-%date:~8,2%.log"  :: ��־�ļ���
set "max_loop=36000"        :: ���ѭ����������ֹ�������У�

:: ������־Ŀ¼����������ڣ�
if not exist "%logdir%" (
    mkdir "%logdir%"
)

:: ɾ���ɵ���־�ļ���������ڣ�
if exist "%logfile%" (
    del "%logfile%"
)

:: ��ʼ��������
set /a count=0

:loop
:: ����Ƿ�ﵽ���ѭ������
if %count% geq %max_loop% (
    echo [INFO] �ﵽ���ѭ���������ű��Զ��˳���
    goto end
)

for /f "tokens=* skip=2" %%A in ('ping %host% -n 1') do (
    set "pings=%%A"
    :: ��� ping ����Ƿ�Ϊ��
    if "!pings!"=="" (
        echo [ERROR] ping ���Ϊ��
    ) else (
        echo %date:~0,-3% %time:~0,-3% !pings!
        for /f "tokens=1-5 delims= " %%B in ("!pings!") do (
            REM echo Token1: %%B & echo Token2: %%C & echo Token3: %%D & echo Token4: %%E & echo Token5: %%F
            :: ��ȡ����
            for /f "tokens=2 delims==" %%v in ("%%F") do (
                set "time_ms=%%v"
            )
            :: ��"time=15ms"�н�һ����ȡ�����ֲ���
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
echo [INFO] �ű����н�����
pause