REM @echo off
echo 3�����������˯��״̬...
echo ��ȷ���ѱ������й�����
timeout /t 3 /nobreak >nul

:: ʹ��PowerShell����
powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)"

:: ���÷�����ȡ��ע��ʹ�ã�
:: rundll32.exe powrprof.dll,SetSuspendState 0,1,0

echo ������ִ�С�