import tkinter
import mail
import uploadfile
import os

path = os.environ['HOME'] + '/Documents/Axure/HTML/'


def click(file_folder_path, folder_name, content, x):
    uploadfile.compress(file_folder_path, folder_name)
    if x == 2:
        mail.send_mail(folder_name, content)


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

if __name__ == '__main__':
    top.mainloop()
