# -*- coding:UTF-8 -*-
# 只支持windows系统
import os.path
import stat
import time
import operator
import os
import py7zr
import shutil

sys_user_path = os.path.expanduser('~')
html_file_path = sys_user_path + '/Documents/Axure/HTML/'
seven_zip_temp_dir = sys_user_path + '\\Documents\\我的坚果云\\7z'


# 删除文件，文件路径
def delete_file(file_path):
    if os.path.exists(file_path):
        for fileList in os.walk(file_path):
            for name in fileList[2]:
                os.chmod(os.path.join(fileList[0], name), stat.S_IWRITE)
                os.remove(os.path.join(fileList[0], name))
        shutil.rmtree(file_path)
        print("删除成功", file_path)
    else:
        print("删除失败，因为找不到此文件", file_path)


# 发布原型文件（源路径、文件名、发布目的路径）
def publish(source, file_name, target_dir=html_file_path):
    # 压缩包来源目录
    # 解压到
    delete_file(target_dir + '/' + file_name.split('.')[0])
    files = os.listdir(source)
    for f in files:
        if f == file_name:
            f_path = source + os.sep + f
            if os.path.isfile(f_path):
                exn = f.split(".")[-1]
                if exn == "7z" or exn == 'zip':
                    d_name = f.split(".")[0]
                    target = target_dir + os.sep
                    # print(f_path,"===>",target)
                    # 解压命令(密码为文件名所以是d_name)
                    cmd = "7za.exe x %s -p%s -o%s -aoa" % (f_path, d_name, target)
                    print(cmd)
                    # 文件解压是否失败情况写入文本文档。
                    f = "error.txt"
                    with open(f, "r+") as file:
                        # os.system(cmd)命令执行成功时返回0
                        txtcontent = file.read()
                        file.seek(0, 0)
                        if os.system(cmd) == 0:
                            file.write(str(time.strftime("%Y-%m-%d %H:%M:%S",
                                                         time.localtime())) + d_name + "-发布成功" + "\n" + txtcontent)
                            print("----------------原型发布成功！------------------")
                            os.remove(source + '\\' + file_name)
                            delete_file(target_dir + '/__MACOSX')
                            print("压缩文件已删除！" + "\n")
                        else:
                            file.write(str(time.strftime("%Y-%m-%d %H:%M:%S",
                                                         time.localtime())) + d_name + "-error" + "\n" + txtcontent)


# 压缩文件
def compress(file_folder_path, file_folder_name):
    with py7zr.SevenZipFile(file_folder_name + '.7z', 'w') as archive:
        archive.writeall(file_folder_path + file_folder_name, file_folder_name)
        shutil.move(file_folder_name + '.7z', sys_user_path + '/Nutstore Files/我的坚果云/7z')  # move file


# 解压缩并发布
# 判断文件是否存在
def if_exist():
    filename = 'out.txt'
    if os.path.exists(filename):
        # message = 'OK, the "%s" file exists.'
        return
    else:
        message = "Sorry, I cannot find the '%s' file..but I create it."
        a = open('out.txt', 'w', encoding='utf-8')
        a.close()
        print(message % filename)


# 文件全路径和对应最后修改时间写入到out.txt文档中；
def update_log(file_dir):
    with open('out.txt', 'w') as f:
        f.close()
    for file_name in os.listdir(file_dir):
        if ('.7z' in file_name or '.zip' in file_name) and '.icloud' not in file_name and '.nssyncsc' not in file_name:
            file_path = os.path.join(file_dir, file_name)
            file_time = os.stat(file_path).st_mtime
            with open('out.txt', 'a', encoding='utf-8') as f:
                f.write(','.join(['%s' % file_name, '%s\n' % file_time]))
                f.close()


def log_compare(file_dir):
    # 先确保out.txt存在
    if_exist()
    # 获取out.txt文件内容（文件全路径key和最后修改时间value），生成dict
    txt = open('out.txt', 'r', encoding='utf-8').readlines()
    file_dic = {}
    for row in txt:
        if row != '\n' and ',' in row:
            (key, value) = row.split(',')
            file_dic[key] = value
    # print(myDic)
    new_file_list = []
    for file_name in os.listdir(file_dir):
        if ('.7z' in file_name or '.zip' in file_name) and '.icloud' not in file_name and '.nssyncsc' not in file_name:
            file_path = os.path.join(file_dir, file_name)
            file_time = os.stat(file_path).st_mtime
            file_time = '%s\n' % file_time
            if file_name in file_dic:
                if not operator.eq(file_time, file_dic[file_name]):
                    new_file_list.append(file_name)
            if file_name not in file_dic:
                with open('out.txt', 'a', encoding='utf-8') as f:
                    f.write(','.join(['%s' % file_name, '%s\n' % file_time]))
                    f.close()
                    print(file_name + '追加成功')
                    publish(file_dir + '\\', file_name)

    if len(new_file_list) > 0:
        print(new_file_list)
    return new_file_list


def loop_monitor():
    while True:
        # publish()
        new_file_list = log_compare(seven_zip_temp_dir)
        if len(new_file_list) > 0:
            update_log(seven_zip_temp_dir)
            for folder in new_file_list:
                publish(seven_zip_temp_dir, folder)

        # s检查一次
        time.sleep(10)


if __name__ == '__main__':
    loop_monitor()
# git init
# git remote add origin http://118.24.156.138:30000/root/axps.git
# git add .
# git commit -m "Initial commit"
# git push -u origin master
