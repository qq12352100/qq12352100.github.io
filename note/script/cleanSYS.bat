@echo off
:: 清理C盘脚本
:: 请以管理员权限运行此脚本

echo 正在清理C盘，请稍候...

:: 删除临时文件夹中的文件
echo 正在清理临时文件...
del /s /q %temp%\*
del /s /q C:\Windows\Temp\*

:: 清空回收站
echo 正在清空回收站...
rd /s /q C:\$Recycle.Bin

:: 清理系统缓存
echo 正在清理系统缓存...
del /s /q C:\Windows\Prefetch\*

:: 使用磁盘清理工具清理系统文件
echo 正在运行磁盘清理工具...
cleanmgr /sagerun:1

echo C盘清理完成！
pause