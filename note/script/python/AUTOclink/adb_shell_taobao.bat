@echo off
:: ���ô��ڴ�С����ɫ
mode con cols=80 lines=20 & color 0c

:: �л���ָ��Ŀ¼
D:
cd /A/scrcpy-win64-v3.2

:: ִ�����̺���
call :process_flow

:: �򿪶���������Ա�ͼ��
call :tap_screen 10 412 197

:: ���ǩ�򿨣���ҳ���
call :tap_screen 10 118 392
:: ���ǩ�򿨣���ҳ���-���ǩ��
call :tap_screen 1 540 684

:: ��ͣ�ű����ȴ��û�ȷ��
pause

exit /b

:: ����һ��ͨ�ú���������ģ����Ļ�������
:tap_screen
    set delay=%1
    set x=%2
    set y=%3
    echo %delay% %x% %y%
    adb shell input tap %x% %y%
    timeout /t %delay% /nobreak
exit /b

:: ����һ�����̺�������װ���˵��������񡢹رյȲ���
:process_flow
    :: ���˵���������˵���ť
    call :tap_screen 1 540 2100

    :: �����񣺵��������ť
    call :tap_screen 1 316 2090

    :: �رգ��رյ�ǰӦ��
    call :tap_screen 3 542 1880
exit /b