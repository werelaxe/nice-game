import queue
from random import random, randint, choice
from itertools import product

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def plus(first, second):
    return first[0] + second[0], first[1] + second[1]


class Field:
    def __init__(self, width, height):
        self.map = []
        self.width = width
        self.height = height
        self.player_pos = 0, 0
        self.show_map = False
        self.probability = 0.4
        self.count_around = -1
        self.path = []
        self.create_map()
        self.update_count_around()

    def __setitem__(self, key, value):
        self.map[key[0]][key[1]] = value

    def __getitem__(self, item):
        return self.map[item[0]][item[1]]

    def create_map(self):
        self.generate_map()
        while not self.exists_way():
            self.generate_map()
            self.probability += 0.001
        self.path = self.bfs((0, 0),
                             (self.width - 1, self.height - 1), True)[1]

    def show_rand_cell(self):
        if self.path:
            self[choice(list(self.path))].hidden = False

    def generate_map(self):
        self.map = []
        for index_x in range(self.width):
            self.map.append([])
            for index_y in range(self.height):
                self.map[index_x].append(Cell(True, random() > self.probability))
        self[(0, 0)] = Cell(True, False)
        self[(self.width - 1, self.height - 1)] = Cell(True, False)

    def is_inside(self, pos):
        return (pos[0] < self.width) and (pos[0] >= 0)\
               and (pos[1] < self.height) and (pos[1] >= 0)

    def update_count_around(self):
        count_around = 0
        for offset in product([-1, 0, 1], repeat=2):
            neigboor = plus(self.player_pos, offset)
            if self.is_inside(neigboor) and\
                    any(offset) and self[neigboor].dang:
                count_around += 1
        self.count_around = count_around

    def reverse_cell(self, cell):
        coord_x, coord_y = cell
        return self.width - coord_x - 1, self.height - coord_y - 1

    def step(self, dir):
        new_pos = plus(dir, self.player_pos)
        if self.is_inside(new_pos):
            if new_pos == (self.width - 1, self.height - 1):
                self.show_map = True
            if self[new_pos].dang:
                self[new_pos].hidden = False
                self[self.player_pos].hidden = False
                self.player_pos = 0, 0
            else:
                if self[self.player_pos].hidden:
                    self.show_rand_cell()
                self[self.player_pos].hidden = False

                self.player_pos = new_pos
        self.update_count_around()

    def exists_way(self):
        start = (0, 0)
        finish = (self.width - 1, self.height - 1)
        return self.bfs(start, finish, False)[0]

    def bfs(self, start, finish, find_way):
        q = queue.Queue()
        used = set()
        used.add(start)
        q.put(start)
        path = {}
        cells = set()
        way_exists = False
        while not q.empty():
            buff = q.get()
            for offset in DIRS:
                neib = plus(offset, buff)
                if self.is_inside(neib):
                    if (neib not in used) and (not self[neib].dang):
                        q.put(neib)
                        used.add(neib)
                        path[neib] = buff
                        if neib == finish:
                            way_exists = True
        if find_way:
            if finish in path:
                cells.add(finish)
                current_cell = finish
                while current_cell != start:
                    current_cell = path[current_cell]
                    cells.add(current_cell)
                cells.add(start)
        return way_exists, cells

    def show_way(self):
        cells = self.bfs((0, 0), (self.width - 1, self.height - 1), True)[1]
        for cell in cells:
            self[cell].hidden = False


class Cell:
    def __init__(self, hidden, dang):
        self.hidden = hidden
        self.dang = dang

    def __str__(self):
        return "Cell(hidden={}, dangerous={})".format(self.hidden, self.dang)
