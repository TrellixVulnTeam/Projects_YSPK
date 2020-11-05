@ECHO OFF

echo "Bot Docs B 'CodeHelper' Installer Windows 64 Bit"
echo "Installing all needed tools for just installing the extension use the other batch file"
echo "Needs to Restart after installing the tools with this batch file"
echo "Please check the box with the 'set to windows PATH' otherwise this installer will fail"
echo

echo "Installing Python3..."
CD python-3.8.1-amd64
START /W python-3.8.1-amd64.exe
CD ..
echo "python3 installed"
echo

echo "Installing Python3 Libraries..."
SET libs=(requests sys os beautifulsoup4 numpy sklearn2 scikit-learn scipy nltk)
(FOR %%a in %libs% DO (
	echo "Installing Python Library %%a"
	py -3 -m pip install %%a
))
echo "Installed all Python3 Libraries"
echo

echo "Installing Nltk Data ..."
SET data=(stopwords averaged_perceptron_tagger)
(FOR %%a in %data% DO (
	echo "Installing %%a Data"
	py -3 -m nltk.downloader %%a
))
echo "Installed all Nltk Data"
echo

echo "Installing VS Code..."
CD vscode
START /W VSCodeUserSetup-x64-1.42.1.exe
CD ..
echo "Installed VS code"
echo

echo "Installing Node JS..."
CD nodejs
START /W node-v12.16.0-x64.msi
CD ..
echo "Installed Node JS"
echo

echo "please Restart the PC and run the other batch file to complete the installation process" 
echo

PAUSE