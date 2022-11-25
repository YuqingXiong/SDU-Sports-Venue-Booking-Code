# SDU-Sports-Venue-Booking-Code

python + Selenium + schedule

# 使用方式

[Selenium 详细教程_CS_Hoyun的博客-CSDN博客_selenium](https://blog.csdn.net/sinat_28631741/article/details/115634230)

1. 下载Chrome 浏览器和Chrome Driver驱动

2. 更改学号和密码，选择想要的时间列表

   注意时间的格式，需要与预约时间相匹配

   ```py
   username = 'studentID'  # 学号,eg:202211111
   password = 'password'   # 密码，eg:sduxyqxxx
   
   # 想要的时间
   play_time = ["8:00-9:30", ]
   ```

3. 设置运行的时间

   ```py
   schedule.every().day.at("9:00").do(main)  # 每天九点执行
   ```

4. 在电脑时间标准下，至少提前比设置时间提前一分钟运行程序