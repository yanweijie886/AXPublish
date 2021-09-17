# -*- coding:UTF-8 -*-
import tkinter
import uploadfile
import os
import api
import config.GVC
import tkinter as tk
import time

path = os.environ[config.GVC.HOME] + config.GVC.PATH["HTMLPath"]
project = ['小嘀师傅', '小嘀管家', '小嘀进货', '原型-ERP']





class AutoTest():


    def __init__(self):
        self.top = tkinter.Tk()
        self.top.wm_attributes('-topmost', 1)
        self.top.geometry("400x400+520+250")

        self.v = tkinter.IntVar()
        self.i = 1
        for project_name in project:
            radio = tkinter.Radiobutton(self.top, variable=self.v, text=project_name, value=self.i)
            radio.grid(row=self.i, column=0)
            self.i = self.i + 1

        self.te = tkinter.Text(
            self.top,
            width=50,
            height=20,
            borderwidth=1,
        )
        self.te.insert(index=tkinter.END, chars='更新日志：')
        self.te.grid(row=self.i + 2, column=0)

        self.B = tkinter.Button(
            self.top,
            text="发布",
            command=self.click
        ).grid(row=self.i, column=0)

        self.L = tkinter.Text(
            self.top,
            background='#E0E0E0',
            height=20,
            width=50,
        )
        self.L.grid(row=self.i + 1, column=0)

        self.top.mainloop()

    def changeText(self, content):
        self.L.insert(index=tk.END, chars=str(content) + '\n')


    def click(self):
        folder_name = project[self.v.get() - 1]
        print(folder_name)
        content = self.te.get('0.0', 'end')
        res_list=uploadfile.compress(path, folder_name)
        api.addlog(content)
        for res in res_list:
            self.changeText(res)
        time.sleep(3)




if __name__ == '__main__':

    APP = AutoTest()
