"""
Hi future me,
this script is kind of funny because of the default version of tkinter
that is installed on mac os x systems.

For this to work, we have to use the python installed by homebrew, not by
conda aka =>
"""
#!/opt/homebrew/bin/python3

from chaos_knob import ChaosKnob
import tkinter as tk
from tkinter import font as tkFont
from tkdial import Dial


chaos_knob = ChaosKnob()

app = tk.Tk()

helv36 = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)

colors = ("red", "pink")
dial = Dial(master=app, color_gradient=colors, unit_length=20, radius=80, needle_color=colors[1], start=0, end=11, text_color="red")
dial.grid(padx=10, pady=10, row=1, column=0)

def button_click():
  chaos_knob.do_it(chaos=dial.get())

b = tk.Button(app, bg="#222222", fg="#ffaa00", text="ENGAGE", width=10, height=3, font=helv36, command=button_click)
b.grid(padx=10, pady=10, row=2, column=0)

app.mainloop()