# SDU-Sports-Venue-Booking-Code

python + Selenium + ddddocr + schedule
# 使用方式

# 开发方式

[Selenium 详细教程_CS_Hoyun的博客-CSDN博客_selenium](https://blog.csdn.net/sinat_28631741/article/details/115634230)

## 1.下载Chrome 浏览器和Chrome Driver驱动
查看Chrome浏览器版本
![image](https://xiongyuqing-img.oss-cn-qingdao.aliyuncs.com/blog_img/202212091549831.png)

在网址 http://npm.taobao.org/mirrors/chromedriver/ 中搜索版本号下载对应驱动

![image-20221209154903216](https://xiongyuqing-img.oss-cn-qingdao.aliyuncs.com/blog_img/202212091549344.png)

解压缩到对应环境的python环境中，驱动文件与python.exe同级
## 2.对应环境下载相关库 
`pip install selenium`

`pip install ddddocr `

`pip install schedule`

...

3. 更改学号和密码，选择想要的时间列表

   注意时间的格式，需要与预约时间相匹配

   ```py
   username = 'studentID'  # 学号,eg:202211111
   password = 'password'   # 密码，eg:sduxyqxxx
   
   # 想要的时间
   play_time = ["8:00-9:30", ]
   ```

4. 设置运行的时间

   ```py
   schedule.every().day.at("09:00").do(main)  # 每天九点执行
   ```

5. 在电脑时间标准下，至少提前比设置时间提前一分钟运行程序
