import tkinter as tk
from tkinter import ttk
from time import strftime

def update_time():
    time_string = strftime('%H:%M:%S')
    clock_label.config(text=time_string)
    clock_label.after(1000, update_time)

clock_app = tk.Tk()
clock_app.title("Clock")
clock_label = ttk.Label(clock_app, font=('Helvetica', 48))
clock_label.pack(pady=20, padx=20)
update_time()
clock_app.mainloop()
