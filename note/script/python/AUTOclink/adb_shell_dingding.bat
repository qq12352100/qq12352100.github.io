@echo off
:: ���ô��ڴ�С����ɫ
mode con cols=30 lines=5 & color 0c
:: �л���ָ��Ŀ¼
D: && cd /A/scrcpy-win64-v3.2

REM adb tcpip 5555
REM adb connect 192.168.3.100:5555

:: ��ʼ����־�������Ƿ���������ִ�й�����
set "friday_alert_done=no"

call :dingding
:: ѭ���жϵ�ǰΪ12�㡢12��55��17��30��
:start
    :: ��ȡ��ǰСʱ�ͷ���
    for /f "tokens=1,2 delims=: " %%a in ('time /t') do (
        set hour=%%a
        set minute=%%b
    )
    :: ��ȡ��ǰ�ܼ�
    for /f %%a in ('powershell -command "$(Get-Date).DayOfWeek"') do set "dayofweek=%%a"
    
    :: ȥ��ǰ���ո���Щϵͳ��ʽΪ " 9:45 AM"��
    set hour=%hour: =%
    set minute=%minute: =%
    echo ��ǰʱ��Ϊ��%hour%:%minute% (%dayofweek%)

    :: �ж��Ƿ�Ϊָ��ʱ���֮һ
    set "run=no"
    if "%hour%"=="12" if "%minute%"=="00" set run=yes
    if "%hour%"=="12" if "%minute%"=="55" set run=yes
    if "%hour%"=="17" if "%minute%"=="30" set run=yes

    if "%run%"=="yes" (
        echo ʱ��ƥ�䣡�������� dingding �ӳ���...
        call :dingding
    )
    :: ����� 17:30������ִ����������,���˳�����
    if "%hour%"=="17" if "%minute%"=="35" (
        powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)"
        exit
    )
    
    :: �ж��Ƿ������壬�Ƿ��һ��ִ�У��Ƿ�����5�㣬��������дppt
    if /i "%friday_alert_done%" neq "yes" if /i "%dayofweek%"=="Friday" if "%hour%"=="17" (
        msg * "�����������壡�ǵ�дpptŶ��"
        set "friday_alert_done=yes"
    )
        
    :: �ȴ� 50 ����ٴμ��
    timeout /t 50 /nobreak >nul
    cls
goto :start

:: ������
:dingding
    :: ִ�����̺���-�����̨����
    REM call :clear_bak_task
    call :back3time

    adb shell monkey -p com.alibaba.android.rimet -c android.intent.category.LAUNCHER 1     rem �򿪶������������ͼ��
    timeout /t 2 /nobreak

    call :clink_t_x_y 5 752 381     rem ���ǩ�򿨣�������ǩ��λ��
    call :clink_t_x_y 1 534 1297    rem �м�򿨣�����м��λ��
exit /b

    REM pause                       rem ��ͣ�ű����ȴ��û�ȷ��

:: ����һ��ͨ�ú���������ģ����Ļ�������
:clink_t_x_y
    set delay=%1
    set x=%2
    set y=%3
    adb shell input tap %x% %y%
    timeout /t %delay% /nobreak
exit /b

::��������
:back3time
    set count=3
    for /L %%i in (1,1,%count%) do (
        adb shell input keyevent KEYCODE_BACK
        timeout /t 1 /nobreak >nul
    )
exit /b

:: ����һ�����̺�������װ���˵��������񡢹رյȲ���
:clear_bak_task
    adb shell input keyevent KEYCODE_HOME   rem ���˵���������˵���ť   # �ص�����Ļ
    timeout /t 1 /nobreak

    adb shell input keyevent KEYCODE_MENU   rem �����񣺵��������ť   # �˵���
    timeout /t 1 /nobreak

    call :tap_screen 1 542 1880             rem �رգ��رյ�ǰӦ��
exit /b


