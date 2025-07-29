REM @echo off
echo 3秒后计算机进入睡眠状态...
echo 请确保已保存所有工作。
timeout /t 3 /nobreak >nul

:: 使用PowerShell方法
powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)"

:: 备用方法（取消注释使用）
:: rundll32.exe powrprof.dll,SetSuspendState 0,1,0

echo 命令已执行。