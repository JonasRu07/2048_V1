import tkinter as tk
from random import randint


class GUI(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('512x512+-1000+500')
        self.root.title('2028')

        self.frame_fields = tk.Frame(master=self.root,
                                     bg='#b6aca0',
                                     width=300,
                                     height=300)
        self.frame_fields.place(x=40, y=40)
        self.colours_fields = ['#ece0c8', '#f5b178', '#f79460']
        self.list_fields:list[tk.Label] = []
        for i in range(16):
            self.list_fields.append(
                tk.Label(master=self.frame_fields,
                         bg='#c6bcb0',
                         text=i)
            )
            self.list_fields[i].place(x=(i%4)*70 + 20, y=(i//4)*70 + 20, width=60, height=60)
        self.root.bind('<Up>', self.up)
        self.root.bind('<Down>', self.up)
        self.root.bind('<Left>', self.up)
        self.root.bind('<Right>', self.up)
        self.root.bind('<Escape>', self.destroy)
        self.root.mainloop()

    def up(self, event):
        pass

    def down(self, event):
        pass

    def left(self, event):
        pass

    def right(self, event):
        pass

    def destroy(self, event):
        self.root.destroy()
