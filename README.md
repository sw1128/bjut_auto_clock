# 北京工业大学（BJUT）自动健康打卡

## ✨ 项目介绍
随着疫情的到来，学校规定每天都需要进行健康打卡。本项目旨在帮助学生进行健康打卡，减轻学生的打卡负担。
## 📢 注意
本项目仅供学习交流使用，请勿进行其他用途，使用本软件所造成的一切后果与本人无关。
## 🎄 项目功能

* [x] 自动生成一次性code，返回JWT Token
* [x] 实现每日指定时间自动打卡
* [x] 打卡成功后发送邮件通知
* [x] 多人打卡配置

## 🔔 使用方法
### 获取eai-sess（身份标识）
1.打开浏览器，按F12打开开发者工具，点击网络/Network选项卡

2.输入网址👇，回车
`https://yqfk.bjut.edu.cn/api/login?url_back=pages/index/index`

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock1.jpg)

3.找到`https://itsapp.bjut.edu.cn/uc/api/oauth/index?redirect=http://yqfk.bjut.edu.cn/api/login/pages-index-index?login=1&appid=200220501233430304&state=STATE`请求，如果没有就重新进行第2步

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock2.jpg)

4.查看请求标头的Cookie，复制eai-sess=后面的内容备用

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock3.jpg)

### 配置腾讯云函数

1. 注册腾讯云函数（此处不赘述），新用户注册三个月免费？（貌似），如果没有免费额度，可以学生认证完之后花1块钱买一年资源包

2. 打开函数服务，[新建函数](https://console.cloud.tencent.com/scf/list-create?rid=1&ns=default&createType=empty)，选择”从头开始“，函数名称随意，地域随意，运行环境选择`Python3.6`，函数代码选择”在线编辑“，复制`index.py`的代码，粘贴

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock4.jpg)

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock5.jpg)

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock6_1.jpg)

3. 日志可以启用也可以不启用，启用的话便于排查报错，但是会略微扣费，新用户三个月免费？（貌似）。

4. 高级配置中，执行超时改为`900`秒，其他不用管

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock7.jpg)

5. 触发器配置选”自定义创建“，然后选自定义触发周期，自己写cron表达式，例如每天的0点10分和6点10分打卡，就写`0 10 0,6 * * * *`

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock8.jpg)

6. 点击完成创建函数

### 配置代码

1. 点开刚刚创建的函数，在index.py文件同目录下创建user.json和items.json文件，然后复制项目中对应文件的代码并粘贴

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock9.jpg)

👇 特别注意 👇

2. 打卡项在`clock`函数中配置，需要修改，则可以对照`items.json`中的打卡项id进行修改，通州校区的同学务必修改打卡项第二行的位置和经纬度信息，若今日所在位置想改成京内校外，则将question_id=50那行的`answer_id`改为`115`，添加打卡项和删除打卡项应该不用多讲了吧，对照着上面写就行

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock10.jpg)

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock11.jpg)

#### 配置单人/多人打卡
 
　在user.json中填入eai-sess等信息，其中eai-sess为必填项，多人打卡则按照第一条的模板重复添加即可

#### 配置邮箱推送（以QQ邮箱为例）

　1. 打开QQ邮箱，点击设置-账户-POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务，开启服务：`POP3/SMTP服务`和`IMAP/SMTP服务`，开启成功后点击”生成授权码“，复制授权码填入user.json文件的`email_auth = ""`中
 
![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock12.jpg)

　2. `email_1 = ""`填发送邮件人的邮箱，`email_2 = ""`填自己的邮箱，可以都填自己的

### 运行

确认无误后，点击右上角的”测试“，执行成功后会将打卡结果推送到邮箱

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock13.jpg)

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock14.jpg)

## 如果您遇到问题欢迎提出Issue，如果您觉得有用，请为我点亮star⭐吧
