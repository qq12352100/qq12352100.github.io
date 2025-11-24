@echo off
:: 设置窗口大小和颜色
mode con cols=30 lines=5 & color 0c
cmdow @ /top /mov 1000 10
:: 切换到指定目录
D:/A/scrcpy-win64-v3.3.1/scrcpy.exe
REM pause