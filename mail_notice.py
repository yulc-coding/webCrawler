import smtplib
from email.mime.text import MIMEText

"""异常发送邮件通知"""

# 发送者账号
SEND_USER = "vipyulichao@sina.com"
# 发送者密码
SEND_PWD = "5794f5eddda2da1e"
# 邮箱接收人地址，多个账号以逗号隔开
RECEIVE = "mr.yulichao@foxmail.com"


def send_mail(title, content, mail_host='smtp.sina.com', ssl_port=465):
    """
    发送邮件函数，阿里云默认禁用25端口，所以用SSL方式发送
    :param title: 邮件标题
    :param content: 邮件内容
    :param mail_host: 邮箱服务器
    :param ssl_port: SSL端口号
    :return:
    """
    print("开始发送<<<<<<")
    # 邮件内容
    msg = MIMEText(content)
    # 邮件主题
    msg['Subject'] = title
    # 发送者账号
    msg['From'] = SEND_USER
    # 接收者账号列表
    msg['To'] = RECEIVE
    # 连接邮箱，传入邮箱地址，和端口号
    smtp = smtplib.SMTP_SSL(mail_host, port=ssl_port)
    # 发送者的邮箱账号，密码
    smtp.login(SEND_USER, SEND_PWD)
    # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
    smtp.sendmail(SEND_USER, RECEIVE, msg.as_string())
    smtp.quit()  # 发送完毕后退出smtp
    print("发送完毕>>>>>>>")
