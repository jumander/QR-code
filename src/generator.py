from re import X
from qrcode import QRCode


def draw_rect(code, start, end, state=True):
  for y in range(start[1], end[1]+1):
    for x in range(start[0], end[0]+1):
      code.board[y][x].state = state

def reserve_rect(code, start, end):
  for y in range(start[1], end[1]+1):
    for x in range(start[0], end[0]+1):
      code.board[y][x].reserved = True

def get_alignment_locations(requested_version):
  table = {}
  with open("data/alignment-locations.txt") as f:
    for line in f:
      version, rest = line.split(' ')
      locs = rest.split(',')
      locs = [int(x) for x in locs]
      table[int(version)] = locs

  if requested_version in table:
    return table[requested_version]
  else:
    return []

def add_trackers(code):

  # Draw small trackers
  locs = get_alignment_locations(code.version)
  trackers = []
  for y in locs:
    for x in locs:
      if (x == 6 or x == code.size-7) and (y == 6 or y == code.size-7):
        continue
      trackers.append((x, y))
  if code.version > 1:
    trackers.append((code.size-7, code.size-7))

  for tracker in trackers:
    x, y = tracker
    reserve_rect(code, (x-2, y-2), (x+2, y+2))
    draw_rect(code, (x-2, y-2), (x+2, y+2), False)
    draw_rect(code, (x-1, y-1), (x+1, y+1), True)
    draw_rect(code, (x, y), (x, y), False)

  # Draw large trackers
  reserve_rect(code, (0, 0), (7, 7))
  reserve_rect(code, (0, code.size-8), (7, code.size-1))
  reserve_rect(code, (code.size-8, 0), (code.size-1, 7))
  for start in [(0, 0), (0, code.size-7), (code.size-7, 0)]:
    sx, sy = start
    draw_rect(code, (sx+0, sy+0), (sx+6, sy+6), False)
    draw_rect(code, (sx+1, sy+1), (sx+5, sy+5), True)
    draw_rect(code, (sx+2, sy+2), (sx+4, sy+4), False)

  # Draw timings
  for i in range(6, code.size-7):
    code.board[i][6].reserved = True
    code.board[i][6].state = i % 2
    code.board[6][i].reserved = True
    code.board[6][i].state = i % 2

  # Add dark module
  code.board[code.size-8][8].reserved = True
  code.board[code.size-8][8].state = False

def retrieve_data_path(code):

  # Reserve space for format
  reserve_rect(code, (0, 0), (8, 8))
  reserve_rect(code, (8, code.size-7), (8, code.size-1))
  reserve_rect(code, (code.size-8, 8), (code.size-1, 8))
  if code.version >= 7:
    reserve_rect(code, (0, code.size-11), (6, code.size-8))
    reserve_rect(code, (code.size-11, 0), (code.size-8, 6))

  data_path = []

  dir = -1 # -1 is upwards
  x, y = (code.size-1, code.size-1)
  sidestep = True
  while x >= 0:
    if not code.board[y][x].reserved:
      data_path.append((x, y))
    else:
      pass
    if sidestep:
      x -= 1
    else:
      if dir < 0 and y == 0:
        x -= 1 if x != (6+1) else 2
        dir = 1
      elif dir > 0 and y == code.size-1:
        x -= 1
        dir = -1
      else:
        x += 1
        y += dir
    sidestep = not sidestep
  return data_path

def encode_message(code, message):
  data_path = retrieve_data_path(code)
  print(len(data_path))

def generate(message):
  code = QRCode(1, True)

  add_trackers(code)
  encode_message(code, message)

  print(message)
  return code
