from enum import Enum
import numpy as np

class BlockType(Enum):
  UNINITIALIZED = 1
  RESERVED = 2
  DATA = 3


class Block:
  def __init__(self, state=False, block_type=BlockType.UNINITIALIZED):
    self.state = state
    self.block_type = block_type


class QRCode:
  def __init__(self, size, state=False):
    self.size = size
    self.board = [[Block(state) for x in range(size)] for y in range(size)]