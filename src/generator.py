from qrcode import QRCode


def draw_rect(code, start, end, state=True):
  for y in range(start[1], end[1]+1):
    for x in range(start[0], end[0]+1):
      code.board[y][x].state = state

def add_trackers(code):
  # Draw large trackers
  for start in [(0, 0), (0, code.size-7), (code.size-7, 0)]:
    sx, sy = start
    draw_rect(code, (sx+0, sy+0), (sx+6, sy+6), False)
    draw_rect(code, (sx+1, sy+1), (sx+5, sy+5), True)
    draw_rect(code, (sx+2, sy+2), (sx+4, sy+4), False)

  # Draw timings
  for i in range(6, code.size-7):
    code.board[i][6].state = i % 2
    code.board[6][i].state = i % 2

def generate(message):
  code = QRCode(21, True)

  add_trackers(code)

  print(message)
  return code