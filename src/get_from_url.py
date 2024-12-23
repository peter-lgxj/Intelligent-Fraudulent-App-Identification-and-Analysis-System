import tkinter as tk
from tkinter import messagebox
from Domain import Domain

d=Domain()

def get_from_url(d):
    def on_download():
        url = url_entry.get()
        result = d.get_from_url(url)
        if result:
            messagebox.showinfo("下载结果", "下载成功")
        else:
            messagebox.showerror("下载结果", "下载失败")

    root = tk.Tk()
    root.title("下载器")

    url_label = tk.Label(root, text="请输入URL：")
    url_label.grid(row=0, column=0, padx=5, pady=5)

    url_entry = tk.Entry(root)
    url_entry.grid(row=0, column=1, padx=5, pady=5)

    download_button = tk.Button(root, text="下载", command=on_download)
    download_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()
