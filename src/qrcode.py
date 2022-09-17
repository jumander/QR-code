from enum import Enum
import numpy as np

class Block:
  def __init__(self, state=False):
    self.state = state
    self.reserved = False


class QRCode:
  def __init__(self, version, state=False):
    assert(isinstance(version, int))
    assert(version >= 1 and version <= 40)
    self.version = version
    self.size = version * 4 + 17
    self.board = [[Block(state) for x in range(self.size)] for y in range(self.size)]