@echo off
:: ����C�̽ű�
:: ���Թ���ԱȨ�����д˽ű�

echo ��������C�̣����Ժ�...

:: ɾ����ʱ�ļ����е��ļ�
echo ����������ʱ�ļ�...
del /s /q %temp%\*
del /s /q C:\Windows\Temp\*

:: ��ջ���վ
echo ������ջ���վ...
rd /s /q C:\$Recycle.Bin

:: ����ϵͳ����
echo ��������ϵͳ����...
del /s /q C:\Windows\Prefetch\*

:: ʹ�ô�������������ϵͳ�ļ�
echo �������д���������...
cleanmgr /sagerun:1

echo C��������ɣ�
pause