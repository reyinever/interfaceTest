import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from config.email_conf import *
from utils.Log import *


def send_mail(html_file_path, mail_content_str):
    mail_host = email_host  # 设置服务器
    mail_user = email_user  # 用户名
    mail_pass = email_pass  # 口令
    sender = email_sender
    receivers = email_receivers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = formataddr(["测试负责人：figure", email_sender])
    message['To'] = ','.join(receivers)
    subject = 'xxx自动化测试报告'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText(mail_content_str, 'plain', 'utf-8'))

    # 构造附件1，传送测试结果的html文件
    att = MIMEText(open(html_file_path, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    file_name = os.path.basename(html_file_path)
    att["Content-Disposition"] = 'attachment; filename="' + '%s' % file_name + '"'
    message.attach(att)

    try:
        smtpObj = smtplib.SMTP(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        info("邮件发送成功")
    except smtplib.SMTPException as e:
        info("Error: 邮件发送失败：%s" % e)
