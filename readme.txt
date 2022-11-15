Step 1
安装 anaconda
安装 Google Chrome
打开 anaconda navigator
Conda install python=3.7
Conda install pip=20.0
pip install selenium
打开 ticket_order.py

Step 2
- 查找Google Chrome路径,输入网址⬇️
chrome://version
例子：
(1) Mastaffs
C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
(2) Mac
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


打开powershell/cmd
cd path (found in step2)
.\chrome.exe --remote-debugging-port=9222 --user-data-dir=“一个自己设定的路径例如 D:\autoticket\9222” 

Step 3
- python ticket_order.py


