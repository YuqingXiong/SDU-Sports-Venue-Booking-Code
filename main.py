from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from PIL import Image
import ddddocr
import schedule
import time

get_time = 0

options = Options()
# options.add_argument('--headless')  # 设置chrome浏览器无界面模式

# 调起浏览器，打开网页
url = "https://scenter.sdu.edu.cn/tp_fp/view?m=fp#act=fp/formHome"

# 用于定位登录
pos1 = '//*[@id="un"]'
pos2 = '//*[@id="pd"]'
pos3 = '//*[@id="index_login_btn"]'
username = 'xxxxxxxxx'  # 学号
password = 'xxxxxxxxx'  # 密码

# 想要的时间
play_time = ["8:00-9:30", ]


def main():
    global get_time
    driver = webdriver.Chrome(options=options)
    driver.get(url)
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
    area_li = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div/button")
    area_li.click()

    for i in range(1, area_list_len):
        # 获取时间列表
        time_list = []
        while True:
            try:
                # 点击场地列表
                area_li = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div/button")
                area_li.click()
                driver.implicitly_wait(1)
                area_list = driver.find_element_by_xpath(
                    "/html/body/div[1]/div[3]/div[2]/div/div/ul").find_elements_by_xpath('li')
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
        driver.switch_to.parent_frame()  # 返回上一级
        driver.find_element_by_id("commit").click()
        # 获取验证码图像
        img_code = driver.find_element_by_class_name("ide_code_image")
        print("验证码的坐标为：", img_code.location)  # 控制台查看
        print("验证码的大小为：", img_code.size)  # 图片大小
        left = img_code.location['x']  # x点的坐标
        top = img_code.location['y']  # y点的坐标
        right = img_code.size['width'] + left  # 上面右边点的坐标
        down = img_code.size['height'] + top  # 下面右边点的坐标
        # 页面截图
        driver.save_screenshot("./image.png")  # 可以修改保存地址
        image = Image.open('./image.png')
        # (4)将图片验证码截取
        code_image = image.crop((left, top, right, down))
        code_image.save('./image.png')  # 截取的验证码图片保存为新的文件
        ocr = ddddocr.DdddOcr()
        with open(r'./image.png', 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)
        print("验证码识别结果：", res)
        driver.find_element_by_id("applyCode").send_keys(str(res))
        # 点击确定
        driver.find_element_by_id("fp_apply_code_apply")
        driver.quit()


schedule.every().day.at("09：00").do(main)  # 每天九点执行

while True:
    schedule.run_pending()
    if get_time:
        break
    time.sleep(5)
