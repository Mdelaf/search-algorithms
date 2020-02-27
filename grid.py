import tkinter as tk
import tkinter.ttk as ttk
import threading
from time import sleep
from algorithms import depth_first_search, breadth_first_search, \
    iterative_depth_first_search, best_first_search, a_star


ALGORITHMS = {
    'Depth First Search (blind)': depth_first_search,
    'Breadth First Search (blind, optimal)': breadth_first_search,
    'Iterative DFS (blind, optimal)': iterative_depth_first_search,
    'Best First Search (aware)': best_first_search,
    'A Star (aware, optimal)': a_star
}


class GraphicGrid(tk.Tk):
    def __init__(self, height, width, allow_diagonals=False, interval=0.02):
        super().__init__(None)
        self.xheight = height
        self.xwidth = width
        self.height = max(height, 2)
        self.width = max(width, 24)
        self.start_pos = None
        self.end_pos = None
        self.allow_diagonals = allow_diagonals
        self.interval = interval
        self.simulation_running = False

        # Main Window title
        self.title("Search Algorithms")

        # Start button
        self.start_btn = tk.Button(self, text="Start Simulation", command=self.start_simulation)
        self.start_btn.grid(row=self.height, column=self.width - 3, columnspan=3, sticky='nesw')

        # Clear traceback
        self.clear_tb_btn = tk.Button(self, text="Clear traceback", command=self.reset_grid)
        self.clear_tb_btn.grid(row=self.height, column=self.width - 7, columnspan=3, sticky='nesw')

        # Operator selector buttons
        self.operator = tk.StringVar()
        self.rd_start = tk.Radiobutton(self, text="Start pos", indicatoron=0,
                                       variable=self.operator, value="start")
        self.rd_start.grid(row=self.height, column=1, columnspan=2, sticky="nesw")
        self.rd_end = tk.Radiobutton(self, text="End pos", indicatoron=0,
                                     variable=self.operator, value="end")
        self.rd_end.grid(row=self.height, column=4, columnspan=2, sticky="nesw")
        self.rd_obs = tk.Radiobutton(self, text="Obstacle", indicatoron=0,
                                     variable=self.operator, value="obstacle")
        self.rd_obs.grid(row=self.height, column=7, columnspan=2, sticky="nesw")

        # Algorithm combobox
        self.algorithms_cb = ttk.Combobox(self, values=[algorithm_name for algorithm_name in ALGORITHMS.keys()])
        self.algorithms_cb.set(next(iter(ALGORITHMS.keys())))
        self.algorithms_cb.grid(row=self.height, column=10, columnspan=6, sticky='nesw')

        # Cells
        self.cells = {}
        for r in range(self.xheight):
            for c in range(self.xwidth):
                cell = Cell(self, c, r, ' o ')
                self.cells.update({(c, r): cell})
        self.start_pos = self.cells[(0, 0)]
        self.start_pos.mark_as_initial()
        self.end_pos = self.cells[(self.xwidth - 1, self.xheight - 1)]
        self.end_pos.mark_as_final()

    def get_cell(self, x, y):
        return self.cells[(x, y)]

    def distance(self, cell_1, cell_2):
        x_dif = abs(cell_1.x - cell_2.x)
        y_dif = abs(cell_1.y - cell_2.y)
        if self.allow_diagonals:
            return max(x_dif, y_dif)
        else:
            return x_dif + y_dif

    def neighbour_cells(self, cell):
        for x in range(cell.x - 1, cell.x + 2):
            for y in range(cell.y - 1, cell.y + 2):
                if (x, y) != (cell.x, cell.y) and 0 <= x < self.xwidth and 0 <= y < self.xheight:
                    if self.allow_diagonals or (cell.x == x) or (cell.y == y):
                        neighbour_cell = self.cells[(x, y)]
                        if not neighbour_cell.is_obstacle:
                            yield neighbour_cell

    def mark_cell(self, cell):
        if self.simulation_running:
            return
        op = self.operator.get()
        if op == "start":
            self.start_pos.mark_as_white()
            self.start_pos = cell
            self.start_pos.mark_as_initial()
        elif op == "end":
            self.end_pos.mark_as_white()
            self.end_pos = cell
            self.end_pos.mark_as_final()
        elif op == "obstacle":
            if cell.is_initial or cell.is_final:
                return
            if cell.is_obstacle:
                cell.mark_as_white()
            else:
                cell.mark_as_obstacle()

    def mark_visited_cell(self, cell):
        cell.mark_as_visited()
        sleep(self.interval)

    def mark_traceback(self, cell):
        while cell.parent is not None:
            cell.mark_as_traceback()
            cell = cell.parent

    def reset_grid(self):
        for cell in self.cells.values():
            cell.reset()

    def start_simulation(self):
        self.reset_grid()
        t = threading.Thread(target=self._start_simulation)
        t.setDaemon(True)
        t.start()

    def _start_simulation(self):
        print("Simulation initialized")
        self.simulation_running = True
        self.start_btn['state'] = 'disabled'
        self.clear_tb_btn['state'] = 'disabled'
        algorithm = ALGORITHMS.get(self.algorithms_cb.get(), lambda *_: print('Invalid algorithm'))
        algorithm(self)
        self.start_btn['state'] = 'normal'
        self.clear_tb_btn['state'] = 'normal'
        self.simulation_running = False


class Cell(tk.Label):

    def __init__(self, parent, x, y, value):
        super().__init__(parent, text=value, font=('Courier New', 11))
        self.bind("<Button-1>", lambda *_: self.master.mark_cell(self))
        self.grid(row=y, column=x)
        self.x = x
        self.y = y
        self.value = value
        self.parent = None
        self.depth = 0  # Used by A* (cost) and IDFS
        self.is_obstacle = False
        self.is_initial = False
        self.is_final = False
        self.mark_as_white()

    def mark_as_initial(self):
        self.is_initial = True
        self.is_final = False
        self.is_obstacle = False
        self['bg'] = 'orange'

    def mark_as_final(self):
        self.is_initial = False
        self.is_final = True
        self.is_obstacle = False
        self['bg'] = 'red'

    def mark_as_obstacle(self):
        self.is_initial = False
        self.is_final = False
        self.is_obstacle = True
        self['bg'] = 'black'

    def mark_as_white(self):
        self.is_initial = False
        self.is_final = False
        self.is_obstacle = False
        self['bg'] = 'white'

    def mark_as_visited(self):
        if not (self.is_initial or self.is_final):
            self['bg'] = 'green'

    def mark_as_traceback(self):
        if not (self.is_initial or self.is_final):
            self['bg'] = 'yellow'

    def reset(self):
        self.parent = None
        self.depth = 0
        if not any([self.is_final, self.is_initial, self.is_obstacle]):
            self.mark_as_white()
