# -*- coding:UTF-8 -*-
import tkinter
import uploadfile
import os
import api
import config.GVC

path = os.environ[config.GVC.HOME] + config.GVC.PATH["HTMLPath"]


def click():
    folder_name = entry.get()
    content = te.get('0.0', 'end')
    uploadfile.compress(path, folder_name)
    api.addlog(content)


top = tkinter.Tk()
top.wm_attributes('-topmost', 1)
top.geometry("400x400+520+250")

entry = tkinter.Entry(top, width=20)
entry.insert(0, '原型-ERP')
entry.grid(row=1, column=0)

te = tkinter.Text(
    top,
    width=50,
    height=20,
    borderwidth=1,
)
te.insert(index=tkinter.END, chars='更新日志：')
te.grid(row=0, column=0)

B = tkinter.Button(
    top,
    text="发布",
    command=click
).grid(row=3, column=0)

L = tkinter.Text(
    top,
    background='#E0E0E0',
    height=2,
    width=10
).grid(row=4, column=0)

if __name__ == '__main__':
    top.mainloop()
