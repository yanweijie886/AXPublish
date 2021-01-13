import shutil
import stat
import py7zr
import os
import os.path
import tkinter
import time
from subprocess import call
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


def delete_file(filepath):
    if os.path.exists(filepath):
        for fileList in os.walk(filepath):
            for name in fileList[2]:
                os.chmod(os.path.join(fileList[0], name), stat.S_IWRITE)
                os.remove(os.path.join(fileList[0], name))
        shutil.rmtree(filepath)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "临时文件已删除")
    else:
        print("no filepath")


def print_with_time(content):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), content)


# 压缩文件夹并移动
def compress(file_folder_path, folder_name, tar_dic=os.environ['HOME'] + '/SynologyDrive'):
    cmd = 'display notification \"' + \
          "正在发布，请勿操作" + '\" with title \"发布提醒\"'
    call(["osascript", "-e", cmd])
    if os.path.exists(os.path.join(file_folder_path, folder_name)):
        with py7zr.SevenZipFile(folder_name + '.7z', 'w') as archive:
            print_with_time("开始压缩文件夹")
            archive.writeall(file_folder_path + folder_name, folder_name)
            print_with_time('文件夹压缩成功，文件名称为：' + folder_name)
            if os.path.exists(os.path.join(tar_dic, folder_name + '.7z')):
                os.remove(os.path.join(tar_dic, folder_name + '.7z'))
            shutil.move(folder_name + '.7z', tar_dic)
            delete_file(file_folder_path + folder_name)
            print_with_time('发布成功！')
            cmd = 'display notification \"' + \
                  "发布成功" + '\" with title \"恭喜\"'
            call(["osascript", "-e", cmd])
    else:
        print('文件不存在')
        cmd = 'display notification \"' + \
              "文件不存在" + '\" with title \"发布失败\"'
        call(["osascript", "-e", cmd])


def click(file_folder_path, folder_name, content, x):
    compress(file_folder_path, folder_name)
    if x == 2:
        send_mail(folder_name, content)


path = os.environ['HOME'] + '/Documents/Axure/HTML/'

top = tkinter.Tk()
top.wm_attributes('-topmost', 1)
top.geometry("250x500+750+200")

LANGS = [
    ("不发送更新日志", 1),
    ("发送更新日志", 2)]

v = tkinter.IntVar()
v.set(1)

for lang, num in LANGS:
    b = tkinter.Radiobutton(top, text=lang, variable=v, value=num)
    b.grid(row=num + 3, column=0)

entry = tkinter.Entry(top, width=20)
entry.insert(0, '原型-ERP')
entry.grid(row=0, column=0)

entry2 = tkinter.Entry(top, width=20)
entry2.insert(0, '原型-ERP')
entry2.grid(row=1, column=0)

entry3 = tkinter.Entry(top, width=20)
entry3.insert(0, '原型-ERP')
entry3.grid(row=2, column=0)

te = tkinter.Text(
    top,
    width=20
)
te.insert(index=tkinter.END, chars='更新日志：')
te.grid(row=3, column=0)

B = tkinter.Button(
    top,
    text="发布",
    command=lambda: click(path, entry.get(), te.get('0.0', 'end'), v.get())
).grid(row=0, column=1)

B2 = tkinter.Button(
    top,
    text="发布",
    command=lambda: click(path, entry2.get(), te.get('0.0', 'end'), v.get()),
).grid(row=1, column=1)

B3 = tkinter.Button(
    top,
    text="发布",
    command=lambda: click(path, entry3.get(), te.get('0.0', 'end'), v.get())
).grid(row=2, column=1)

if __name__ == '__main__':
    top.mainloop()
