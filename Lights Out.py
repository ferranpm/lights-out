#!/usr/bin/python

import pygame, math
from pygame.locals import *

WIDTH = 480
HEIGHT = 640
NCELLS = 5
NLEVELS = 4

file_cellon = "img/CellON.png"
file_celloff = "img/CellOFF.png"
file_selecton = "img/select1.png"
file_selectoff = "img/select0.png"

CellOn = pygame.image.load(file_cellon)
CellOff = pygame.image.load(file_celloff)
SelectOn = pygame.image.load(file_selecton)
SelectOff = pygame.image.load(file_selectoff)

class Cell:
  def __init__(self, x, y):
    self.active = False
    size = WIDTH/NCELLS
    self.rect = pygame.Rect(x, y, size, size)
  
  def toggle(self):
    if self.active: self.active = False
    else: self.active = True

  def set_active(self, active):
    self.active = active

  def display(self, screen):
    if self.active: screen.blit(CellOn, self.rect)
    else: screen.blit(CellOff, self.rect)


class Board:
  def __init__(self):
    self.cells = []
    for j in range(NCELLS):
      row = []
      for i in range(NCELLS):
        x = i*(WIDTH/NCELLS)
        y = j*(WIDTH/NCELLS)
        row.append(Cell(x, y))
      self.cells.append(row)

  def __valid_position(self, x, y):
    return (x < NCELLS and x >= 0 and 
        y < NCELLS and y >= 0)

  def set_active(self, x, y, active):
    if self.__valid_position(x, y):
      self.cells[x][y].set_active(active)

  def change(self, x, y):
    if self.__valid_position(x, y): self.cells[x][y].toggle()
    if self.__valid_position(x+1, y): self.cells[x+1][y].toggle()
    if self.__valid_position(x-1, y): self.cells[x-1][y].toggle()
    if self.__valid_position(x, y+1): self.cells[x][y+1].toggle()
    if self.__valid_position(x, y-1): self.cells[x][y-1].toggle()

  def empty(self):
    for row in self.cells:
      for cell in row:
        if cell.active:
          return False
    return True

  def display(self, screen):
    for row in self.cells:
      for cell in row:
        cell.display(screen)

class SelectLevel(Board):
  def __init__(self):
    Board.__init__(self)
    i = j = 0;
    while j*NCELLS + i < NLEVELS:
      self.cells[j][i].set_active(True)
      i = i + 1
      if i >= NCELLS:
        i = 0
        j = j + 1

  def select(self, x, y):
    if x*NCELLS + y < NLEVELS:
      return x*NCELLS+y+1
    return -1

class Select:
  def __init__(self):
    self.selected = False
    height = HEIGHT - WIDTH
    self.rect = pygame.Rect(0, WIDTH, WIDTH, height)

  def toggle(self):
    if self.selected: self.selected = False;
    else: self.selected = True

  def display(self, screen):
    if self.selected: screen.blit(SelectOn, self.rect)
    else: screen.blit(SelectOff, self.rect)

class LevelHandler:
  def __init__(self):
    self.level = 1

  def set_level(self, level):
    self.level = level

  def next_level(self):
    self.level = self.level + 1
    if self.level > 4: self.level = 1

  def read_level(self, board):
    file_level = "lvl/" + str(self.level)
    f = open(file_level, "r")
    string = f.read()
    i = j = 0
    for c in string:
      if c != '\n':
        if c == 'o': board.set_active(j, i, True)
        elif c == 'x': board.set_active(j, i, False)
        i = i + 1
      else:
        i = 0
        j = j + 1

def RenderText(screen, text, size, pos):
  font = pygame.font.SysFont(pygame.font.get_default_font(), size)
  screen.blit(font.render(text, True, (0,0,0)), pos)

def LevelLoad(screen):
  board = Board()
  for row in board.cells:
    for cell in row:
      cell.set_active(True)
      board.display(screen)
      pygame.time.delay(50)
      cell.set_active(False)
      pygame.display.flip()
  pygame.event.get()

if __name__ == '__main__':
  pygame.font.init()
  pygame.display.init()
  pygame.display.set_icon(CellOff)
  pygame.display.set_caption("Lights Out")

  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  running = True
  board = Board()
  select = Select()
  select_level = SelectLevel()
  level_handler = LevelHandler()

  level_handler.read_level(board)

  select.display(screen)
  #LevelLoad(screen)

  while running:
    if (select.selected): select_level.display(screen)
    else: board.display(screen)
    select.display(screen)
    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == QUIT:
        running = False
      if event.type == MOUSEBUTTONDOWN:
        if event.pos[1] < WIDTH and not select.selected:
          x = int(math.floor(event.pos[1]/(WIDTH/NCELLS)))
          y = int(math.floor(event.pos[0]/(WIDTH/NCELLS)))
          board.change(x,y)
        elif event.pos[1] < WIDTH and select.selected:
          x = int(math.floor(event.pos[1]/(WIDTH/NCELLS)))
          y = int(math.floor(event.pos[0]/(WIDTH/NCELLS)))
          lvl = select_level.select(x,y)
          if lvl > 0:
            level_handler.set_level(lvl)
            level_handler.read_level(board)
            select.selected = False
        elif event.pos[1] > WIDTH:
          select.toggle()

    if board.empty():
      level_handler.next_level()
      level_handler.read_level(board)

  pygame.display.quit()
