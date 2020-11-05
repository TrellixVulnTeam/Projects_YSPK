@ECHO OFF

echo "Bot Docs B 'CodeHelper' Installer Windows 64 Bit"
echo "Installing the vscode extension, please run this file after you run the other batch file and restarted your PC"
echo "or if you have, python3/vs code and nodejs already installed otherwise this installer will fail"
echo

echo "Installing VS Code Extenstion 'CodeHelper'..."
xcopy "codehelper" "%USERPROFILE%" /s /h /e /k /f /c
cd "%USERPROFILE%\codehelper"
code .
echo "Installed VS Code Extenstion 'CodeHelper'"

PAUSE