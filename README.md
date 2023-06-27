## 2022/12/14 项目完结

接学校通知，即日起健康打卡正式取消。

本项目历经2022-09-17至2022-12-14共88天正式完结🎉，感谢各位同学的star、fork和使用。

感谢党和政府为保护我们所做的一切，感谢学校为我们提供一个安全、健康的学习环境。

愿疫情退散，祝身体健康！

<div align="center">
 <h1 align="center">北京工业大学自动健康打卡</h1>
 
 ![](https://img.shields.io/badge/Author-sw1128-red) 
 ![](https://img.shields.io/github/forks/sw1128/bjut_auto_clock) 
 ![](https://img.shields.io/github/stars/sw1128/bjut_auto_clock?color=green)
</div>

## 目录
[1. 更新日志](#更新日志)

[2. 项目介绍](#xmjs)

[3. 注意](#zy)

[4. 项目功能](#xmgn)

[5. 使用方法](#syff)

## 更新日志
### 2022/12/10 更新
打卡项更新，获取打卡项方法请查看 [Wiki](../../wiki)
### 2022/11/16 更新
健康打卡系统更新，删除和新增了一些打卡项。
### 2022/11/11 更新
无更新，光棍节快乐(doge)
### 2022/10/01 更新
健康打卡系统更新，删除和新增了一些打卡项。

## <span id="xmjs">✨ 项目介绍</span>

&emsp;&emsp;随着疫情的到来，鉴于学校这种人员较多的地方容易引发聚集性疫情，因此学校开始实行每日健康打卡制度，这是学校出于全面了解学生和教职工的防疫状况、保证学生健康安全的一项重要举措，然而在实际的执行过程中，有些同学会受到一些不可避免的情况的干扰，导致打不上卡或者忘记打卡，给自己和辅导员老师增添了很多麻烦。

&emsp;&emsp;因此本项目旨在帮助学生从每日打卡的重复性工作中解放出来，同时减轻辅导员老师的负担。
## <span id="zy">📢 注意</span>
本项目仅供学习交流使用，请勿进行其他用途，使用本项目所造成的一切后果与本人无关。
## <span id="xmgn">🎄 项目功能</sapn>

✅ 自动生成一次性code，返回JWT Token

✅ 实现每日指定时间自动打卡

✅ 打卡成功后发送邮件通知

✅ 多人打卡配置

## <span id="syff">🔔 使用方法</sapn>
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

5. 触发器配置选”自定义创建“，然后选自定义触发周期，自己写cron表达式，例如每天的0点10分和6点10分打卡，就写`0 10 0,6 * * * *`，之后若要停止打卡，只需要在触发管理中停用触发器即可

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock8.jpg)

6. 点击完成创建函数

### 配置代码

1. 点开刚刚创建的函数，在index.py文件同目录下创建user.json和items.json文件，然后复制项目中对应文件的代码并粘贴

![](https://zwhy-1310134253.cos.ap-beijing.myqcloud.com/clock9.jpg)

👇 特别注意 👇

2. 打卡项在`clock`函数中配置，需要修改，则可以对照`items.json`中的打卡项id进行修改，通州校区的同学务必修改打卡项第二行的位置和经纬度信息，若今日所在位置想改成京内校外，则将question_id=50那行的`answer_id`改为`115`，添加打卡项和删除打卡项应该不用多讲了吧，对照着上面写就行

　　`获取经纬度`：按F12打开开发者工具，点击网络/Network选项卡，在打卡界面点击获取位置的框，就可以看到一条getCityByLocation?location=XXX的请求，点击负载便可以知道经纬度信息。

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
