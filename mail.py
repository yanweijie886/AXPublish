import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_mail(folder_name, content):
    # 第三方 SMTP 服务
    mail_host = "hwhzsmtp.qiye.163.com"  # 设置服务器
    mail_user = "weijie.yan@dessmann.com.cn"  # 用户名
    mail_pass = "fyS-m3v-CK8-k9c"  # 密码

    sender = 'weijie.yan@dessmann.com.cn'
    receivers = ['15329885@qq.com', '2656062151@qq.com', 'kaige.chen@dessmann.com.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message = MIMEText('原型地址：http://192.168.30.55/HTML/' + folder_name + '\r\n' + content, 'plain', 'utf-8')
    message['From'] = Header(sender, 'utf-8')
    message['To'] = Header("所有人", 'utf-8')

    subject = folder_name + '更新日志'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")