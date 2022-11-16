import time
import datetime
from email.mime.text import MIMEText
import smtplib
import requests
import json

def get_code(eai_sess):
    url = "https://itsapp.bjut.edu.cn/uc/api/oauth/index?redirect=http://yqfk.bjut.edu.cn/api/login/pages-index-index?login=1&appid=200220501233430304&state=STATE HTTP/1.1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Cookie": "eai-sess=" + eai_sess
    }
    response = requests.get(url, headers=headers, verify=False, allow_redirects=False)
    code = response.headers['Location'].split("code=")[1].split("&")[0]
    print("随机生成code：" + code)
    return code

def get_token(code):
    code_url = "https://yqfk.bjut.edu.cn/api/code"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    code_params = {
        "code": code
    }
    response_1 = requests.get(code_url, headers=headers,params=code_params, verify=False)
    token = response_1.json()['token']
    print("token：" + token)
    return token

def get_info(token):
    print("正在获取用户信息...")
    info_url = "https://yqfk.bjut.edu.cn/api/home/user_info"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Authorization": "Bearer " + token
    }
    info = requests.get(info_url, headers=headers, verify=False).json()
    print(info)
    return info

def clock(token):
    clock_data = [
        {"question_id": 48, "answer": {"id": 111, "text": None}},   # 所在地区：中国大陆
        {"question_id": 36, "answer": {"id": 71, "text": "北京市,北京市,朝阳区"}, "location": "116.4793046312184,39.884066537698715"},
        {"question_id": 50, "answer": {"id": 114, "text": None}},   # 京内校内
        {"question_id": 51, "answer": {"id": 119, "text": None}},   # 中蓝校区
        {"question_id": 52, "answer": {"id": 121, "text": None}},   # 住宿舍
        {"question_id": 54, "answer": {"id": 126, "text": None}},   # 是否离校：否
        {"question_id": 56, "answer": {"id": 130, "text": None}},   # 是否离京：否
        {"question_id": 58, "answer": {"id": 134, "text": None}},   # 是否离境：否
        {"question_id": 64, "answer": {"id": 145, "text": None}},   # 低风险地区
        {"question_id": 65, "answer": {"id": 149, "text": None}},   # 体温自测：正常
        {"question_id": 95, "answer": {"id": 252, "text": None}},    # 最近一次核酸结果：阴性
        # 2022/10/01 新增项
        {"question_id": 103, "answer": {"id": 267, "text": None}},  # 7天内是否有本土新冠病毒感染者所在县（市、区、旗）旅居史：否
        {"question_id": 112, "answer": {"id": 280, "text": None}},  # 本人及共同居住者早午晚健康状况：正常
        {"question_id": 114, "answer": {"id": 283, "text": None}},  # 北京健康宝状态：无异常情况
        {"question_id": 115, "answer": {"id": 287, "text": None}},  # 本人及家庭成员、共同居住者是否有以下异常情况：无异常情况
        {"question_id": 117, "answer": {"id": 300, "text": None}},  # 今日是否核酸检测：校内做核酸检测
        # 2022/11/16 新增项
        {"question_id": 123, "answer": {"id": 316, "text": None}},  # 当日健康宝查询核酸几天：1天
        # 2022/11/16 删除项
        # {"question_id": 75, "answer": {"id": 183, "text": None}},   # 是否参加核酸检测：学校全员
        # {"question_id": 93, "answer": {"id": 240, "text": None}},   # 今日健康宝状态：无异常
        # {"question_id": 94, "answer": {"id": 244, "text": None}},   # 今日是否有异常状况：无

    ]
    clock_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Authorization": "Bearer " + token,
    }
    r = requests.post(url="https://yqfk.bjut.edu.cn/api/home/daily_form", json=clock_data, headers=clock_headers, verify=False)
    print(r.status_code)
    print(r.json())
    return r.json()

def send_email(news,email_1,email_2,email_auth):
    print("正在推送到邮箱...")
    msg_from = email_1  
    passwd = email_auth  
    msg_to = email_2 
    subject = "打卡通知"  # 邮件主题
    content = news  # 邮件内容
    msg = MIMEText(content)
    # 放入邮件主题
    msg['Subject'] = subject
    # 放入发件人
    msg['From'] = msg_from
    try:
        # 通过ssl方式发送，服务器地址，端口，qq和网易的有区别，注意修改。
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 登录到邮箱
        s.login(msg_from, passwd)
        # 发送邮件：发送方，收件方，要发送的消息
        s.sendmail(msg_from, msg_to, msg.as_string())
    except s.SMTPException as e:
        print(e)
    finally:
        print("邮件推送成功！")
        s.quit()

def multi_clock(eai_sess,email_1,email_2,email_auth):
    code = get_code(eai_sess)
    token = get_token(code)
    info = get_info(token)
    result = clock(token)
    utc8_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    news = f"""
    个人信息：{info["data"]['username']} {info["data"]['depart_name']} {info["data"]['identity']}
    打卡时间：{utc8_time.strftime("%Y-%m-%d %H:%M:%S %p")}
    code：{result['code']}
    打卡结果：{result['message']}
    success：{result['success']}
    error：{result['error']}
    """
    if email_1 and email_2 and email_auth:
        send_email(news,email_1,email_2,email_auth)
    else:
        print("用户未正确配置邮箱推送")
    print("打卡完成！")

def main_handler(event, context):
    with open("user.json", "r", encoding="utf-8") as f:
        user = json.load(f)
    for i in user:
        print("#####用户" + i["name"] + "正在打卡...#####")
        eai_sess = i["eai-sess"]
        email_1 = i["email_1"]
        email_2 = i["email_2"]
        email_auth = i["email_auth"]
        if eai_sess:
            multi_clock(eai_sess,email_1,email_2,email_auth)
            print("等待3秒...")
            time.sleep(3)
        else:
            print("信息不完整，请检查user.json")
