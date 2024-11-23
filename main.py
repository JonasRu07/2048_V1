import tkinter as tk
from random import randint, seed
from math import log
from copy import deepcopy
seed()

#TODO: optimise move -> redundant code (ex. gui.update_...(), same params with nearly the same execution)

class GUI(object):
    """
    Visual interface of the game "2048"
    """
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

        self.label_counter = tk.Label(master=self.root,
                                      bg='#11998e',
                                      font='Aral, 20',
                                      text='NAN')
        self.label_counter.place(x=370, y=40, width=100, height=40)

        self.label_last_score = tk.Label(master=self.root,
                                        bg='white',
                                        font='Aral, 20',
                                        text='NAN')
        self.label_last_score.place(x=370, y=100, width=100, height=40)

        self.label_highscore = tk.Label(master=self.root,
                                        bg='white',
                                        font='Aral, 20',
                                        text='NAN')
        self.label_highscore.place(x=370, y=160, width=100, height=40)


        self.root.bind('<Up>', self.event_move)
        self.root.bind('<Down>', self.event_move)
        self.root.bind('<Left>', self.event_move)
        self.root.bind('<Right>', self.event_move)
        self.root.bind('<Escape>', self.destroy)

    def load_board(self, board:list[list[int]]):
        for i in range(16):
            field = self.list_fields[i]
            value = board[i%4][i//4]
            if value != 0:
                colour = self.colours_fields[int(log(value, 2))]
                field.config(text=value,
                             bg=colour)
            else:
                field.config(text='',
                             bg=self.colours_fields[0])

    def update_counter(self, value:int):
        self.label_counter.config(text=value)

    def update_last_score(self, value:int):
        self.label_last_score.config(text=value)

    def update_highscore(self, value:int):
        self.label_highscore.config(text=value)

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
    """
    The "brain" of the program. It keeps trak of the current position and other values stored. All, calculation take
    here place and are given out as parameters
    """
    def __init__(self):
        self.gui: GUI | None = None
        self.board: list[list[int]] = [[0, 0, 0, 0],
                                       [0, 0, 0, 0],
                                       [0, 0, 0, 0],
                                       [0, 0, 0, 0]]
        self.counter: int = 0
        self.highscore: int = 0

    def move(self, event: str, change: bool = True) -> bool | None:
        """
        control of all possible moves, currently all main action happening here
        :param event: event of the arrow keys of a keyboard
        :param change: if the board should be updated
        :return: None
        """
        start_board = deepcopy(self.board)
        tmp_counter = deepcopy(self.counter)
        if event == 'Up':
            for i in range(0, 4):
                tmp_list = start_board[i]
                tmp_list, tmp_counter = self.__move_aid(tmp_list, tmp_counter, in_front=False)
                start_board[i] = tmp_list
        elif event == 'Down':
            for i in range(0, 4):
                tmp_list = start_board[i]
                tmp_list, tmp_counter = self.__move_aid(tmp_list, tmp_counter, in_front=True)
                start_board[i] = tmp_list
        elif event == 'Left':
            for i in range(4):
                tmp_list = [start_board[0][i]] + [start_board[1][i]] + [start_board[2][i]] + [start_board[3][i]]
                tmp_list, tmp_counter = self.__move_aid(tmp_list, tmp_counter, in_front=False)
                for j in range(4):
                    start_board[j][i] = tmp_list[j]
        elif event == 'Right':
            for i in range(4):
                tmp_list = [start_board[0][i]] +[start_board[1][i]] +[start_board[2][i]] +[start_board[3][i]]
                tmp_list, tmp_counter = self.__move_aid(tmp_list, tmp_counter, in_front=True)
                for j in range(4):
                    start_board[j][i] = tmp_list[j]

        if change:
            self.board = start_board
            self.counter = tmp_counter
            self.__post_move_actions()
        else:
            if start_board == self.board:
                return False
            else:
                return True

    def possible_moves_available(self, check_board:list[list[int]]) -> bool:
        for i in range(4):
            if 0 in check_board:
                return True
            else:
                if self.move('Up', False) or \
                        self.move('Down', False) or \
                        self.move('Right', False) or \
                        self.move('Left', False):
                    return True
                else:
                    return False

    def __move_aid(self, lst: list[int], counter:int, in_front: bool = True) -> (list[int], int):
        """
        support method for move \n
        checking for two fields to merge together and moving them around the board
        :param lst: list of 4 fields of a line that will move together
        :param in_front: if the list needs to be filled up from the front or the back, also used for checking the
         direction multiple fields should be merged together in case of ex. 3 same valued fields next to each other
        :return: list with merged and added fields
        """
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
                    counter += current_value[0] * 2
                    work_list[current_value[1]] = current_value[0] * 2
                    work_list[i] = 0
                    current_value = (0, -1)
        work_list = [y for y in work_list if y != 0]
        while len(work_list) != 4:
            if in_front:
                work_list = [0] + work_list
            else:
                work_list.append(0)
        return work_list, counter

    def __post_move_actions(self):

        tmp_idx_lst = []
        while True:
            new_piece_index = randint(0, 15)
            if new_piece_index not in tmp_idx_lst:
                tmp_idx_lst.append(new_piece_index)
                if self.board[new_piece_index // 4][new_piece_index % 4] == 0:
                    new_piece_value = randint(1, 2) * 2
                    self.counter += new_piece_value
                    self.board[new_piece_index // 4][new_piece_index % 4] = new_piece_value
                    break
            if len(tmp_idx_lst) >= 16:
                break

        if self.counter >= self.highscore:
            self.highscore = self.counter
            self.gui.update_highscore(self.highscore)
        if not self.possible_moves_available(self.board):
            self.gui.update_last_score(self.counter)
            self.counter = 0
            self.board = [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]
        self.gui.update_counter(self.counter)
        self.gui.load_board(self.board)

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