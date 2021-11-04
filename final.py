import tkinter as tk
from tkinter import ttk
import datetime
import os

batches = []

for root, dirs, files in os.walk('unused/'):
    for filename in files:
        batches.append(filename) # collect unused batches' names

batches.sort()

class Window:
    def __init__(self, width, height, title="tkinter", values=[], resizable=(False, False), icon=''):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+200+200")
        self.root.resizable(resizable[0], resizable[1])
        if icon:
            self.root.iconbitmap(icon)

        self.label = tk.Label(self.root, width=15, height=2, text="Keys batches")
        self.box = ttk.Combobox(self.root, values=values, width=40, state='readonly')
        self.get_button = ttk.Button(self.root, text='Get Key', command=self.get_key)
        self.close_button = ttk.Button(self.root, text='Quit', command=self.root.destroy)
        self.text = tk.Text(self.root, width=400, height=50)

    def run(self):
        self.draw_widgets()
        self.root.mainloop()

    def get_key(self):
        batch = self.box.get()
        with open ('unused/' + batch, 'r+') as un_batch:
            key = un_batch.readline().strip()
            lines = un_batch.readlines()
            now = datetime.datetime.now()
            f_now = now.strftime('%Y/%d/%m %H:%M:%S')
            un_batch.seek(0)
            un_batch.truncate(0)
            un_batch.writelines(lines)
        with open ('used/used_' + batch, 'a') as u_batch:
            u_batch.write(f'\n{key}\n{os.getlogin()} - {f_now}\n')
        self.print_key(key)

    def draw_widgets(self):
        self.label.place(x=0, y=20)
        self.box.place(x=120, y=27)
        self.get_button.place(x=120, y= 50)
        self.close_button.place(x=220, y=50)
        self.text.place(x=0, y=75)

    def print_key(self, key='Sorry, no keys left'):
        try:
            self.text.configure(state='normal')
            self.text.delete('1.0', tk.END)
        except Exception:
            pass
        self.text.insert('1.0', key)
        self.text.configure(state='disabled')
        
window = Window(400, 150, 'Key Dispenser', batches)
window.run()