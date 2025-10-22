import os
import tkinter as tk
from tkinter import messagebox

def kill_explorer():
    os.system("taskkill /F /IM explorer.exe")
    messagebox.showinfo("Explorer", "Explorer.exe has been terminated!")

def restart_explorer():
    os.system("start explorer.exe")
    messagebox.showinfo("Explorer", "Explorer.exe has been restarted!")

root = tk.Tk()
root.title("Explorer Control")
root.geometry("300x150")

tk.Button(root, text="Kill Explorer", command=kill_explorer, bg="red", fg="white").pack(pady=10)
tk.Button(root, text="Restart Explorer", command=restart_explorer, bg="green", fg="white").pack(pady=10)

tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

root.mainloop()
