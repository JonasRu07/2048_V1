import tkinter as tk
from random import randint, seed
from math import log
from copy import deepcopy
from sys import exit
seed(1)

#TODO: !! proper check if no available move is possible; don't rely on smart people to not fuck up
#TODO: optimise move -> redundant code, just moving things in general
#TODO: general code structure -> packing things together which belong together
#TODO: DOCUMENT THE SHIT OUT OF THIS

class GUI(object):
    def __init__(self):
        self.system : System | None = None

        self.root = tk.Tk()
        self.root.geometry('490x390')
        self.root.title('2048')

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

        self.label_counter = tk.Label(master = self.root,
                                      bg='#11998e',
                                      font='Aral, 20',
                                      text='NAN')
        self.label_counter.place(x=370, y=40, width=100, height=40)

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

    def update_counter(self, value):
        self.label_counter.config(text=value)

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
        self.board = [0]*16
        self.counter = 0

    def move(self, event:str):
        start_board = deepcopy(self.board)
        if event == 'Up':
            for i in range(4):
                tmp_list = [self.board[i]] + [self.board[i + 4]] + [self.board[i + 8]] + [self.board[i + 12]]
                tmp_list = self.move_aid(tmp_list, in_front=False)
                self.board[i], self.board[i + 4], self.board[i + 8], self.board[i + 12] = tmp_list
        elif event == 'Down':
            for i in range(4):
                tmp_list = [self.board[i]] + [self.board[i + 4]] + [self.board[i + 8]] + [self.board[i + 12]]
                tmp_list = self.move_aid(tmp_list, in_front=True)
                self.board[i], self.board[i + 4], self.board[i + 8], self.board[i + 12] = tmp_list
        elif event == 'Left':
            for i in range(0, 16, 4):
                tmp_list = self.board[i:i+4]
                tmp_list = self.move_aid(tmp_list, in_front=False)
                self.board = self.board[:i] + tmp_list + self.board[i+4:]
        elif event == 'Right':
            for i in range(0, 16, 4):
                tmp_list = self.board[i:i+4]
                tmp_list = self.move_aid(tmp_list, in_front= True)
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
        self.gui.update_counter(self.counter)
        self.gui.load_board(self.board)
        if self.board == start_board:
            print(self.counter)
            exit()

    def move_aid(self, lst:list[int], in_front:bool = True):
        work_list = lst
        current_value = (0, -1)
        for i in range(len(work_list)):
            if in_front: # Check for direction as right/down need inverted list iteration for right combining of values
                i = -(i+1)
            if work_list[i] == 0:
                continue
            else:
                if current_value[0] != work_list[i]:
                    current_value = (work_list[i], i)
                elif current_value[0] == work_list[i]:
                    self.counter += current_value[0] * 2
                    work_list[current_value[1]] = current_value[0] * 2
                    work_list[i] = 0
                    current_value = (0, -1)
        work_list = [y for y in work_list if y != 0]
        while len(work_list) != 4:
            if in_front:
                work_list = [0] + work_list
            else:
                work_list.append(0)
        return work_list

    def start(self):
        self.gui.load_board(self.board)
        self.gui.start()

    def set_gui(self, ref_gui):
        self.gui = ref_gui


#Code execution and setup
gui = GUI()
system = System()
system.set_gui(gui)
gui.set_system(system)
system.start()