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
  def __init__(self, version, state=False):
    assert(isinstance(version, int))
    assert(version >= 1 and version <= 40)
    self.version = version
    self.size = version * 4 + 17
    self.board = [[Block(state) for x in range(self.size)] for y in range(self.size)]