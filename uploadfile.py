import shutil
import stat
import py7zr
import os
import os.path
import time
from subprocess import call


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
    cmd = 'display notification \"' + \
          content + '\" with title \"日志\"'
    call(["osascript", "-e", cmd])


# 压缩文件夹并移动
def compress(file_folder_path, folder_name, tar_dic=os.environ['HOME'] + '/SynologyDrive'):
    print_with_time('正在发布，请勿操作')
    if os.path.exists(os.path.join(file_folder_path, folder_name)):
        with py7zr.SevenZipFile(folder_name + '.7z', 'w') as archive:
            # print_with_time("开始压缩文件夹")
            archive.writeall(file_folder_path + folder_name, folder_name)
            print_with_time('文件夹压缩成功，文件名称为：' + folder_name)
            if os.path.exists(os.path.join(tar_dic, folder_name + '.7z')):
                os.remove(os.path.join(tar_dic, folder_name + '.7z'))
            shutil.move(folder_name + '.7z', tar_dic)
            delete_file(file_folder_path + folder_name)
            print_with_time('发布成功！')
    else:
        print_with_time('文件不存在')


