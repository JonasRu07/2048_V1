import tkinter as tk
from random import randint, seed
from math import log
from copy import deepcopy
from sys import exit
seed(1)

class GUI(object):
    def __init__(self):
        self.system : System | None = None

        self.root = tk.Tk()
        self.root.geometry('390x390')
        self.root.title('2028')

        self.frame_fields = tk.Frame(master=self.root,
                                     bg='#b6aca0',
                                     width=310,
                                     height=310)
        self.frame_fields.place(x=40, y=40)
        self.colours_fields = ['#ebdfc7', '#f3b179', '#f59561', '#f57c5f',
                               '#f95d3d', '#edce74', '#eccc61', '#ebc74f',
                               '#eec33e', '#edc229', '#ef666d', '#ed4d59',
                               '#e14338', '#72b3d9', '#5ca0dd', '#007bbe']
        self.list_fields:list[tk.Label] = []
        for i in range(16):
            self.list_fields.append(
                tk.Label(master=self.frame_fields,
                         bg='#c6bcb0')
            )
            self.list_fields[i].place(x=(i%4)*70 + 20, y=(i//4)*70 + 20, width=60, height=60)
        self.root.bind('<Up>', self.event_move)
        self.root.bind('<Down>', self.event_move)
        self.root.bind('<Left>', self.event_move)
        self.root.bind('<Right>', self.event_move)
        self.root.bind('<Escape>', self.destroy)

    def load_board(self, board:list[int]):
        for index, value in enumerate(board):
            self.list_fields[index].config(text=value if value != 0 else '')
            if value > 0:
                self.list_fields[index].config(bg=self.colours_fields[int(log(value, 2))])
            else:
                self.list_fields[index].config(bg=self.colours_fields[0])

    def event_move(self, event:tk.Event):
        self.system.move(event.keysym)

    def destroy(self, event):
        print(event)
        self.root.destroy()

    def start(self):
        self.root.mainloop()

    def set_system(self, ref_system):
        self.system = ref_system

class System(object):
    def __init__(self):
        self.gui: GUI | None = None
        self.board = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.counter = 0

    def move(self, event:str):
        start_board = deepcopy(self.board)
        if event == 'Up':
            for i in range(4):
                tmp_list = [self.board[i]] + [self.board[i + 4]] + [self.board[i + 8]] + [self.board[i + 12]]
                while 0 in tmp_list:
                    tmp_list.remove(0)
                for j in range(len(tmp_list)-1):
                    if tmp_list[j] == tmp_list[j+1]:
                        self.counter += tmp_list[j] * 2
                        tmp_list[j], tmp_list[j+1] = 0, tmp_list[j] * 2
                while 0 in tmp_list:
                    tmp_list.remove(0)
                while len(tmp_list) != 4:
                    tmp_list.append(0)
                self.board[i], self.board[i + 4], self.board[i + 8], self.board[i + 12] = \
                    tmp_list[0], tmp_list[1], tmp_list[2], tmp_list[3]
        elif event == 'Down':
            for i in range(4):
                tmp_list = [self.board[i]] + [self.board[i + 4]] + [self.board[i + 8]] + [self.board[i + 12]]
                while 0 in tmp_list:
                    tmp_list.remove(0)
                for j in range(len(tmp_list)-1):
                    if tmp_list[j] == tmp_list[j+1]:
                        self.counter += tmp_list[j] * 2
                        tmp_list[j], tmp_list[j+1] = 0, tmp_list[j] * 2
                while 0 in tmp_list:
                    tmp_list.remove(0)
                while len(tmp_list) != 4:
                    tmp_list = [0] + tmp_list
                self.board[i], self.board[i + 4], self.board[i + 8], self.board[i + 12] = \
                    tmp_list[0], tmp_list[1], tmp_list[2], tmp_list[3]
        elif event == 'Left':
            for i in range(0, 16, 4):
                tmp_list = self.board[i:i+4]
                while 0 in tmp_list:
                    tmp_list.remove(0)
                for j in range(len(tmp_list)-1):
                    if tmp_list[j] == tmp_list[j+1]:
                        self.counter += tmp_list[j] * 2
                        tmp_list[j], tmp_list[j+1] = 0, tmp_list[j] * 2
                while 0 in tmp_list:
                    tmp_list.remove(0)
                while len(tmp_list) != 4:
                    tmp_list.append(0)
                self.board = self.board[:i] + tmp_list + self.board[i+4:]
        elif event == 'Right':
            for i in range(0, 16, 4):
                tmp_list = self.board[i:i+4]
                while 0 in tmp_list:
                    tmp_list.remove(0)
                for j in range(len(tmp_list)-1):
                    if tmp_list[j] == tmp_list[j+1]:
                        self.counter += tmp_list[j] * 2
                        tmp_list[j], tmp_list[j+1] = 0, tmp_list[j] * 2
                while 0 in tmp_list:
                    tmp_list.remove(0)
                while len(tmp_list) != 4:
                    tmp_list = [0] + tmp_list
                self.board = self.board[:i] + tmp_list + self.board[i+4:]

        tmp_idx_lst  =[]
        while True:
            new_piece_index = randint(0,15)
            if new_piece_index not in tmp_idx_lst:
                tmp_idx_lst.append(new_piece_index)
                if self.board[new_piece_index] == 0:
                    new_piece_value = randint(1, 2 ) * 2
                    self.counter += new_piece_value
                    self.board[new_piece_index] = new_piece_value
                    break
            if len(tmp_idx_lst) >= 16:
                break

        if self.board == start_board:
            print(self.counter)
            exit()

        self.gui.load_board(self.board)


    def start(self):
        self.gui.load_board(self.board)
        self.gui.start()

    def set_gui(self, ref_gui):
        self.gui = ref_gui

gui = GUI()
system = System()
system.set_gui(gui)
gui.set_system(system)
system.start()