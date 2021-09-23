# coding:utf-8
import shutil
import stat
import py7zr
import os
import os.path
import time
from subprocess import call
import platform
import config.GVC
import threading


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
    res=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+content
    if platform.system() != 'Windows':
        cmd = 'display notification \"' + \
              content + '\" with title \"日志\"'
        call(["osascript", "-e", cmd])
    return res




# 压缩文件夹并移动
def compress(file_folder_path, folder_name, tar_dic=os.environ[config.GVC.HOME] + config.GVC.PATH["sycnPath"]):
    log_list=[]
    log_list.append(print_with_time('正在发布，请勿操作'))
    tar_file_dic = os.path.join(tar_dic, folder_name + '.7z')
    file_folder_ab_path = os.path.join(file_folder_path, folder_name)
    if platform.system() == 'Windows':
        file_folder_ab_path = "C:" + file_folder_ab_path
        tar_dic = "C:" + tar_dic
        tar_file_dic = "C:" + tar_file_dic
    if os.path.exists(file_folder_ab_path):
        with py7zr.SevenZipFile(folder_name + '.7z', 'w') as archive:
            # print_with_time("开始压缩文件夹")
            archive.writeall(file_folder_ab_path, folder_name)
            log_list.append(print_with_time('文件夹压缩成功，文件名称为：' + folder_name))
        if os.path.exists(tar_file_dic):
            os.remove(tar_file_dic)
        shutil.move(folder_name + '.7z', tar_dic)
        delete_file(file_folder_ab_path)
        log_list.append(print_with_time('发布成功！'))
    else:
        log_list.append(print_with_time('文件不存在'))
    return log_list
