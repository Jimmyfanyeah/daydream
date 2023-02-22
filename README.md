# daydream
get ticket for

### 2022-11-10 抢票时发现的问题
- [x] 梳理现在的逻辑
- [x] 演出时间选择方法（原先：筛选关键词“星期”）
- [x] 选座时选择多种价位
- [x] 选一个座位失败后，需要刷新页面再选

### 其他有可能性的问题
- [ ] 爬取javascript


## Executing program
### Step 1
- 安装 [anaconda](https://www.anaconda.com)
- 安装 [Google Chorme](https://www.google.com/intl/zh-CN/chrome/)
- 打开 anaconda navigator / terminal, set up the environment for running codes using Conda
```
conda install python=3.7
conda install pip=20.0
pip install selenium
```
- 打开 ticket_order.py

### Step 2
- 查找Google Chrome路径,输入网址: chrome://version，例如
(1) Mastaffs
C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
(2) Mac
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

打开powershell/cmd or terminal
- 打开google chrom port 9222 website
```
cd path (found in step2)
.\chrome.exe --remote-debugging-port=9222 --user-data-dir=“一个自己设定的路径例如 D:\autoticket\9222”
```
- 自己扫码登陆保利票务
- 修改一些参数
    - line 414: 修改抢票时间
    - line 36: 修改抢票链接
    - line 43&44: 修改票的日期和价位
    - line 58-64: 修改取票人和手机号为真实的(line 63&64),把测试用的(line 59&60)注释掉

run the programe:
```
python ticket_order.py
```
