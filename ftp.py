#!/usr/bin/env python
# coding:utf-8

import os
import ftplib
import time

today = time.strftime('%Y%m%d', time.localtime(time.time()))
ip = '111.111.111.6'
username = 'ftpUserName'
password = 'ftpPassWord'
filename = '203200189' + today + 'A001.tar.gz'
src_file = '/ftpFilePath/' + filename


class MyFtp:
    ftp = ftplib.FTP()
    ftp.set_pasv(False)

    def __init__(self, host, port=21):
        self.ftp.connect(host, port)

    def login(self, user, passwd):
        self.ftp.login(user, passwd)

        print(self.ftp.welcome)

    def download_file(self, local_file, remote_file):  # 下载指定目录下的指定文件
        file_handler = open(local_file, 'wb')

        print(file_handler)
        # self.ftp.retrbinary("RETR %s" % (remote_file), file_handler.write)#接收服务器上文件并写入本地文件
        self.ftp.retrbinary('RETR ' + remote_file, file_handler.write)
        file_handler.close()
        return True

    def download_file_tree(self, local_dir, remote_dir):  # 下载整个目录下的文件
        print("remote_dir:", remote_dir)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
            self.ftp.cwd(remote_dir)
            remote_names = self.ftp.nlst()
            print("remote_names", remote_names)
            for file in remote_names:
                local = os.path.join(local_dir, file)
                print(self.ftp.nlst(file))
                if file.find(".") == -1:
                    if not os.path.exists(local):
                        os.makedirs(local)
                        self.download_file_tree(local, file)
                    else:
                        self.download_file(local, file)
                        self.ftp.cwd("..")
            return True

    # 从本地上传文件到ftp
    def upload_file(self, remote_path, local_path):
        bufsize = 1024
        fp = open(local_path, 'rb')
        self.ftp.storbinary('STOR ' + remote_path, fp, bufsize)
        self.ftp.set_debuglevel(0)
        fp.close()

    def close(self):
        self.ftp.quit()


if __name__ == "__main__":
    ftp = MyFtp(ip)
    ftp.login(username, password)
    ftp.download_file(filename, src_file)
    # ftp.download_file_tree('.', '/cteidate/')
    ftp.close()
    print("ok!")
