from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
import datetime
import random


# 抢票目标页
# target_url="https://www.polyt.cn/#/detail?productId=4766000"
# target_url="https://www.polyt.cn/#/detail?productId=4708600" #王者荣耀

# 矛盾
# price = 5
# target_url = 'https://www.polyt.cn/#/detail?productId=4398400' #人世间

# 红楼梦
# target_url = 'https://www.polyt.cn/#/detail?productId=4724800'
#
# 日出
target_url = 'https://www.polyt.cn/#/detail?productId=4294100' 

# 猫 有滑块
# target_url = 'https://www.polyt.cn/#/detail?productId=2009300'
# target_url = 'https://www.polyt.cn/#/detail?productId=4836300'
# target_url = 'https://www.polyt.cn/#/detail?productId=4825100'
# target_url = 'https://www.polyt.cn/#/detail?productId=4847400'


# 即将开票



class Concert(object):

    # 类注释化
    def __init__(self):
        self.date = 1  # 选择那一天，比如有2021-01-01，2021-01-02，2021-01-03可选，想选01-01填1，想选01-02填2
        self.price = [1,2,3,4]  # 买哪一档票，从贵到便宜

        self.total_wait_short = 5   #WebDriverWait总等待时间
        self.refresh_wait_short = 0.3 #WebDriverWait刷新动作的时间

        self.total_wait_long = 10
        self.refresh_wait_long = 0.5

        self.total_wait_time = 5
        self.refresh_wait_time = 0.3

        self.login_user = '13206009560' # 登录账号
        self.login_pw = 'qq123456' # 登录密码

        self.collector = '戴飞飞' # 取票人信息
        self.collector_tel = '13725478253' # 取票人电话号码

        self.num_slide_move = 30
        self.num_click_checkout = 50

        self.need_click = False

        port = 9222 # ???
        chrome_options = Options()
        # chrome_options.page_load_strategy = 'eager' #风险
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")  # 控制当前chrome页面
        self.driver = webdriver.Chrome(options=chrome_options)



    # 模块 - 滑块移动
    def slide_bar_move(self):
        num_move = self.num_slide_move
        # Count number of moving slider
        count = 0
        while count < num_move and len(self.driver.find_elements(By.CLASS_NAME, "nc_wrapper"))>0:
            # print('next tiem')
            count += 1
            try:
                el2 = self.driver.find_element(By.CLASS_NAME, "nc_wrapper") # 获取滑槽长度
                # click slide bar
                print(f'-----> 移动滑块 {count}')
                if len(self.driver.find_elements(By.CLASS_NAME, "errloading"))>0:
                    print('----->     errloading')
                    slider_bar = self.driver.find_element(By.CLASS_NAME, "errloading").click()

                self.driver.find_element(By.CLASS_NAME, "btn_slide")
                slider = self.driver.find_element(By.CLASS_NAME, "btn_slide")
                ActionChains(self.driver).click_and_hold(slider).perform()
                ActionChains(self.driver).move_by_offset(xoffset=el2.size['width']+1, yoffset=0).perform() #向右划260个像素
                # ActionChains(self.driver).release().perform()
            except:
                print('滑块报错')
                pass
        
        print(f"-----> 结束滑框 {count}/{num_move} 次后")


    # 获取目标页面
    def prepare(self):
        while self.driver.title.find('选择座位') == -1:
            locator = (By.CLASS_NAME, "status-text")
            while True:
                try:
                    WebDriverWait(self.driver, 3, 0.1).until(EC.text_to_be_present_in_element(locator,'售票中'))
                    print(f"=> 获取页面成功 {datetime.datetime.now()}")
                    break
                except Exception as e:
                    print(f'----------- 未开始 刷新网页 {datetime.datetime.now()}')
                    self.driver.refresh()
            break

    # 登录账号
    def login(self):
        print("=============== 进入登录环节 ===============")
        while not len(self.driver.find_elements(By.CLASS_NAME, "user-is-login"))>0:  # repeat while not log-in successful
            print("=> 登录账号")
            try:
                # click right upper corner
                login_in_wait = WebDriverWait(self.driver, self.total_wait_short, self.refresh_wait_short).until(
                                                EC.text_to_be_present_in_element((By.CLASS_NAME,"user-no-login"),"登录/注册"))
                login_in_button = self.driver.find_element(By.CLASS_NAME, "user-no-login").click()

                # click from QR code to login by username and password
                login_in_method_wait = WebDriverWait(self.driver, self.total_wait_short, self.refresh_wait_short).until(
                                                EC.text_to_be_present_in_element((By.XPATH,'//div[@id="tab-2"]'),"账号登录"))
                login_in_method = self.driver.find_element(By.XPATH,'//div[@id="tab-2"]').click()

                login_username_input = self.driver.find_element(By.XPATH, '//input[@placeholder="请输入账号（手机号）"]').send_keys(self.login_user)
                login_usertel_input = self.driver.find_element(By.XPATH,'//input[@placeholder="请输入密码"]').send_keys(self.login_pw)

                # repeat click login button for 10 times
                login_count = 0
                while len(self.driver.find_elements(By.XPATH, '//*[@id="pane-2"]/form/div[4]/div/button/span'))>0 and login_count<10:
                    login_in_confirm = self.driver.find_element(By.XPATH, '//*[@id="pane-2"]/form/div[4]/div/button/span').click()
                    time.sleep(0.3)
                    login_count += 1
            except:
                self.driver.refresh()
        print(f'=> 账号登录成功 {datetime.datetime.now()}')


    # 选择日期，进入下一页面
    def choose_ticket(self):
        print("=============== 选择日期 ===============")
        print(f"选择日期 {datetime.datetime.now()}")

        while self.driver.title.find('选择座位') == -1: # or len(self.driver.find_elements(By.XPATH, "//span[contains(text(),'选座购买')]"))>0: # 如果跳转到了订单结算界面就算这步成功了，否则继续执行此步
            try:
                WebDriverWait(self.driver, 3, 0.1).until(EC.presence_of_element_located((By.XPATH, "//div[@class='show-time-list el-col el-col-20']")))
                # choiceTime_list = self.driver.find_elements(By.XPATH,'//div[@class="show-time-list el-col el-col-20"]/button')
                choiceTime_list = self.driver.find_elements(By.XPATH, '//div[contains(@class,"show-time")]/div[2][contains(@class,"show-time-list")]/button')
                print(f"可选日期长度 = {len(choiceTime_list)} ")
                for tt in choiceTime_list:
                    print(tt.text)

                if self.date>len(choiceTime_list):      
                    actualDate = choiceTime_list[0]
                    choiceTime_list[0].click()
                    print("==> 想选的日期不存在，自动选择" + actualDate.text)

                else:
                    choiceTime_list[self.date-1].click()
                    print(f"=> 选择日期 {choiceTime_list[self.date-1].text}")

                # “选座购买” 按钮,是可以直接在until后面加click的
                date_select_but = WebDriverWait(self.driver, 3, 0.1).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="purchase-btn el-row is-justify-center el-row--flex"]/button/span')))
                # date_select_but = WebDriverWait(self.driver, 3, 0.1).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class,"purchase-btn")]')))
                date_select_but.click()
                WebDriverWait(self.driver, 3, 0.1).until(EC.title_contains("选择座位"))

            except:
                pass

        print(f"=> 日期选择成功 {datetime.datetime.now()}")

    
    # 读取座位种类,要修改为随档数来
    def check_price_list(self):
        print("="*30)
        print(f"=> 查看座位种数 {datetime.datetime.now()}")

        while True:  # 当中有耗时的查找座位表动作，用true循环查到再进下一步
            try:
                WebDriverWait(self.driver, self.total_wait_long, self.refresh_wait_long).until(EC.presence_of_element_located((By.CLASS_NAME, "price-list")))
                botLeft_list = self.driver.find_elements(By.CLASS_NAME, "price-list")
                print(f'=> 可选种类数: {len(botLeft_list)}')
            except Exception as e:
                print("=> 找不到座位信息，刷新网页")
                self.driver.refresh()
            # 构建座位颜色列表
            self.price_color_list = []
            for botLeft in botLeft_list:
                seatcolor = botLeft.find_element(By.CLASS_NAME,'price-color').get_attribute('style')
                p1 = re.compile(r'[(](.*?)[)]', re.S)
                color = re.findall(p1, seatcolor)
                self.price_color_list.append(color[0])

            if len(self.price_color_list) <= 0 :
                print("=> 没有可选的票档，刷新")
                self.driver.refresh()
                continue

            break


    def seatSelect(self):
        print("=============== 选择座位 ===============")
        while self.driver.title.find('确认订单') == -1 or len(self.driver.find_elements(By.CLASS_NAME, "seat-price"))>0: 

            """ Find seat list """
            print(f"=> 找可选的位置 {self.price}档 {datetime.datetime.now()}")
            while True:  #当中有耗时的查找座位表动作，用true循环查到再进下一步
                try:
                    WebDriverWait(self.driver, 10, 0.1).until(EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "seat-item")]')))
                    seat_list = None
                    for id in self.price:
                        if not seat_list:
                            seat_list = []
                        seat_list = seat_list + self.driver.find_elements(By.XPATH, f'//li[@style="color: rgb({self.price_color_list[id - 1]});"]')
                    print(f'=> 可选位置个数 {len(seat_list)}')
                    if len(seat_list) == 0:
                        self.driver.refresh()
                        continue
                except Exception as e:
                    print('找不到位置信息，刷新网页')
                    self.driver.refresh()
                    continue

                if len(seat_list) != 0:
                    break

            """ Lock seat """
            random.shuffle(seat_list)
            for seat in seat_list:
                if len(seat.get_attribute('title'))>0:
                    seatid = seat.get_attribute('title')

                    if '实名购票' in seatid:
                        self.need_click = True
                        print('##### 需要点击继续购买')

                    try:
                        #这里的逻辑，点不了就跑下一个去点！
                        seat.click()
                        print('=> 选择座位 ' + seatid)
                    except:
                        print(f"选座失败 253行")
                        continue

                    break

            """ Find right bottom corner """
            if self.driver.title.find("确认订单") == 0:
                continue

            try:
                print('=> 已选座位，等结账框')
                WebDriverWait(self.driver,15,0.3).until(EC.presence_of_element_located((By.CLASS_NAME, "el-drawer__open")))
            except:
                if not self.driver.title.find('确认订单') == 0:
                    print('已选座位，没有结账框，刷新网页!')
                    self.driver.refresh()
                continue

            """ Count times to click buy key """
            print(f"=> 点击结账 {datetime.datetime.now()}")
            buy_but_idx = 0
            while buy_but_idx < self.num_click_checkout and self.driver.title.find('确认订单') == -1:
                buy_but_idx += 1         
                try:
                    # 这里需要添加一个element_to_be_clickable来检测这个按钮是否可以点击了，很快的！
                    WebDriverWait(self.driver, 3, 0.3).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="cart-bottom el-row"]/button/span')))
                    print("输出文本 = " + self.driver.find_element(By.XPATH, '//*[@class="cart-bottom el-row"]/button/span').text)
                    checkout_but = self.driver.find_element(By.XPATH, '//*[@class="cart-bottom el-row"]/button/span').click()
                    WebDriverWait(self.driver, 3, 0.1).until(EC.title_contains("确认订单"))
                    print(f'=> 点击结账 {buy_but_idx}')

                    # 检测温馨提示
                    if self.need_click:
                        WebDriverWait(self.driver, 3, 0.2).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"继续购买")]'),"继续购买"))
                        self.driver.find_element(By.XPATH, '//span[contains(text(),"继续购买")]').click()
                        print(f'-----> 点击 继续购买 {datetime.datetime.now()}')
                except:
                    print(buy_but_idx)
                    pass

                # 检测滑块
                if len(self.driver.find_elements(By.CLASS_NAME, "nc_wrapper"))>0:
                    print('-----> 需要滑块')
                    self.slide_bar_move()
                    if len(self.driver.find_elements(By.CLASS_NAME, "nc_wrapper"))>0:
                        print('滑太多次，刷新网页')
                        self.driver.refresh()
                        break


    def checkout_by_often_user(self):
        print("=============== 开始付钱啦 ===============")
        while self.driver.title.find('订单支付') == -1:
            try:
                take_ticket = WebDriverWait(self.driver, self.total_wait_short, self.refresh_wait_short).until(
                            EC.text_to_be_present_in_element((By.CLASS_NAME,"tab-title"),"取票方式"))

                print(f"=> 进入摇人阶段 {datetime.datetime.now()}" )

                audience = WebDriverWait(self.driver, self.total_wait_short, self.refresh_wait_short).until(
                            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="请输入取票人姓名"]')))

                username_input = self.driver.find_element(By.XPATH, '//input[@placeholder="请输入取票人姓名"]')
                usertel_input = self.driver.find_element(By.XPATH,'//input[@placeholder="请输入取票人手机号码"]')
                username_input.clear() #清除原有信息
                usertel_input.clear()
                username_input.send_keys(self.collector) #输入取票人
                usertel_input.send_keys(self.collector_tel)

                payment_choice_click = self.driver.find_element(By.XPATH, '//img[@src="https://res.polyt.cn/ptpc-web/img/icon-payment-weixin.e0a5ad38.png"]').click() #选择付款方式
                # 这个位置测试了可以选择的支付方式，可以通过1 2 3 4 来进行选择支付方式，怕到时候这个src不对
                # payment_choice_list = self.driver.find_elements(By.XPATH, '//div[contains(@class,"pay-list")]/div') 
                # for pcl in payment_choice_list:
                #     print(pcl)

                # 勾选所有框框
                checked = len(self.driver.find_elements(By.XPATH,"//span[contains(@class, 'el-checkbox__input is-checked')]"))
                checkboxes = self.driver.find_elements(By.CLASS_NAME,'el-checkbox__input')
                print(f'=> 已经勾选 {checked}/{len(checkboxes)}个框')
                if checked < len(checkboxes):
                    # VERSION 1
                    for box in checkboxes:
                        box.click()
                        print('-----> 点击')


            except:
                print('---- 信息填写不进去')
                if self.driver.title.find("选择座位") == 0:
                    break
                continue

            print(f'=> 信息填写完毕,点击支付 {datetime.datetime.now()}')

            while self.driver.title.find('订单支付') == -1:
                try:
                    pay_confirm = WebDriverWait(self.driver, 3, 0.05).until(EC.element_to_be_clickable((By.CLASS_NAME, "pay-confirm")))
                    pay_confirm.click()

                except:
                    continue
                break
            break

        

if __name__ == '__main__':
    startTime = datetime.datetime(2022, 11, 14, 11, 18, 0, 0)  #定时功能：2019-9-25 09:17:07秒开抢
    print('=> 抢票程序还未开始...')

    while datetime.datetime.now() < startTime:
        time.sleep(0.5)
    print('=> 开始进入抢票 %s' % datetime.datetime.now())

    start_time = time.time()
    con = Concert()             #具体如果填写请查看类中的初始化函数
    con.driver.get(target_url)
    con.prepare()               #判别是否进入了售票页面，
    # con.login()                 #登录
    con.choose_ticket()
    con.check_price_list()
    while True:
        loop_start_time = time.time()
        print(f'======> 进入 选座 {datetime.datetime.now()}')
        con.seatSelect()
        print(f'======> 跳出 选座 {datetime.datetime.now()}')
        con.checkout_by_often_user()
        print(f'======> 跳出 确认订单 {datetime.datetime.now()}')
        try:
            WebDriverWait(con.driver, 3, 0.1).until(EC.title_contains("订单支付"))
            print('！！！！！快去付钱')
            break
        except:
            print('======> 重新进入 选座，刷新页面 {datetime.datetime.now()}')
            con.driver.back()

    end_time = time.time() - start_time
    print(f'总耗时{end_time}s')


            

 
        




