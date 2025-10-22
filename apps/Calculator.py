import tkinter as tk

def on_button_click(value):
    if value == "=":
        try:
            entry_var.set(eval(entry_var.get()))  # Evaluate the expression
        except Exception:
            entry_var.set("Error")  # Handle invalid expressions
    elif value == "C":
        entry_var.set("")  # Clear the entry field
    else:
        entry_var.set(entry_var.get() + value)  # Append character to the entry field

calc_app = tk.Tk()
calc_app.title("Calculator")

entry_var = tk.StringVar()
entry = tk.Entry(calc_app, textvariable=entry_var, font=("Helvetica", 24), justify='right')
entry.grid(row=0, column=0, columnspan=4)
entry_var.set("")  # Initialize with an empty string

buttons = [
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('C', '0', '=', '+')
]

for r, row in enumerate(buttons):
    for c, char in enumerate(row):
        tk.Button(calc_app, text=char, font=("Helvetica", 20), width=5, height=2,
                  command=lambda ch=char: on_button_click(ch)).grid(row=r+1, column=c, sticky='nsew')

calc_app.mainloop()
