from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import schedule
import time

get_time = 0

options = Options()
# options.add_argument('--headless')  # 设置chrome浏览器无界面模式

# 调起浏览器，打开网页
url = "https://scenter.sdu.edu.cn/tp_fp/view?m=fp#act=fp/formHome"
driver = webdriver.Chrome(options=options)
driver.get(url)

# 用于定位登录
pos1 = '//*[@id="un"]'
pos2 = '//*[@id="pd"]'
pos3 = '//*[@id="index_login_btn"]'
username = 'studentID'  # 学号,eg:202211111
password = 'password'   # 密码，eg:sduxyqxxx

# 想要的时间
play_time = ["8:00-9:30", ]


def main():
    global get_time
    actions = ActionChains(driver)
    # 学生登录
    driver.find_element_by_xpath(pos1).clear()
    driver.find_element_by_xpath(pos1).send_keys(username)
    driver.find_element_by_xpath(pos2).clear()
    driver.find_element_by_xpath(pos2).send_keys(password)
    driver.find_element_by_xpath(pos3).click()
    actions.perform()
    driver.switch_to.window(driver.window_handles[-1])
    driver.implicitly_wait(1)

    # 打开教务教学
    pos4 = '//a[@vid="1079350034432"]'
    # 打开青岛校区风雨操场页面
    pos5 = '//span[@title="青岛校区风雨操场预约"]'
    while True:
        try:
            teach = driver.find_element_by_xpath(pos4)
            teach.click()
            book_span = driver.find_element_by_xpath(pos5)
            book_span.click()
            break
        except:
            driver.implicitly_wait(1)

    # 切换到内嵌网页
    while True:
        try:
            driver.switch_to.frame("formIframe")
            break
        except:
            driver.implicitly_wait(1)

    # 点击选择最后一个日期
    date_list = []
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/button").click()
            date_list = driver.find_element_by_xpath(
                "/html/body/div[1]/div[2]/div[2]/div/div/ul").find_elements_by_xpath('li')
            break
        except:
            driver.implicitly_wait(0.5)
    date_list[-1].click()
    print("date_list ========== ", len(date_list))
    # 获取场地列表
    area_list = []
    driver.implicitly_wait(1)
    while True:
        try:
            area_li = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div/button")
            area_li.click()
            area_list = driver.find_element_by_xpath(
                "/html/body/div[1]/div[3]/div[2]/div/div/ul").find_elements_by_xpath('li')
            print("area list while len ========== ", len(area_list))
            if len(area_list) > 1:
                break
        except:
            driver.implicitly_wait(0.5)
    area_list_len = len(area_list)
    print("area_list_len ========== ", area_list_len)

    for i in range(1, area_list_len):
        # 获取时间列表
        time_list = []
        while True:
            try:
                # 点击场地列表
                driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div/button").click()
                driver.implicitly_wait(0.5)
                area_list[i].click()
                driver.implicitly_wait(1)
                # 点击时间列表
                driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[4]/div/button").click()
                time_list = driver.find_element_by_xpath(
                    "/html/body/div[1]/div[3]/div[4]/div/div/ul").find_elements_by_xpath('li')
                print("time list len while ===== ", len(time_list))
                break
            except:
                driver.implicitly_wait(0.5)
        time_list_len = len(time_list)
        print("time_list_len ========== ", time_list_len)
        # 时间列表中匹配目标时间列表
        for j in range(1, time_list_len):
            if time_list[j].text in play_time:
                time_list[j].click()
                get_time = 1
        if get_time:
            break

    if get_time:
        people_boxs = driver.find_elements_by_xpath("//input[@type='checkbox']")
        people_boxs[0].click()  # 选择全选复选框
        # 点击申请按钮
        # driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[13]/div/div[2]/div/div[2]/div/div/div[4]/div/div[2]/div[1]/div/div[3]/div[1]/button").click()
        # driver.quit()


schedule.every().day.at("9:00").do(main)  # 每天九点执行

while True:
    schedule.run_pending()
    if get_time:
        break
