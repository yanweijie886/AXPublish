# -*- coding:UTF-8 -*-
import tkinter
import uploadfile
import os
import api
import config.GVC
import time

path = os.environ[config.GVC.HOME] + config.GVC.PATH["HTMLPath"]

project=['小嘀师傅','小嘀管家','小嘀进货','原型-ERP']

def click():
    folder_name = project[v.get()-1]
    print(folder_name)
    content = te.get('0.0', 'end')
    uploadfile.compress(path, folder_name)
    api.addlog(content)
    time.sleep(3)


top = tkinter.Tk()
top.wm_attributes('-topmost', 1)
top.geometry("400x400+520+250")


v=tkinter.IntVar()
i=1
for project_name in project:
    radio=tkinter.Radiobutton(top,variable=v,text=project_name,value=i)
    radio.grid(row=i, column=0)
    i=i+1

te = tkinter.Text(
    top,
    width=50,
    height=20,
    borderwidth=1,
)
te.insert(index=tkinter.END, chars='更新日志：')
te.grid(row=i+2, column=0)

B = tkinter.Button(
    top,
    text="发布",
    command=click
).grid(row=i, column=0)

L = tkinter.Text(
    top,
    background='#E0E0E0',
    height=2,
    width=10
).grid(row=i+1, column=0)

if __name__ == '__main__':
    top.mainloop()
